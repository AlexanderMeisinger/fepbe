# FEPBE - Financing energy partnerships beyond Europe
A case study on the way to a European-African energy transition

## Abstract
Germany and the European Union (EU) have traditionally maintained a strong economy and a high-value chain in energy-intensive industries. However, the current situation is challenging, with energy-intensive industries facing structural barriers, such as the intermittent availability of green energy, to compete with climate targets and international competitors. African countries can play a key role in addressing these challenges, but are dependent on financial support and remain under-represented in energy research. Therefore, this research investigates potential energy partnerships between Germany and African countries, with a particular focus on the H2Global auction mechanism as a financing instrument for green hydrogen exchange and its impact on the local energy transition.

The open-source tools PyPSA-Eur and PyPSA-Earth are used and further developed to analyze the transformation of sector-coupled energy systems in line with climate targets. This allows to match the German and EU hydrogen demand with green exports from African countries. The H2Global auction mechanism is analyzed by comparing merit order curves for hydrogen demand and supply while achieving a cost-effective local energy transition. The financial gap between both merit order curves shows the relevance of the H2Global mechanism for each country and identifies potential green energy partnerships. 

The results highlight the role of H2Global in structuring transparent and effective auction mechanisms, enabling long-term contracts and reducing investment and supply risks for both European off-takers (energy-intensive industries) and African producers. The findings show that a well-designed H2Global mechanism can reduce the cost of hydrogen while increasing the availability of green energy for industry. However, this research also highlights the importance of complementing such mechanisms with sustainability criteria and policy coherence to ensure local developments and global climate benefits.

## Respository structure
- `config`: contains configuration files for PyPSA-Eur (Europe) and PyPSA-Earth (African countries). These configurations are adjusted according to the year (2030 or 2050) and the scenario settings.
- `workflow/envs:` contains the environment used for PyPSA-Eur and PyPSA-Earth.
- `workflow/notebooks:` contains the Jupyter notebooks and Python files used for the evaluation of results
- `workflow/pypsa-eur:` contains the PyPSA-Eur branch used for this calculations. 
- `workflow/pypsa-earth:` contains the PyPSA-Earth branch used for this calculations.

## Run scenarios
To run both models (PyPSA-Eur and PyPSA-Earth), we recommend cloning each branch directly from the linked repository and following the installation guides for PyPSA-Eur (https://pypsa-eur.readthedocs.io/en/latest/) and PyPSA-Earth (https://pypsa-earth.readthedocs.io/en/latest/index.html). Both models run independently of each other. The environment and configs settings are available in this repository.

## License
The code in this repo is MIT licensed, see ./LICENSE.md.
