# Interactive maps of mutations to the SARS-CoV-2 RBD that reduce antibody binding
The Bloom lab has used [deep mutational scanning](https://www.sciencedirect.com/science/article/pii/S1931312820306247) to map how all mutations to the SARS-CoV-2 receptor binding domain (RBD) affect binding by [antibodies](https://www.science.org/doi/10.1126/science.abf9302) or [sera](https://www.sciencedirect.com/science/article/pii/S1931312821000822).
These "escape maps" are useful for understanding the antigenic impact of viral mutations.

The escape maps for individual antibodies and sera samples have all been published across a wide variety of studies.
The goal this repository is to aggregate those data, and enable it to be easily and interactively interrogated.

Specifically, this repository hosts the code for two ways to interact with the data:

  - The full data can be visualized and individual escape maps queried using the interactive plots at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps).

  - The data are used to generate an "escape calculator" that visualizes the impact of combinations of mutations at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/).

  - The raw escape data for all antibodies and sera are [here](processed_data/escape_data.csv).

  - The data used by the escape calculator are [here](processed_data/escape_calculator_data.csv).

## Command-line escape calculator
If you are performing batch analyses of SARS-CoV-2 variants or mutations, you may want to calculate the extent of escape as implemented in the "escape calculator" at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/) in batch.
You can do this by downloading the Python module [bindingcalculator.py](bindingcalculator.py), which provides a Python interface that implements the escape calculator.
How to use the [bindingcalculator.py](bindingcalculator.py) module is documented within the module.

## Adding data to these maps
The input data on how mutations affect antibody binding or neutralization are in [./data/](data), and is collated from Bloom lab deep mutational scanning experiments.
See [./data/README.md](data/README.md) for details on how to add new data.

To process the data to build the interactive visualizations, first build the `conda` environment in [environment.yml](environment.yml).
Then activate that `conda` environment with:

    conda activate SARS2_RBD_Ab_escape_maps

Next, process the raw data by running [process_data.py](process_data.py):

    python process_data.py

This command will process the input data in [./data/](data) to create the processed data in [./processed_data/](processed_data).
Specifically, the processed data includes the following two files:

 - [processed_data/escape_data.csv](processed_data/escape_data.csv) contains the raw escape data for all antibodies / sera.
 - [processed_data/studies.csv](processed_data/studies.csv) contains information on the studies.

The [process_data.py](process_data.py) script also adds information about citations to the bottom of [docs/index.md](docs/index.md) for rendering on the webpage.

Finally, open the Jupyter notebook [plot_data.ipynb](plot_data.ipynb) using `jupyterlab` and run it.
This creates three interactive [Altair](https://altair-viz.github.io/) charts:

  - [docs/_includes/chart.html](docs/_includes/chart.html)
  - [docs/_includes/escape_calc_chart.html](docs/_includes/escape_calc_chart.html)
  - [docs/_includes/mini_example_escape_calc.html](docs/_includes/mini_example_escape_calc_chart.html)

The interactive charts will be rendered via [GitHub pages](https://pages.github.com/).
Specifically, when updates are pushed to the `main` branch of the repo on GitHub, they will be rendered at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps).
See [docs/README.md](docs/README.md) for more information on how the webpage is served via [GitHub Pages](https://pages.github.com/)

The [plot_data.ipynb](plot_data.ipynb) notebook also creates the following file:

  - [processed_data/escape_calculator_data.csv](processed_data/escape_calculator_data.csv)
