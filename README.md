# Bridging the green hydrogen gap: The role of H2Global in cross-continental hydrogen, ammonia and methanol markets
FEPBE - Financing energy partnerships beyond Europe

## Abstract
Achieving climate neutrality requires large-scale production of green hydrogen and its derivatives. A persistent cost gap between producers and offtakers, however, impedes market growth. Our study couples European-African energy markets to analyse the role of the H2Global mechanism in bridging this gap, employing sector-coupled energy models. We find that no analysed pathway is cost-competitive in 2030, with African export costs (140-229~€/MWh) exceeding European willingness to pay (40-100~€/MWh) for hydrogen, ammonia, and methanol. The required annual funding ranges between 0.6 and 11.4~billion~€. By 2050, early-stage support enables a market entry and the ramp-up of a hydrogen and Power-to-X economy: trade volumes of up to 236~TWh become cost-competitive, potentially reaching 450~TWh through reinvested savings. We conclude that, although ambitious European climate targets are the main reason for market ramp-up, the H2Global mechanism is a key and cost-effective instrument for overcoming the initial 'chicken-and-egg' problem, enabling market creation and ramp-up.

## Installation and usage

## Respository structure
- `config`: contains configuration files for PyPSA-Eur (Europe) and PyPSA-Earth (African countries). These configurations are adjusted according to the year (2030 or 2050) and the scenario settings.
- `workflow/envs:` contains the environment used for PyPSA-Eur and PyPSA-Earth.
- `workflow/notebooks:` contains the Jupyter notebooks and Python files used for the evaluation of results
- `workflow/pypsa-eur:` contains the PyPSA-Eur branch used for this calculations. 
- `workflow/pypsa-earth:` contains the PyPSA-Earth branch used for this calculations.

## Run scenarios
To run both models (PyPSA-Eur and PyPSA-Earth), we recommend cloning each branch directly from the linked repository and following the installation guides for PyPSA-Eur (https://pypsa-eur.readthedocs.io/en/latest/) and PyPSA-Earth (https://pypsa-earth.readthedocs.io/en/latest/index.html). Both models run independently of each other. The environment and configs settings are available in this repository.

## Result and input data
A dataset of the model results is available on [Zenodo](https://doi.org/10.5281/zenodo.19331304) under a CC-BY-4.0 license. Please refer to the documentation of [PyPSA-Eur](https://pypsa-eur.readthedocs.io/en/latest/) and [PyPSA-Earth](https://pypsa-earth.readthedocs.io/en/latest/index.html) for details on the input data.

## License
The code in this repo is MIT licensed, see ./LICENSE.md.
