# Interactive maps of mutations to the SARS-CoV-2 RBD that reduce antibody binding
The citation for this repository is [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).

Most data come from [Cao et al (2022)](https://www.biorxiv.org/content/10.1101/2022.09.15.507787v1).

Briefly, the Bloom lab and the group of [Yunlong Cao, Sunney Xie, and coworkers at Peking University](https://www.biorxiv.org/content/10.1101/2021.12.07.470392v1) have used [deep mutational scanning](https://www.sciencedirect.com/science/article/pii/S1931312820306247) to map how all mutations to the SARS-CoV-2 receptor binding domain (RBD) affect binding by [antibodies](https://www.science.org/doi/10.1126/science.abf9302) or [sera](https://www.sciencedirect.com/science/article/pii/S1931312821000822).
These "escape maps" are useful for understanding the antigenic impact of viral mutations.

The escape maps for individual antibodies and sera samples have all been published across a wide variety of studies.
The goal this repository is to aggregate those data, and enable it to be easily and interactively interrogated.

Specifically, this repository hosts the code for two ways to interact with the data:

 - The data are used to generate an "escape calculator" that visualizes the impact of combinations of mutations at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/).
    The escape-calculator is described in detail in [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).

 - Some data can be visualized and individual escape maps queried using the interactive plots at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps). **This visualization is no longer being updated with new data.**

 - The processed data used by the escape calculator are [here](processed_data/escape_calculator_data.csv).
 
 - More complete raw data are:
 
  - Current data used by escape calculator at [mutation-level](processed_data/escape_data_mutation.csv) and [site-level](processed_data/escape_data_site.csv).
 
  -  Old file with data displayed at level of individual maps [here](processed_data/escape_data.csv). **This file is no longer being updated with new data.**
  
Note in the above files, an IC50 of 10 should be taken as corresponding to non-neutralizing.

## Command-line escape calculator for batch calculations
If you are performing batch analyses of SARS-CoV-2 variants or mutations, you may want to calculate the extent of escape as implemented in the "escape calculator" at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/) in batch.
You can do this by downloading the Python module [bindingcalculator.py](bindingcalculator.py), which provides a Python interface that implements the escape calculator.
[Here is the documentation](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/bindingcalculator) for that module (built with [pdoc](https://pdoc.dev/docs/pdoc.html)) with `pdoc bindingcalculator.py -o docs/_layouts/`.

## **New** method of building escape calculator
Note that as of Sept-19-2022, we have changed how we get data for the escape calculator.
Now all those data come from [Cao et al (2022)](https://www.biorxiv.org/content/10.1101/2022.09.15.507787v1) and we no longer update the antibody-specific visualizations.
There are two reasons: first, the data was now too large to display in the old non-calculator format, and second we just want data from that single study.

To build the calculator, first build the `conda` environment in [environment.yml](environment.yml).
Then activate that `conda` environment with:

    conda activate SARS2_RBD_Ab_escape_maps

Next open the Jupyter notebooks [plot_calculator.ipynb](plot_calculator.ipynb) and run it.
It creates an interactive [Altair](https://altair-viz.github.io/) chart:

  - [docs/_includes/escape_calc_chart.html](docs/_includes/escape_calc_chart.html)

The interactive chart will be rendered via [GitHub pages](https://pages.github.com/).
Specifically, when updates are pushed to the `main` branch of the repo on GitHub, it will be rendered at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc).
See [docs/README.md](docs/README.md) for more information on how the webpage is served via [GitHub Pages](https://pages.github.com/)
The notebook also creates the following file, which has the input data for the escape calculator:

  - [processed_data/escape_calculator_data.csv](processed_data/escape_calculator_data.csv)
  
Less processed forms of the same data (not collapsed at site level or only for neutralizing antibodies) are here: [mutation-level](processed_data/escape_data_mutation.csv) and [site-level](processed_data/escape_data_site.csv)

## **Obsolete** method of adding data to these maps
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

Finally, open the Jupyter notebooks [plot_calculator.ipynb](plot_calculator.ipynb) and [plot_escape_maps.ipynb](plot_escape_maps.ipynb) and run them.
They create two interactive [Altair](https://altair-viz.github.io/) charts:

  - [docs/_includes/chart.html](docs/_includes/chart.html)
  - [docs/_includes/escape_calc_chart.html](docs/_includes/escape_calc_chart.html)

The interactive charts will be rendered via [GitHub pages](https://pages.github.com/).
Specifically, when updates are pushed to the `main` branch of the repo on GitHub, they will be rendered at [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc)
and [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps).
See [docs/README.md](docs/README.md) for more information on how the webpage is served via [GitHub Pages](https://pages.github.com/)

The [plot_escape_maps.ipynb](plot_escape_maps.ipynb) notebook also creates the following file, which has the input data for the escape calculator:

  - [processed_data/escape_calculator_data.csv](processed_data/escape_calculator_data.csv)
