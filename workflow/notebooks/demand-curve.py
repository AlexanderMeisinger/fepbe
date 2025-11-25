# Analyse demand curves

# Import packages
import pypsa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker


# Demand curve settings (PyPSA-Eur)
carrier = "H2" # Methanol, NH3, H2

scenarios = {
    "config.GreenDeal": f"3H-imp+{carrier}",
    "config.BAU": f"3H-imp+{carrier}"
    }

years = [2030, 2050]
prices = np.arange(0, 201, 10)
cluster = 39
regions = ["DE", "EU"] #"DE", "EU"

plots_region_labels = {
    "DE": "Germany",
    "EU": "Europe"
}

prefix = "fepbe"

path_analyse_results = f"workflow/results/s-d-curve/{prefix}-{carrier}"

# General settings
path_notebooks = "/home/alex-charly/SSD/H2GMA/Github/AP10/analyse-h2g-a-ap10/workflow/notebooks/supply-curve-analysis/fepbe/"

# Function: Extract import demand and price from PyPSA network
def import_demand(pypsa_path, regions, price, year, scenario, carrier):
    """
    Extract import demand and price for selected regions from a PyPSA-Eur network.

    Parameters:
    - pypsa_path: path to the .nc network file
    - regions: list of region names (e.g., ["DE", "EU"])
    - price: price applied in the run
    - year: target year
    - scenario: scenario key (e.g., "config.main")
    - carrier: export carrier

    Returns:
    - DataFrame with import carrier demand per region
    """
    import_demand_carrier = pd.DataFrame()
    n = pypsa.Network(pypsa_path)
    
    for region in regions:
        if region == "EU":
            df_import_carrier = n.statistics.energy_balance()
            idx = pd.IndexSlice
            try:
                if carrier == "H2":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"Hydrogen Storage"]].div(1e6).Generator["import H2"]
                elif carrier == "NH3":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"NH3"]].div(1e6).Generator["import NH3"]
                elif carrier == "Methanol":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"methanol"]].div(1e6).Link["import methanol"]
            except:
                df_import_carrier = 0  
        else:
            df_import_carrier = n.statistics.energy_balance(groupby=["carrier", "bus_carrier", "country"])
            idx = pd.IndexSlice
            try:
                if carrier == "H2":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"Hydrogen Storage",region]].div(1e6).Generator["import H2"]
                elif carrier == "NH3":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"NH3",region]].div(1e6).Generator["import NH3"]
                elif carrier == "Methanol":
                    df_import_carrier = df_import_carrier.loc[idx[:,:,"methanol",region]].div(1e6).Link["import methanol"]
            except:
                df_import_carrier = 0

        # Store extracted values in consistent format  
        df_import_carrier = pd.DataFrame({"region": region, "year": [year], "scenario": [scenario], "price": [price], "import_demand": [df_import_carrier]})
        import_demand_carrier = pd.concat([import_demand_carrier, df_import_carrier], ignore_index=True)

    return import_demand_carrier


# Build demand curve dataFrame
demand_curve = pd.DataFrame()

for scenario in scenarios:
    for year in years:
        for price in prices:
            path = f"/mnt/c/Users/mea39219/Downloads/pypsa-eur/{scenario}/base_s_{cluster}__{scenarios[scenario]}+{price}_{year}.nc"

            # Get import demand in relation to import price
            import_demand_carrier = import_demand(
                pypsa_path=path, 
                regions=regions, 
                price=price, 
                year=year, 
                scenario=scenario,
                carrier=carrier)
            
            # Store demand caurve data
            demand_curve = pd.concat([demand_curve, import_demand_carrier], ignore_index=True)

# Create csv file with demand curve data
demand_curve.to_csv(f"{path_notebooks}/demand_curve-{prefix}-{carrier}.csv")







