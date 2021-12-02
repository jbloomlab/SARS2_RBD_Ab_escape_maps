# bindingcalculator module

Calculate residual antibody binding after some mutations.

Defines `BindingCalculator` which does the calculation.

Written by Jesse Bloom.


### class bindingcalculator.BindingCalculator(csv_or_url='https://raw.githubusercontent.com/jbloomlab/SARS2_RBD_Ab_escape_maps/main/processed_data/escape_calculator_data.csv', eliciting_virus='SARS-CoV-2', normalized=True, metric='sum of mutations at site', mutation_escape_strength=2)
Bases: `object`

Calculates residual polyclonal antibody binding after some mutations.

The model implemented here is the one described at
[https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/)

csv_or_url

    Path to CSV or URL of CSV containing the escape data. Should
    have columns ‘condition’, ‘normalized’, ‘metric’, and ‘escape’.

eliciting_virus

    Include antibodies elicited by these viruses.

normalized

    Whether to use normalized or non-normalized data.

metric

    Which escape metric to use.

mutation_escape_strength

    Scaling exponent $s$; larger values mean stronger escape, see
    [https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/](https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/)

escape_data

    The data frame read from csv_or_url after filtering for specified
    normalized and metric and scaling escape for each condition.

sites

    All sites for which we have escape data. We can only calculate effects
    of mutations at these sites.

Create escape calculator. Here we do that specifying a URL for a specific
commit on GitHub repo storing data. Specifying the commit is just for
testing purposes (so test still works if data updated); you will generally
to use the equivalent file on the main branch without specifying commit
(this is URL that is the default value of csv_or_url):

```python
>>> bindcalc = BindingCalculator(csv_or_url='https://raw.githubusercontent.com/jbloomlab/SARS2_RBD_Ab_escape_maps/9ac0417cf414423239511eceeb24abf86b58a067/processed_data/escape_calculator_data.csv')
```

We can look at the escape data after geting the specified normalization
and metric and then scaling each escape value relative to max for condition:

```python
>>> bindcalc.escape_data.head()
   condition       virus  site  normalized                    metric   escape  max_escape  scale_escape
0  COV2-2196  SARS-CoV-2   331        True  sum of mutations at site  0.01715         1.0       0.01715
1  COV2-2196  SARS-CoV-2   332        True  sum of mutations at site  0.02091         1.0       0.02091
2  COV2-2196  SARS-CoV-2   333        True  sum of mutations at site  0.01978         1.0       0.01978
3  COV2-2196  SARS-CoV-2   334        True  sum of mutations at site  0.02050         1.0       0.02050
4  COV2-2196  SARS-CoV-2   335        True  sum of mutations at site  0.02015         1.0       0.02015
```

We can also check what sites have escape data. Here we just
show min and max sites with data:

```python
>>> min(bindcalc.sites)
331
>>> max(bindcalc.sites)
531
```

Now calculate the fraction of all polyclonal antibody binding retained
after some sites have been mutated. If no sites have been mutated, all
binding is retained:

```python
>>> bindcalc.binding_retained([])
1.0
```

With mutation at site 484:

```python
>>> round(bindcalc.binding_retained([484]), 3)
0.589
```

With mutation at site 417 and 484:

```python
>>> round(bindcalc.binding_retained([417, 484]), 3)
0.457
```

If you have a data frame of variants, you can just map the
calculation of the binding retained to a new column, like this:

```python
>>> variants = pd.DataFrame([('Wuhan-Hu-1', []),
...                          ('B.1.351', [417, 484, 501]),
...                          ('B.1.1.7', [501]),
...                          ('B.1.429', [452])],
...                         columns=['variant', 'mutated RBD sites'])
>>> variants['binding_retained'] = (variants['mutated RBD sites']
...                                 .map(bindcalc.binding_retained))
>>> variants.round(3)
      variant mutated RBD sites  binding_retained
0  Wuhan-Hu-1                []             1.000
1     B.1.351   [417, 484, 501]             0.419
2     B.1.1.7             [501]             0.930
3     B.1.429             [452]             0.877
```

We can also calculate the escape remaining at each site after a mutation:

```python
>>> bindcalc.escape_per_site([417, 484]).query('site in [484, 486, 490]').round(3)
     site  original_escape  retained_escape
153   484            0.362            0.019
155   486            0.254            0.076
159   490            0.243            0.050
```


#### binding_retained(mutated_sites)
Fraction binding retained after mutating indicated sites.

mutated_sites

    List of mutated sites, must all be in `BindingCalculator.sites`.

float

    The fraction binding retained after these mutations.


#### escape_per_site(mutated_sites)
Escape at each site after mutating indicated sites.

mutated_sites

    List of mutated sites, must all be in `BindingCalculator.sites`.

pandas.DataFrame

    For each site, gives the original escape and the escape
    retained after mutations.
