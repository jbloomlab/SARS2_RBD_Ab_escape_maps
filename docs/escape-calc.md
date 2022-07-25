---
layout: escape-calc
permalink: /escape-calc/
---

## Overview
This page hosts the SARS-CoV-2 receptor-binding domain (RBD) escape calculator described in [this paper](https://academic.oup.com/ve/article/8/1/veac021/6549895).
It calculates polyclonal antibody binding remaining after mutating one or more sites in the SARS-CoV-2 RBD.
The calculations are based on [deep mutational scanning of a large set of RBD targeting antibodies](https://www.sciencedirect.com/science/article/pii/S1931312820306247).

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
This equation meeans that 10 $$\mu$$g/m is the lowest potency IC50 we consider neutralizing, and antibodies without known IC50s have their weight set to zero.
Using the IC50 weighting is recommended, as it avoids giving to much weight to low potency antibodies.

The blue lines show the escape at each site **after** making the mutations $$\mathcal{M}$$.
For each site $$r$$, this is $$\frac{\sum_a x_{a,r} \times b_a\left(\mathcal{M}\right)}{A}$$.

The bar chart shows the total fraction of all antibodies that still bind after the mutations, $$\frac{\sum_a b_a\left(\mathcal{M}\right)}{\sum_a w_a}$$.

[Here]({{ site.baseurl }}{% link mini-example-escape-calc.md %}) is a mini-example that helps explain the principle used by the escape calculator.

## Code and data
The code that implements the escape calculator is at [https://github.com/jbloomlab{{ site.baseurl }}](https://github.com/jbloomlab{{ site.baseurl }}).
That link also provides a Python module that can perform the calculations in batch.

The raw data used by the calculator [are here](https://raw.githubusercontent.com/jbloomlab{{ site.baseurl }}/main/processed_data/escape_calculator_data.csv).

## Citations for experimental dataa
The citation for this escape calculator itself is [Greaney, Starr, Bloom (2022)](https://academic.oup.com/ve/article/8/1/veac021/6549895).

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
  - [Cao et al. Nature (2022a)](https://www.nature.com/articles/s41586-022-04980-y)
  - [Cao et al. Nature (2022b)](https://www.nature.com/articles/s41586-021-04385-3)
  - [Greaney et al. PLoS Path (2022)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1010248)
