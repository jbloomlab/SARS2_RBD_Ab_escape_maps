---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

## Overview
This page allows you to interactively analyze how mutations to the SARS-CoV-2 receptor binding domain (RBD) affect escape from monoclonal antibodies or polyclonal sera.
It does this by integrating multiple experimental studies by the [Bloom lab](https://research.fredhutch.org/bloom/en.html) and [Y Cao, XS Xie and coworkers at Peking University](https://icg.pku.edu.cn/en/research/faculty/269364.htm) that use [deep mutational scanning](https://www.sciencedirect.com/science/article/pii/S1931312820306247) to map how all mutations to the RBD affect antibody or sera binding.
The citations for the data shown here are listed at the bottom of this page.

The upper line plot shows the per-site escape for each individual antibody, and you can zoom and click on specific lines for details.
The lower line plot shows the mean escape at each site across all displayed antibodies, or those that you have currently selected by clicking (choose which option by clicking buttons below plot).

Antibodies are classfied using the [Barnes et al scheme](https://www.nature.com/articles/s41586-020-2852-1), and displayed in a multidimensional scaling plot using the approach described [here](https://www.sciencedirect.com/science/article/pii/S1931312820306247).
There is also a selection box on the right that lists individual antibodies.
All these plots are interactive so you can select by clicking, make multiple selections by shift-clicking, and clear selections by double clicking.

At the bottom of the plot are options about what to display, including:

 - show data only from specific labs
 - show only antibodies elicited by specific viruses
 - show only antibodies known to neutralize Omicron
 - use a site-level escape metric of the total or mean effects of all mutations at a site

The escape metrics are normalized for each antibody so a value of one corresponds to the larger of the maximal escape at any site or 20 times the median escape across all sites.

For the antibody list at top right, you can shift-click the hyperlinks next to the names to open the citation or get a [dms-view](https://dms-view.github.io/docs/) of escape projected onto a [crystal structure](https://www.rcsb.org/structure/6M0J) of the RBD bound to ACE2.

[Follow us on Twitter](https://twitter.com/jbloom_lab) to get updates when more data are added.

## Escape calculator
[Click here]({{ site.baseurl }}{% link escape-calc.md %}) for an [escape calculator](https://doi.org/10.1101/2021.12.04.471236) that aggregates these data to estimate the antigenic effect on polyclonal sera of mutating combinations of RBD sites.

## Raw data and code
The experimental data plotted here are in [this CSV file](https://github.com/jbloomlab{{ site.baseurl }}/blob/main/processed_data/escape_data.csv?raw=true).

The computer code that generates this plot and website is at [https://github.com/jbloomlab/{{ site.baseurl }}](https://github.com/jbloomlab/{{ site.baseurl }}).

## Citations
The experimental data shown here are taken from the following papers:
  - [Dong et al. Nat Micro (2021)](https://www.nature.com/articles/s41564-021-00972-2)
  - [Greaney et al. Cell Host Microbe (2021a)](https://www.sciencedirect.com/science/article/pii/S1931312820306247)
  - [Greaney et al. Cell Host Microbe (2021b)](https://www.sciencedirect.com/science/article/pii/S1931312821000822)
  - [Greaney et al. NA (2021)](https://github.com/jbloomlab/SARS-CoV-2-RBD_MAP_COV2-2955)
  - [Greaney et al. Nat Comm (2021)](https://www.nature.com/articles/s41467-021-24435-8)
  - [Greaney et al. Sci Transl Med (2021)](https://stm.sciencemag.org/content/13/600/eabi9915)
  - [Starr et al. Cell Reports Medicine (2021)](https://doi.org/10.1016/j.xcrm.2021.100255)
  - [Starr et al. Nature (2021)](https://www.nature.com/articles/s41586-021-03807-6)
  - [Starr et al. Science (2021)](https://science.sciencemag.org/content/early/2021/01/22/science.abf9302)
  - [Tortorici et al. Nature (2021)](https://www.nature.com/articles/s41586-021-03817-4)
  - [Cao et al. Nature (2022)](https://www.nature.com/articles/s41586-021-04385-3)
  - [Greaney et al. PLoS Path (2022)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1010248)
