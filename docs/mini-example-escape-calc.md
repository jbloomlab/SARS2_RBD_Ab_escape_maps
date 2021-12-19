---
layout: mini-example-escape-calc
permalink: /mini-example-escape-calc/
---

This mini-example helps illustrate the principle behind the [full escape calculator]({{ site.baseurl }}{% link escape-calc.md %}).

The thin colored lines show deep mutational scanning escape maps for three different monoclonal antibodies:

 - LY-CoV016 (class 1 epitope)
 - LY-CoV555 (class 2 epitope)
 - REGN01987 (class 2 epitope)

The thick black line shows the mean escape across the three antibodies.
If you click on any antibody in the key on the top that simulates "escaping" it and its contribution to the overall mean escape profile disappears.

This is a simplified version of what the [full escape calculator]({{ site.baseurl }}{% link escape-calc.md %}) does: it averages over escape maps for a much larger set of antibodies.
Then it calculates how much of each antibody is escaped by mutating each site, and adjusts the mean escape accordingly.
