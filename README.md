# Bridging the green hydrogen gap: The role of H2Global in cross-continental hydrogen, ammonia and methanol markets
FEPBE - Financing energy partnerships beyond Europe

## Abstract
The transition to a climate-neutral Europe requires large-scale production of green hydrogen and its derivatives, with imports from African countries offering a promising option. However, a significant cost gap between African production and European offtakers remains the major barrier. For the first time, both markets are coupled using the energy models PyPSA-Eur and PyPSA-Earth to analyse the role of the H2Global mechanism in bridging this gap. Results of both merit-order curves show that in 2030, none of the analysed pathways are cost-competitive, with African export costs (140-229~€/MWh) significantly exceeding European willingness to pay (40-100~€/MWh) for hydrogen, ammonia and methanol. The required annual funding ranges between 0.6 and 11.4 billion €. By 2050 and under European Green Deal conditions, early-stage support enables a market entry and the ramp-up of a hydrogen and Power-to-X economy: trade volumes of up to 236~TWh become cost-competitive, potentially reaching 450~TWh through reinvested savings. While liquid hydrogen shipping becomes the least-cost option for direct hydrogen use, ammonia and methanol offer higher domestic infrastructure synergies. We conclude that, although ambitious European climate targets are the main reason for market ramp-up, the H2Global mechanism is a key and cost-effective instrument for overcoming the initial 'chicken-and-egg' problem of cross-continental energy partnerships, enabling market creation and ramp-up.

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
