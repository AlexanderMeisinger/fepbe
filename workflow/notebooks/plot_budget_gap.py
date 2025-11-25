# Plot budget gap of supply demand curve

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
years = [2030, 2050] # 2030, 2050
regions = ["EU"] # ["DE", "EU"]


def plot_budget_gap(region, years):
    fig, axes = plt.subplots(1, len(years), figsize=(4.5 * len(years), 4), sharey=True)
    
    if len(years) == 1:
        axes = [axes]

    for ax, year in zip(axes, years):
        # Path of budget gap needs to be adapted
        df = pd.read_csv(f"/home/alex-charly/SSD/H2GMA/Github/AP10/analyse-h2g-a-ap10/workflow/results/budget_gap/fepbe/EU_budget_gap_config.GreenDeal_2050.csv")

        if not df.empty:  
            ax.plot(
                df["import_volume"], df["budget_gap_NH3"],
                linestyle="-", linewidth=2,
                color="#2ca02c",
                label={"NH$_3$"}
            )

            ax.plot(
                df["import_volume"], df["budget_gap_MEOH"],
                linestyle="-", linewidth=2,
                color="#d62728",
                label={"MeOH"}
            )

            ax.plot(
                df["import_volume"], df["budget_gap_LH2"],
                linestyle="-", linewidth=2,
                color="orange",
                label={"LH$_2$"}
            )

        ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
        ax.set_title(f"{year}")
        ax.set_xlabel("H$_2$ Volume [TWh]")
        ax.grid(True, linestyle="--", alpha=0.5)

        
    for ax in axes:
        ax.yaxis.set_major_locator(mticker.MultipleLocator(10))

    # Adjust scope of x axis
    axes[0].set_ylabel("Budget Gap [Billion €]")
    axes[0].set_xlim(left=0, right=110)
    axes[1].set_xlim(left=0, right=650)
    axes[0].set_ylim(bottom=-10, top=30)
    axes[1].set_ylim(bottom=-10, top=30)

    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels,
               loc='lower center', bbox_to_anchor=(0.5, -0.1),
               ncol=3, frameon=False)

    #fig.suptitle(f"Budget Gap – {plots_region_labels[region]}", fontsize=14)
    fig.tight_layout(rect=[0, 0.12, 1, 0.95])

    filename = f"EU_budget_gap.png"
    plt.savefig(os.path.join("results/budget_gap/fepbe", filename), dpi=300, bbox_inches='tight')
    plt.close()


for region in regions:
    plot_budget_gap(
        region=region, 
        years=years,
)
