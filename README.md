# FEPBE - Financing energy partnerships beyond Europe

This repository contains the entire scientific project for the paper "Bridging the green hydrogen gap: The role of H2Global in cross-continental hydrogen, ammonia and methanol markets".

## Abstract
Achieving climate neutrality requires large-scale production of green hydrogen and its derivatives. A persistent cost gap between producers and offtakers, however, impedes market growth. Our study couples European-African energy markets to analyse the role of the H2Global mechanism in bridging this gap, employing sector-coupled energy models. We find that no analysed pathway is cost-competitive in 2030, with African export costs (140-229 €/MWh) exceeding European willingness to pay (40-100 €/MWh) for hydrogen, ammonia, and methanol. The required annual funding ranges between 0.6 and 11.4 billion €. By 2050, early-stage support enables a market entry and the ramp-up of a hydrogen and Power-to-X economy: trade volumes of up to 236 TWh become cost-competitive, potentially reaching 450 TWh through reinvested savings. We conclude that, although ambitious European climate targets are the main reason for market ramp-up, the H2Global mechanism is a key and cost-effective instrument for overcoming the initial 'chicken-and-egg' problem, enabling market creation and ramp-up.

## Respository structure
- `config`: contains configuration files for PyPSA-Eur (Europe) and PyPSA-Earth (African countries). These configurations are adjusted according to the year (2030 or 2050) and the scenario settings.
- `workflow/envs:` contains the environment used for PyPSA-Eur and PyPSA-Earth.
- `workflow/notebooks:` contains the Jupyter notebooks and Python files used for the evaluation of results
- `workflow/pypsa-eur:` contains the PyPSA-Eur branch used for this calculations. 
- `workflow/pypsa-earth:` contains the PyPSA-Earth branch used for this calculations.

## Installation and usage
1. Open your terminal at a location where you want to install the repository fepbe including it's subworkflows PyPSA-Eur and PyPSA-Earth. Type the following in your terminal to download the packages and the dependencies (pypsa-eur, pypsa-earth) from GitHub. Note that the tag `--recursive-submodules` is needed to automatically clone also the pypsa-eur and pypsa-earth dependencies.
   
   ```bash
   git clone --recurse-submodules https://github.com/AlexanderMeisinger/fepbe.git
   ```
   
3. Move the current directory to the head of the repository.
   
   ```bash
   .../some/path/without/spaces % cd fepbe
   ```
   
3. The PyPSA-Eur python package requirements are curated in the `workflow/pypsa-eur/envs/environment.yaml` file of the PyPSA-Eur repository. The environment can be installed using conda or mamba:
   
   ```bash
   .../fepbe % conda env create -f workflow/pypsa-eur/envs/environment.yaml
   ```
   
5. The PyPSA-Earth python package requirements are curated in the `workflow/pypsa-earth/envs/environment.yaml` of the PyPSA-Earth respository. The environment can be installed using conda or mamba:
   
   ```bash
   .../fepbe % conda env create -f workflow/pypsa-earth/envs/environment.yaml
   ```
   
7. For running the optimisation one has to install the solver. We can recommend the open source `HiGHs` solver, see more details on solvers in the documentation of PyPSA-Eur and PyPSA-Earth. The optimisation in this work was performed using the commercial `Gurobi` solver.

## Run scenarios
For starting the PyPSA-Eur model, run the following command:
```bash
.../fepbe/workflow/pypsa-eur % conda activate pypsa-eur
```
```bash
% snakemake --cores all --configfile .../fepbe/config/pypsa-eur/scenario-name.yaml
```

For starting the PyPSA-Earth model, run the following command:
```bash
.../fepbe/workflow/pypsa-earth % conda activate pypsa-earth
```
```bash
% snakemake --cores all solve_sector_networks --configfile .../fepbe/config/pypsa-earth/scenario-name.yaml
```

Please follow the documentation of [PyPSA-Eur](https://pypsa-eur.readthedocs.io/en/latest/) and [PyPSA-Earth](https://pypsa-earth.readthedocs.io/en/latest/index.html) for more details. The estimated time to run one single optimisation is 120 mins on a standard laptop, the full set of paper results includes over 750 optimisations. To run the full set, a high-performance computer is recommended. Both models run independently of each other.

## Result and input data
A dataset of the model results is available on [Zenodo](https://doi.org/10.5281/zenodo.19331304) under a CC-BY-4.0 license. Please refer to the documentation of [PyPSA-Eur](https://pypsa-eur.readthedocs.io/en/latest/) and [PyPSA-Earth](https://pypsa-earth.readthedocs.io/en/latest/index.html) for details on the input data.

## License
The code in this repo is MIT licensed, see ./LICENSE.md.
