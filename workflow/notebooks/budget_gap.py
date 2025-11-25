# Anlyse budget gap of supply demand curve

# Import packages
import numpy as np
import pandas as pd


def interpolate_price_from_demand_curve(demand_slice, volume):
    """
    Returns the interpolated demand price at a given import volume (PyPSA-Eur).
    """

    df = demand_slice.sort_values("import_H2_demand").reset_index(drop=True)
    q = df["import_H2_demand"].to_numpy()
    p = df["price"].to_numpy()

    # Below minimum → use first price
    if volume <= q[0]:
        return float(p[0])
    # Above maximum → use last price
    if volume >= q[-1]:
        return float(p[-1])

    # Find bounding index for interpolation
    idx = np.searchsorted(q, volume)
    q1, q2 = q[idx - 1], q[idx]
    p1, p2 = p[idx - 1], p[idx]

    # Find bounding index for interpolation
    return float(p1 + (p2 - p1) * (volume - q1) / (q2 - q1))


def make_marginal_supply_curve(supply_slice):
    """
    Converts supply curve into marginal supply intervals.
    """

    sup = supply_slice.sort_values("price").copy()
    sup["x_right"] = sup["import_demand"].cumsum()
    sup["x_left"] = sup["x_right"].shift(fill_value=0)
    return sup[["x_left", "x_right", "price"]]


def get_marginal_supply_price(marginal_supply, volume):
    """
    Returns the supply price of the marginal exporter at a given volume.
    """

    row = marginal_supply[marginal_supply["x_right"] >= volume].iloc[0]
    return float(row["price"])


def calculate_budget_gap(
    supply_curve,
    demand_curve,
    region,
    scenario,
    year,
    step=1.0
):
    """
    Analyse the budget gap between supply and demand.
    """

    # Filter demand
    demand_slice = demand_curve[
        (demand_curve["year"] == year) &
        (demand_curve["region"] == region) &
        (demand_curve["scenario"] == scenario)
    ]
    if demand_slice.empty:
        raise ValueError("No matching demand data found.")

    # Filter supply
    supply_slice = supply_curve[supply_curve["year"] == year]
    if supply_slice.empty:
        raise ValueError("No matching supply data found.")

    # Determine maximum feasible import volume
    max_supply = supply_slice["import_demand"].sum()
    max_demand = demand_slice["import_H2_demand"].max()
    max_volume = min(max_supply, max_demand)

    # Analyse marginal supply
    marginal_supply = make_marginal_supply_curve(supply_slice)

    results = []
    cum_gap = 0.0  # € 

    v = step
    while v <= max_volume + 1e-9:
        p_sup = get_marginal_supply_price(marginal_supply, v)              # €/MWh
        p_dem = interpolate_price_from_demand_curve(demand_slice, v)       # €/MWh

        d_gap = (p_sup - p_dem) * step * 1e6
        cum_gap += d_gap

        results.append({
            "import_volume": v,
            "budget_gap": cum_gap / 1e9  # billion €
        })

        v += step

    return pd.DataFrame(results)


# Input data
year = 2050 # 2030, 2050
scenario = "config.GreenDeal" # config.GreenDeal, config.BAU
carriers = ["LH2", "NH3", "MEOH"] # LH2, NH3, MEOH
region = "EU" # "EU", "DE"

df_all = None  

for carrier in carriers:
    # Path of supply and demand curve need to be adapted
    supply_curve = pd.read_csv(f"/home/alex-charly/SSD/H2GMA/Github/AP10/analyse-h2g-a-ap10/workflow/notebooks/supply-curve-analysis/fepbe/supply_curve_{carrier}_3H_inc_fepbe.csv", index_col=0)
    demand_curve = pd.read_csv("/home/alex-charly/SSD/H2GMA/Github/AP10/analyse-h2g-a-ap10/workflow/notebooks/supply-curve-analysis/fepbe/demand_curve-fepbe-H2.csv", index_col=0)

    budget_gap = calculate_budget_gap(
        supply_curve=supply_curve,
        demand_curve=demand_curve,
        region=region,
        scenario=scenario,
        year=year,
        step=1.0
    )

    # rename budget_gap column to carrier-specific
    budget_gap = budget_gap.rename(columns={"budget_gap": f"budget_gap_{carrier}"})

    # merge into wide table
    if df_all is None:
        df_all = budget_gap
    else:
        df_all = df_all.merge(budget_gap, on="import_volume", how="outer")

# save final result
df_all.to_csv(f"results/budget_gap/fepbe/{region}_budget_gap_{scenario}_{year}.csv", index=False)
