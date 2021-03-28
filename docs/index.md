---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

## Overview
This page allows you to look up how mutations to the SARS-CoV-2 receptor binding domain (RBD) affect escape from monoclonal antibodies or polyclonal sera.
It does this by integrating multiple studies by the [Bloom lab](https://research.fredhutch.org/bloom/en.html) that use [deep mutational scanning to completely map how all mutations to the RBD affect antibody or sera binding](https://www.sciencedirect.com/science/article/pii/S1931312820306247).

Specifically, the data shown here are from experiments that [quantify the effect on antibody / sera binding of all RBD mutations](https://www.sciencedirect.com/science/article/pii/S1931312820306247) that are tolerated for protein folding and ACE2-binding
(For how mutations affect RBD folding and ACE2-binding, see this [interactive visualization](https://jbloomlab.github.io/SARS-CoV-2-RBD_DMS/) of the experimental measurements described [here](https://www.sciencedirect.com/science/article/pii/S0092867420310035).)
These mutation-level escape measurements are used to define two site-level escape metrics: the sum of the effects of all mutations at a site, or the mean effect of all tolerated mutations at a site (use the selection box at the bottom of the plots to choose the escape metric).

The multidimensional scaling plot at the upper left arranges antibodies and sera in the "space of escape" such that ones with similar escape mutations are positioned close to each other (see [here](https://www.sciencedirect.com/science/article/pii/S1931312820306247) for methodological details).
Hover over a point to see what antibody / serum it corresponds to, and click to select it in other plots too.
Use shift-click to make multiple selections, and double-click to clear them.
Multidimensional scaling involves a random seed; use the selection box at the bottom of the plot to choose different seeds for slightly different layouts.
You can choose which types of antibodies or sera to display via the small box to the right of the multidimensional scaling plot: for instance, you can show just antibodies, just sera, subsets of these, or all of them.

The upper of the two line plots shows thin lines giving the escape metric at each site for all antibodies / sera of the types that are currently chosen for display.
Click on a line to bold it and highlight that antibody / serum in the other plots.
You can use the zoom bar to get a closer look at specific sites of interest.

The lower of the two line plots shows the **mean** escape at each site for all antibodies / sera you have selected by clicking, or over all antibodies / sera of the type(s) that are displayed in the multidimensional scaling plot (choose which of these it shows via the selection box immediately below this line plot).
These averages are useful to get a general sense of sites that have effects over entire sets of antibodies or sera.

In the upper-right of the plot, you can select antibodies / sera by name by clicking on the boxes by their names (use the zoom bar to find names that are cut off below the plot).
You can also shift-click the hyperlinks next to the names to open the citation that reports the experimental data, or get a detailed [dms-view](https://dms-view.github.io/docs/) of the data projected onto a [crystal structure of the RBD bound to ACE2](https://www.rcsb.org/structure/6M0J).

[Follow us on Twitter](https://twitter.com/jbloom_lab) if you want to get updates when more data are added.

## Raw data and code
The experimental data plotted here is available in [this CSV file](https://raw.githubusercontent.com/jbloomlab/SARS2_RBD_Ab_escape_maps/main/processed_data/escape_data.csv).

The computer code that generates the interactive plot and this rest of this website from that raw data is at [https://github.com/jbloomlab/SARS2_RBD_Ab_escape_maps](https://github.com/jbloomlab/SARS2_RBD_Ab_escape_maps).

## Citations
The experimental data shown here are taken from the following papers:
  - [Dong et al. bioRxiv (2021)](https://www.biorxiv.org/content/10.1101/2021.01.27.428529v1)
  - [Greaney et al. Cell Host Microbe (2021a)](https://www.sciencedirect.com/science/article/pii/S1931312820306247)
  - [Greaney et al. Cell Host Microbe (2021b)](https://www.sciencedirect.com/science/article/pii/S1931312821000822)
  - [Greaney et al. bioRxiv (2021)](https://www.biorxiv.org/content/10.1101/2021.03.17.435863v1)
  - [Starr et al. Science (2021)](https://science.sciencemag.org/content/early/2021/01/22/science.abf9302)
  - [Starr et al. bioRxiv (2021)](https://www.biorxiv.org/content/10.1101/2021.02.17.431683v1)
