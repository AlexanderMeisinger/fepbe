# Analyse supply curves

# How to use
# 1) Addapt your settings at the beginning
# 2) Selection of carrier can be done with following parameters:
#    - transport_carrier_supply (LH2, NH3, MeOH)
#    - final_carrier_supply  (H2, NH3, MeOH)
# 3) Add your scenario settings (cluster, resolution, wacc, wildcard, export)
# 4) Do not forget the path_notebooks


# Import packages
import pypsa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker


# Supply curve settings (PyPSA-Earth)
base_path = "/home/alex-charly/SSD/H2GMA/Github/AP10/pypsa-earth/" # results path

transport_carrier = ["LH2"] # ["LH2", "NH3", "MEOH"]
final_carrier = ["H2"] # "[H2", "NH3", "MEOH"]
cluster = 16
resolution = "3H"
wacc = "0.09" # [0.08, 0.09, 0.1]

# Define config settings for each country
config = {
    "Egypt": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "Kenya": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "Morocco": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "Mauritania": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "Namibia": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "Tunisia": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
    "South-Africa": {
        2030: {"scenario": "Co2L1.01-3H", "export": [5, 10, 15]}, #[5, 10, 15]
        2050: {"scenario": "Co2L0.10-3H", "export": [25, 50, 75]}, #[25, 50, 75]
    },
}

# General settings
path_notebooks = "/home/alex-charly/SSD/H2GMA/Github/AP10/analyse-h2g-a-ap10/workflow/notebooks/supply-curve-analysis/fepbe/"


# Get results
supply_curve = []

for co, years_cfg in config.items():
    for yr, params in years_cfg.items():
        sc = params["scenario"]
        export_list = params["export"]

        for ca in transport_carrier:
            for ex in export_list:
                filename = (
                    f"elec_s_{cluster}_ec_lvopt_{sc}_{resolution}_{yr}"
                    f"_{wacc}_NZ_exp{ca}v{ex}.nc"
                )
                
                results_path = os.path.join(
                    base_path,
                    co,
                    "pypsa-earth",
                    "results",
                    co,
                    "postnetworks",
                    filename,
                )

                try:
                    n = pypsa.Network(results_path)
                except FileNotFoundError:
                    print(f"Missing: {results_path}")
                    continue

                # LCOH2 for export
                # Source: https://github.com/energyLS/aldehyde/blob/main/workflow/scripts/compare_integrated.py#L153
                w = n.snapshot_weightings.objective  # Series indexed by snapshots
            
                # Investments for fuel costs in €
                price_fuel = n.buses_t.marginal_price.filter(like="fuel ship export")
                flow_fuel = -n.links_t.p1.filter(like="fuel ship export")
                fuel_costs_ship_invest = (price_fuel.mul(flow_fuel, axis=0).mul(w, axis=0)).sum().sum()

                # Investments for export w/o fuel costs in €
                price_export = n.buses_t.marginal_price.filter(like="destination carrier export")
                flow_export = n.loads_t.p.filter(like="destination carrier export").sum(axis=1)
                ship_export_invest = (price_export.mul(flow_export, axis=0).mul(w, axis=0)).sum().sum()

                # Investments for export with fuel costs in €/MWh
                price = (fuel_costs_ship_invest + ship_export_invest) / (flow_export.mul(w, axis=0)).sum().sum()

                # Store the results in the same format
                supply_curve.append(
                    {
                        "region": co, 
                        "export": ca, 
                        "year": yr,
                        "import_demand": ex,
                        "price": price,
                    }
                )

# Safe results
supply_curve = pd.DataFrame(supply_curve)
supply_curve.to_csv(f"{path_notebooks}/supply_curve_{transport_carrier[0]}_{final_carrier[0]}_{wacc}_3H_fepbe.csv")

# Consider overall export amount for supply curve
# The sum of all export amounts for each country should not exceed highest export scenario
df = supply_curve.copy()

# Sort data
df = df.sort_values(["region", "year", "import_demand"])

# Calculate incremental energy quantity per country/year
# Relevant for supply-demand curve
group_cols = ["region", "year"]  
df["import_block"] = df.groupby(group_cols)["import_demand"].diff()
df["import_block"] = df["import_block"].fillna(df["import_demand"])

# Keep format of supply curve
supply_curve["import_demand"] = df["import_block"]

# Results to csv
supply_curve.to_csv(f"{path_notebooks}/supply_curve_{transport_carrier[0]}_{final_carrier[0]}_{wacc}_3H_inc_fepbe.csv")
