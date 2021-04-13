---
layout: escape_calc
permalink: /escape_calc/
---

## Overview
This page calculates the total polyclonal antibody binding remaining and sites of escape after making one or more RBD mutations.

We assume a polyclonal antibody mix containing all SARS-CoV-2 monoclonal antibodies for which we have measured escape maps.
Initially, the chart shows the average escape at each site taken across all these antibodies.
If you click on a site, that site is then mutated, and antibodies escaped by mutations at that site are subtracted from the blue escape map (the gray line continues to show the escape map if all antibodies are binding).
Therefore, the blue lines show the sites at which mutations will have the biggest effect on the residual antibody binding after mutating other sites.
You can repeat this process for additional sites (use shift-click to mutate additional sites).
You can double-click to clear mutated sites.

The options at the bottom specify whether to use the escape values with or without normalization across experiments, to use the total escape at each site summed across all mutations or the mean among tolerated mutations, and how "strongly" mutating a site eliminates binding by antibodies targeting that site.

## Assumptions
The escape calculations done here make sense under two biological assumptions, neither of which are expected to be fully true:
 1. The monoclonal antibodies for which we have measured escape maps for provide a representative sampling of the antibodies that actual contribute to biological activity against the RBD in polyclonal sera.
 2. The RBD sequence against which mutations are being called is the same RBD sequence that elicited the immunity.

## Technical details
For each antibody $a$, we have a measurement $x_{a,r}$ of how much mutating site $r$ escapes binding by antibody $a$, where $1 \le a \le A$ (there are $A$ antibodies).
The gray lines in the plot simply show the mean of $x_{a,r}$ over all antibodies $a$ at each site; that is, for each site $r$ they show $\frac{\sum_a x_{a,r}}{A}$.

Let $\mathcal{M}$ be the set of sites that are mutated.
Then for each antibody $a$ we compute the binding retained as $b_a\left(\mathcal{M}\right) = \left(\prod\limits_{r \in \mathcal{M}} \left[\frac{\max_r \left(x_{a,r}\right) - x_{a,r}}{\max_r \left(x_{a,r}\right)}\right]\right)^s$.
Essentially, this equation means that if the RBD is mutated at a strong site of escape for an antibody $a$, much of the binding of that antibody is lost (if mutated at strongest site of escape, all binding is lost).
The $s$ variable represents how dramatically binding is lost for mutations at sites of escape that are not the strongest one: larger values means mutations even at moderate sites of escape reduce binding a lot.
The value of $s$ is set by the slider below the plot.

The blue lines then show the escape at each site **after** making the mutations $\mathcal{M}$.
For each site $r$, this is defined as $\frac{\sum_a x_{a,r} \times b_a\left(\mathcal{M}\right)}{A}$.
