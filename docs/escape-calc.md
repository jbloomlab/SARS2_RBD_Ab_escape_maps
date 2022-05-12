---
layout: escape-calc
permalink: /escape-calc/
---

## Overview
Calculates polyclonal antibody binding remaining after mutating one or more sites in the SARS-CoV-2 RBD.
The calculations are based on [deep mutational scanning of a large set of RBD targeting antibodies]({{ site.baseurl }}{% link index.md %}).

[This paper](https://academic.oup.com/ve/article/8/1/veac021/6549895) explains the calculator in detail.
See this [Tweet chain](https://twitter.com/jbloom_lab/status/1468001874989121542) for more explanation of the escape calculator.
[Tweet 4](https://twitter.com/jbloom_lab/status/1468001909092995073) has a little video illustrating its use.

To use the calculator, click on a site to mutate it.
The mutated site will then turn red, and the blue line will show the remaining key antigenic sites while the gray lines will show the antigenic sites in the absence of mutations.
You can use shift click to mutate multiple sites.
The bar graph shows the total antibody binding remaining after the selected mutations.
Double click the bar chart to clear mutated sites.
Mouse over points for details on sites.

Options at the bottom of the chart specify:
 
 - use data only from specific labs
 - use only antibodies elicited by specific viruses
 - use only antibodies known to neutralize Omicron
 - the strength of escape caused by mutations, see *Technical details* below
 - what site-level escape metric to use

See [here]({{ site.baseurl }}{% link index.md %}) for details on the individual antibodies.

Note that the escape calculator makes several assumptions that could affect the accuracy of the results.
See the Discussion section of [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).

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
The citation for the escape calculator is [Greaney, Starr, and Bloom, Virus Evolution (2022)](https://academic.oup.com/ve/article/8/1/veac021/6549895).

See the bottom of [this page]({{ site.baseurl }}{% link index.md %}) for a list of the citations for all the deep mutational scanning data used by the calculator.
