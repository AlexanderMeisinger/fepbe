# Analyse supply and demand curves

# Import packages
import pypsa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker


# General settings
years = [2030, 2050]
prefix = "fepbe"
carrier = "H2" # Methanol, NH3, H2
path_analyse_results = f"results/s-d-curve/{prefix}-{carrier}"


# Supply curve settings (PyPSA-Earth)
transport_carrier = "NH3" # LH2, NH3, MEOH
path_curves = "notebooks/supply-curve-analysis/fepbe"
path_supply_curve = f"{path_curves}/supply_curve_{transport_carrier}_3H_inc_fepbe.csv"


# Demand curve settings (PyPSA-Eur)
# Scenario and Path Configuration
regions = ["EU"] # ["DE", "EU"]
path_demand_curve = f"{path_curves}/demand_curve-{prefix}-{carrier}.csv"

scenarios = {
    "config.GreenDeal": f"3H-imp+{carrier}",
    "config.BAU": f"3H-imp+{carrier}"
    }

plots_region_labels = {"DE": "Germany", "EU": "Europe"}

plots_scenario_labels = {
    "config.GreenDeal": "Import - Green Deal",
    "config.BAU": "Import - Business As Usual"
    }

color_map = {"config.GreenDeal": "#2ca02c", "config.BAU": "#d62728"}


# Function: Plot all demand curves (scenarios) for one region for all years
def plot_combined_supply_demand_all_years(supply_curve, demand_curve, region, years, output_path, color_map=None):
    """
    Plot and save a combined figure showing supply and demand curves across multiple years for one region.

    Parameters:
    - supply_curve: DataFrame with supply data (columns: region, year, import_demand, price)
    - demand_curve: DataFrame with demand data (columns: region, year, scenario, import_H2_demand, price)
    - region: str, name of the importing region ("DE" or "EU")
    - years: list of int, e.g., [2030, 2040, 2050]
    - output_path: str, path to folder where the output figure is saved
    """

    # Create a row of subplots: one column per year
    fig, axes = plt.subplots(1, len(years), figsize=(4.5 * len(years), 5), sharey=True)

    # Ensure axes is iterable even if only one subplot
    if len(years) == 1:
        axes = [axes]

    legend_handles = []
    legend_labels = []

    # Use a color palette from matplotlib (tab10 or Set2 for better color contrast)
    if color_map == None:
        scenario_list = sorted(demand_curve["scenario"].unique())
        color_palette = list(mcolors.TABLEAU_COLORS.values())
        if len(scenario_list) > len(color_palette):
            color_palette = plt.cm.tab20.colors
        
        color_map = dict(zip(scenario_list, color_palette[:len(scenario_list)]))

    for ax, year in zip(axes, years):
        # --- SUPPLY CURVE ---
        supply = supply_curve[supply_curve["year"] == year].sort_values("price").copy()
        supply["cumulative_export"] = supply["import_demand"].cumsum()
        supply["x_left"] = supply["cumulative_export"].shift(fill_value=0)
        supply["x_right"] = supply["cumulative_export"]

        plotted_regions = set()

        for _, row in supply.iterrows():
            label = f"{row['region']} (Export)" if row["region"] not in plotted_regions else None
            handle = ax.fill_between([row["x_left"], row["x_right"]],
                                     [row["price"], row["price"]],
                                     y2=0,
                                     step="pre",
                                     label=label,
                                     alpha=0.4,
                                     color=export_colors.get(row["region"], "gray"),
                                     edgecolor="none")
            if label:
                legend_handles.append(handle)
                legend_labels.append(label)
            plotted_regions.add(row["region"])

        # --- DEMAND CURVES ---
        demand_subset = demand_curve[(demand_curve["year"] == year) & (demand_curve["region"] == region)]

        for scenario, df in demand_subset.groupby("scenario"):
            df = df.sort_values("import_H2_demand")
            if df["import_H2_demand"].sum() > 0:
                line, = ax.plot(df["import_H2_demand"], df["price"],
                                linestyle="-", linewidth=2, marker="",
                                label=f"{plots_region_labels[region]} ({scenario})",
                                color=color_map[scenario])
                legend_handles.append(line)
                legend_labels.append(f"{plots_region_labels[region]} ({plots_scenario_labels[scenario]})")

        # Labels and layout per subplot
        ax.set_title(f"{year}")
        ax.set_xlabel("H$_2$ Volume [TWh]")
        ax.grid(True, linestyle="--", alpha=0.5)

    # Shared y-axis label
    axes[0].set_ylabel("H$_2$ cost at Europe gate [€/MWh]")
    axes[0].set_xlim(left=0, right=100)
    axes[1].set_xlim(left=0, right=578)

    # --- Shared legend below all subplots ---
    # Remove duplicates while preserving order
    seen = set()
    unique_handles_labels = []
    for h, l in zip(legend_handles, legend_labels):
        if l not in seen:
            unique_handles_labels.append((h, l))
            seen.add(l)

    unique_handles_labels = sorted(
        unique_handles_labels,
        key=lambda x: "Europe" in x[1]  # False first, True last
    )

    handles, labels = zip(*unique_handles_labels)
    fig.legend(handles, labels,
               loc='lower center',
               bbox_to_anchor=(0.5, -0.1),
               ncol=4,
               frameon=False)

    # Title and layout
    fig.suptitle(f"Supply & Demand Curves African Countries-{plots_region_labels[region]}", fontsize=14)
    fig.tight_layout(rect=[0, 0.12, 1, 0.95])  # leave room for title and legend

    # Save output file
    filename = f"{region}_s-d-curve_comb_all_years_{transport_carrier}.png"
    plt.savefig(os.path.join(output_path, filename), dpi=300, bbox_inches='tight')
    plt.close()


# Supply curve (PyPSA-Earth)
# Load supply curve
supply_curve = pd.read_csv(path_supply_curve, index_col=0) 

# Extract unique region names from the 'region' column
region_names = supply_curve["region"].unique().tolist()

# Get default matplotlib colors
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# Assign default colors to each region
export_colors = dict(zip(region_names, default_colors[:len(region_names)]))

# Demand curve (PyPSA-Eur)
# Load demand curve data
demand_curve = pd.read_csv(path_demand_curve, index_col=0)

for region in regions:
    plot_combined_supply_demand_all_years(
        supply_curve=supply_curve,
        demand_curve=demand_curve[demand_curve["scenario"].isin(scenarios.keys())],
        region=region,
        years=years,
        output_path=path_analyse_results,
        color_map=color_map
    )
