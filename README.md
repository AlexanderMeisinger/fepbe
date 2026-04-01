# FEPBE - Financing energy partnerships beyond Europe
A case study on the way to a European-African energy transition

## Abstract
Energy-intensive industries form the backbone of the European economy. Long-term competitiveness depends on access to cost effective low-carbon energy in order to meet the requirements of the European Green Deal. African countries can play a key role in addressing these challenges, but are dependent on financial support and remain under-represented in energy research. Therefore, this research investigates potential energy partnerships between European and African countries, with a particular focus on the H2Global auction mechanism as a financing instrument. The open-source tools PyPSA-Eur and PyPSA-Earth are applied and extended to analyze the impact of import costs and export volumes on sector-coupled energy systems in 2030 and 2050. This enables the development of supply-demand curves by linking European willingness to pay with African export costs for hydrogen, ammonia, and methanol. The financial gap between both merit-order curves shows the impact of the H2Global mechanism. The
results highlight the role of the H2Global mechanism in bridging the cost gap between European demand and African supply in 2030, thereby enabling market entry for hydrogen-based carriers on both sides. On the import side, close alignment with climate targets reduces the need for financial support. On the export side, liquid hydrogen shipping becomes the least-cost option compared to ammonia and methanol. By 2050, declining costs and growing market volumes for hydrogen-based carriers enable cost-competitive European-African energy markets across multiple transport and end-use pathways.

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
