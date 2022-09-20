---
layout: escape-calc
permalink: /escape-calc/
---

## Overview
This page hosts the SARS-CoV-2 receptor-binding domain (RBD) escape calculator described in [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).
It calculates polyclonal antibody binding remaining after mutating one or more sites in the SARS-CoV-2 RBD.
The calculations are based on [deep mutational scanning of RBD targeting antibodies](https://www.sciencedirect.com/science/article/pii/S1931312820306247).
**Thanks to Yunlong Cao, Fanchong Jian, Sunney Xie, and coworkers for generating and sharing the deep mutational scanning data used here** (see citations at bottom of this page).

To use the calculator, click on a site to mutate it.
The mutated site will then turn red, and the blue line will show the remaining key antigenic sites while the gray lines will show the antigenic sites in the absence of mutations.
You can use shift click to mutate multiple sites.
The bar graph shows the total antibody binding remaining after the selected mutations.
Double click the bar chart to clear mutated sites.
Mouse over points for details on sites.

Drop down options at the bottom of the chart specify:
 
 - Use only antibodies elicited by specific viruses. Note that the categories are not all mutually exclusive: for instance, *SARS-CoV-2* includes infection with any SARS-CoV-2 variant as long as there was not prior SARS-CoV-2 exposure.
 - Use only antibodies known to neutralize specific variants; again the categories are not mutually exclusive.
 - Weight the antibodies by the logarithm of their IC50 (or do not weight antibodies).
 - The strength of escape caused by mutations, see *Technical details* below.

See this [Tweet chain](https://twitter.com/jbloom_lab/status/1468001874989121542) for more explanation of the escape calculator.
See [here]({{ site.baseurl }}{% link index.md %}) for details on the individual antibodies.

Note that the escape calculator makes several assumptions that could affect the accuracy of the results.
See the Discussion section of [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).
Note also that the calculator has been modified and improved several times since publication of the paper.

## Technical details
For each antibody $$a$$, let $$x_{a,r}$$ be the measurement of how much mutating site $$r$$ escapes the antibody.
The gray lines show the mean of $$x_{a,r}$$ over all antibodies; that is, they show $$\frac{\sum_a x_{a,r}}{A}$$.

Let $$\mathcal{M}$$ be the set of mutated sites.
For each antibody $$a$$ we compute the binding retained as
$$b_a\left(\mathcal{M}\right) = w_a \left(\prod\limits_{r \in \mathcal{M}} \left[\frac{\max_{r'} \left(x_{a,r'}\right) - x_{a,r}}{\max_{r'} \left(x_{a,r'}\right)}\right]\right)^s.$$
This equation means that if the RBD is mutated at a strong site of escape for an antibody $$a$$, much of the binding of that antibody is lost (if mutated at strongest site of escape, all binding is lost).
The $$s$$ variable represents how dramatically binding is lost for mutations at sites of escape that are not the strongest one: larger values means mutations even at moderate sites of escape reduce binding a lot.
The value of $$s$$ is set by the slider below the plot.

The $$w_a$$ values are the "weights" of the antibodies.
If you select the option for no weighting, then $$w_a = 1$$.
But by default, antibodies are weighted proportional to their log IC50s such that more potent antibodies have greater weight.
Specifically, the weight is calculated as $$w_a = \max\left(0, -\log \left[IC50 / 10\right] \right)$$ where $$IC50$$ is the IC50 in $$\mu$$g/ml.
This equation means that 10 $$\mu$$g/m is the lowest potency IC50 we consider neutralizing, and antibodies without known IC50s have their weight set to zero.
Using the IC50 weighting is recommended, as it avoids giving to much weight to low potency antibodies.

The blue lines show the escape at each site **after** making the mutations $$\mathcal{M}$$.
For each site $$r$$, this is $$\frac{\sum_a x_{a,r} \times b_a\left(\mathcal{M}\right)}{A}$$.

The bar chart shows the total fraction of all antibodies that still bind after the mutations, $$\frac{\sum_a b_a\left(\mathcal{M}\right)}{\sum_a w_a}$$.

[Here]({{ site.baseurl }}{% link mini-example-escape-calc.md %}) is a mini-example that helps explain the principle used by the escape calculator.

## Code and data
The code that implements the escape calculator is at [https://github.com/jbloomlab{{ site.baseurl }}](https://github.com/jbloomlab{{ site.baseurl }}).
That link also provides a Python module that can perform the calculations in batch.

The raw data used by the calculator [are here](https://raw.githubusercontent.com/jbloomlab{{ site.baseurl }}/main/processed_data/escape_calculator_data.csv).

## Citations for experimental data
The citation for this escape calculator itself is [Greaney, Starr, Bloom (2022)](https://academic.oup.com/ve/article/8/1/veac021/6549895).

The experimental data shown here are generated by yeast-display deep mutational scanning of the SARS-CoV-2 RBD (see [Greaney et al. Cell Host Microbe (2021)](https://www.sciencedirect.com/science/article/pii/S1931312820306247)).

The actual data shown here are taken from the following paper, which also aggregates additinoal data from prior studies by the same authors:

 - [Cao et al (2022)](https://www.biorxiv.org/content/10.1101/2022.09.15.507787v1)
