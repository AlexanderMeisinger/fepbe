# Analyse supply curves

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

transport_carrier = ["LH2"] # "LH2", "NH3", "MEOH"
cluster = 5
resolution = "3H"
wacc = "0.09"

# Define config settings for each country
config = {
    "Egypt": {
        2030: {"scenario": "Co2L0.80-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.24-3H", "export": [25, 50, 75]},
    },
    "Kenya": {
        2030: {"scenario": "Co2L0.05-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.00-3H", "export": [25, 50, 75]},
    },
    "Morocco": {
        2030: {"scenario": "Co2L0.83-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.27-3H", "export": [25, 50, 75]},
    },
    "Mauritania": {
        2030: {"scenario": "Co2L0.78-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.15-3H", "export": [25, 50, 75]},
    },
    "Namibia": {
        2030: {"scenario": "Co2L0.78-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.15-3H", "export": [25, 50, 75]},
    },
    "Tunisia": {
        2030: {"scenario": "Co2L0.78-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.15-3H", "export": [25, 50, 75]},
    },
    "South-Africa": {
        2030: {"scenario": "Co2L0.71-3H", "export": [5, 10, 15]},
        2050: {"scenario": "Co2L0.14-3H", "export": [25, 50, 75]},
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

                # LCOH2 for import
                price = n.buses_t.marginal_price.filter(like="destination carrier export").mean().mean()

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
supply_curve.to_csv(f"{path_notebooks}/supply_curve_{transport_carrier[0]}_3H_fepbe.csv")

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
supply_curve.to_csv(f"{path_notebooks}/supply_curve_{transport_carrier[0]}_3H_inc_fepbe.csv")
