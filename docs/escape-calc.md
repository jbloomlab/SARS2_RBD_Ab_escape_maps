---
layout: escape-calc
permalink: /escape-calc/
---

## Overview
Calculates polyclonal antibody binding remaining after mutating one or more sites in the SARS-CoV-2 RBD.
The calculations are based on [deep mutational scanning of a large set of RBD targeting antibodies]({{ site.baseurl }}{% link index.md %}).

See this [Tweet chain](https://twitter.com/jbloom_lab/status/1468001874989121542) for an explanation of the escape calculator.
[Tweet 4](https://twitter.com/jbloom_lab/status/1468001909092995073) has a little video illustrating its use.
[This pre-print](https://doi.org/10.1101/2021.12.04.471236) explains the calculator in detail.

We assume a polyclonal antibody mix of all SARS-CoV-2 antibodies with deep mutational scanning data.
Initially, the line chart shows the average escape at each site across all these antibodies.
If you click a site, antibodies escaped by mutations at that site are subtracted from the resulting blue escape map.
The bar chart shows the fraction total binding retained after the mutation.
You use shift-click to mutate multiple sites.
Double-click the bar chart to clear mutated sites.
Mouseover points to see details.

Options at the bottom of the chart specify:
 
 - use data only from specific labs
 - use only antibodies elicited by specific viruses
 - use only antibodies known to neutralize Omicron
 - the strength of escape caused by mutations, see *Technical details* below
 - what site-level escape metric to use

See [here]({{ site.baseurl }}{% link index.md %}) for details on the individual antibodies.

Note that the escape calculator makes several assumptions that could affect the accuracy of the results.
See the Discussion section of [this pre-print](https://doi.org/10.1101/2021.12.04.471236).

## Technical details
For each antibody $$a$$, let $$x_{a,r}$$ be the measurement of how much mutating site $$r$$ escapes the antibody.
The gray lines show the mean of $$x_{a,r}$$ over all antibodies; that is, they show $$\frac{\sum_a x_{a,r}}{A}$$.

Let $$\mathcal{M}$$ be the set of mutated sites.
For each antibody $$a$$ we compute the binding retained as
$$b_a\left(\mathcal{M}\right) = \left(\prod\limits_{r \in \mathcal{M}} \left[\frac{\max_{r'} \left(x_{a,r'}\right) - x_{a,r}}{\max_{r'} \left(x_{a,r'}\right)}\right]\right)^s.$$
This equation means that if the RBD is mutated at a strong site of escape for an antibody $$a$$, much of the binding of that antibody is lost (if mutated at strongest site of escape, all binding is lost).
The $$s$$ variable represents how dramatically binding is lost for mutations at sites of escape that are not the strongest one: larger values means mutations even at moderate sites of escape reduce binding a lot.
The value of $$s$$ is set by the slider below the plot.

The blue lines show the escape at each site **after** making the mutations $$\mathcal{M}$$.
For each site $$r$$, this is $$\frac{\sum_a x_{a,r} \times b_a\left(\mathcal{M}\right)}{A}$$.

The bar chart shows the total fraction of all antibodies that still bind after the mutations, $$\frac{\sum_a b_a\left(\mathcal{M}\right)}{A}$$.

[Here]({{ site.baseurl }}{% link mini-example-escape-calc.md %}) is a mini-example that helps explain the principle used by the escape calculator.

## Code and data
The code that implements the escape calculator is at [https://github.com/jbloomlab{{ site.baseurl }}](https://github.com/jbloomlab{{ site.baseurl }}).
That link also provides a Python module that can perform the calculations in batch.

The raw data used by the calculator [are here](https://raw.githubusercontent.com/jbloomlab{{ site.baseurl }}/main/processed_data/escape_calculator_data.csv).

## Citations
The citation for the escape calculator is [Greaney, Starr, and Bloom, bioRxiv (2021)](https://doi.org/10.1101/2021.12.04.471236).

The citations for the deep mutational scanning data used by the calculator are:
  - [Cao et al. bioRxiv (2021)](https://www.biorxiv.org/content/10.1101/2021.12.07.470392v1.full)
  - [Dong et al. Nat Micro (2021)](https://www.nature.com/articles/s41564-021-00972-2)
  - [Greaney et al. Cell Host Microbe (2021a)](https://www.sciencedirect.com/science/article/pii/S1931312820306247)
  - [Greaney et al. Cell Host Microbe (2021b)](https://www.sciencedirect.com/science/article/pii/S1931312821000822)
  - [Greaney et al. NA (2021)](https://github.com/jbloomlab/SARS-CoV-2-RBD_MAP_COV2-2955)
  - [Greaney et al. Nat Comm (2021)](https://www.nature.com/articles/s41467-021-24435-8)
  - [Greaney et al. Sci Transl Med (2021)](https://stm.sciencemag.org/content/13/600/eabi9915)
  - [Greaney et al. bioRxiv (2021)](https://www.biorxiv.org/content/10.1101/2021.10.12.464114v1)
  - [Starr et al. Cell Reports Medicine (2021)](https://doi.org/10.1016/j.xcrm.2021.100255)
  - [Starr et al. Nature (2021)](https://www.nature.com/articles/s41586-021-03807-6)
  - [Starr et al. Science (2021)](https://science.sciencemag.org/content/early/2021/01/22/science.abf9302)
  - [Tortorici et al. Nature (2021)](https://www.nature.com/articles/s41586-021-03817-4)
