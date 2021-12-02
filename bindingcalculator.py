"""Calculate residual antibody binding after some mutations.

Defines :class:`BindingCalculator` which does the calculation.

Written by Jesse Bloom.

"""


import pandas as pd


class BindingCalculator:
    """Calculates residual polyclonal antibody binding after some mutations.

    The model implemented here is the one described at
    https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/

    Parameters
    ----------
    csv_or_url : str
        Path to CSV or URL of CSV containing the escape data. Should
        have columns 'condition', 'normalized', 'metric', and 'escape'.
    eliciting_virus : {'all', 'SARS-CoV-2', 'SARS-CoV-1'}
        Include antibodies elicited by these viruses.
    normalized : {True, False}
        Whether to use normalized or non-normalized data.
    metric : {'sum of mutations at site', 'mean of mutations at site'}
        Which escape metric to use.
    mutation_escape_strength : float
        Scaling exponent :math:`s`; larger values mean stronger escape, see
        https://jbloomlab.github.io/SARS2_RBD_Ab_escape_maps/escape-calc/

    Attributes
    ----------
    escape_data : pandas.DataFrame
        The data frame read from `csv_or_url` after filtering for specified
        `normalized` and `metric` and scaling escape for each condition.
    sites : set
        All sites for which we have escape data. We can only calculate effects
        of mutations at these sites.

    Example
    -------
    Create escape calculator. Here we do that specifying a URL for a specific
    commit on GitHub repo storing data. Specifying the commit is just for
    testing purposes (so test still works if data updated); you will generally
    to use the equivalent file on the main branch without specifying commit
    (this is URL that is the default value of `csv_or_url`):

    >>> bindcalc = BindingCalculator(csv_or_url='https://raw.githubusercontent.com/jbloomlab/SARS2_RBD_Ab_escape_maps/9ac0417cf414423239511eceeb24abf86b58a067/processed_data/escape_calculator_data.csv')

    We can look at the escape data after geting the specified normalization
    and metric and then scaling each escape value relative to max for condition:

    >>> bindcalc.escape_data.head()
       condition       virus  site  normalized                    metric   escape  max_escape  scale_escape
    0  COV2-2196  SARS-CoV-2   331        True  sum of mutations at site  0.01715         1.0       0.01715
    1  COV2-2196  SARS-CoV-2   332        True  sum of mutations at site  0.02091         1.0       0.02091
    2  COV2-2196  SARS-CoV-2   333        True  sum of mutations at site  0.01978         1.0       0.01978
    3  COV2-2196  SARS-CoV-2   334        True  sum of mutations at site  0.02050         1.0       0.02050
    4  COV2-2196  SARS-CoV-2   335        True  sum of mutations at site  0.02015         1.0       0.02015

    We can also check what sites have escape data. Here we just
    show min and max sites with data:

    >>> min(bindcalc.sites)
    331
    >>> max(bindcalc.sites)
    531

    Now calculate the fraction of all polyclonal antibody binding retained
    after some sites have been mutated. If no sites have been mutated, all
    binding is retained:

    >>> bindcalc.binding_retained([])
    1.0

    With mutation at site 484:

    >>> round(bindcalc.binding_retained([484]), 3)
    0.589

    With mutation at site 417 and 484:

    >>> round(bindcalc.binding_retained([417, 484]), 3)
    0.457

    If you have a data frame of variants, you can just map the
    calculation of the binding retained to a new column, like this:

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

    We can also calculate the escape remaining at each site after a mutation:

    >>> bindcalc.escape_per_site([417, 484]).query('site in [484, 486, 490]').round(3)
         site  original_escape  retained_escape
    153   484            0.362            0.019
    155   486            0.254            0.076
    159   490            0.243            0.050

    """
    def __init__(self,
                 csv_or_url='https://raw.githubusercontent.com/jbloomlab/SARS2_RBD_Ab_escape_maps/main/processed_data/escape_calculator_data.csv',
                 eliciting_virus='SARS-CoV-2',
                 normalized=True,
                 metric='sum of mutations at site',
                 mutation_escape_strength=2,
                 ):
        """See main class docstring."""
        # read escape data 
        self.escape_data = pd.read_csv(csv_or_url)

        # make sure escape data has expected columns
        if not set(self.escape_data.columns).issuperset({'condition',
                                                         'site',
                                                         'normalized',
                                                         'escape',
                                                         'virus'}):
            raise ValueError(f"escape data in {csv_or_url} lacks expected columns")

        # filter by virus
        if eliciting_virus != 'all':
            if eliciting_virus not in set(self.escape_data['virus']):
                raise ValueError(f"invalid {eliciting_virus=}")
            self.escape_data = self.escape_data.query('virus == @eliciting_virus')

        # filter escape data to just the normalization and metric of interest
        for col, filter_val in [('normalized', normalized), ('metric', metric)]:
            if filter_val not in set(self.escape_data[col]):
                raise ValueError(f"{filter_val} not a valid value for {col}; "
                                 f"valid values are {set(self.escape_data[col])}")
            self.escape_data = (self.escape_data[self.escape_data[col] == filter_val]
                                .reset_index(drop=True)
                                )

        # get escape scaled by the max escape for that condition
        self.escape_data = (
                self.escape_data
                .assign(max_escape=lambda x: (x.groupby('condition')
                                              ['escape']
                                              .transform('max')
                                              ),
                        scale_escape=lambda x: x['escape'] / x['max_escape'],
                        )
                )

        # get all sites for which we have escape data
        self.sites = set(self.escape_data['site'])

        # set mutation escape strength
        self.mutation_escape_strength = mutation_escape_strength

        # number of conditions (antibodies)
        self._n_conditions = self.escape_data['condition'].nunique()

    def escape_per_site(self, mutated_sites):
        """Escape at each site after mutating indicated sites.

        Parameters
        ----------
        mutated_sites : array-like of integers
            List of mutated sites, must all be in :attr:`BindingCalculator.sites`.

        Returns
        -------
        pandas.DataFrame
            For each site, gives the original escape and the escape
            retained after mutations.

        """
        mutated_sites = set(mutated_sites)
        if not mutated_sites.issubset(self.sites):
            raise ValueError(f"invalid sites: {mutated_sites - self.sites}")
        df = (
            self.escape_data
            .assign(
                mutated=lambda x: x['site'].isin(mutated_sites).astype(int),
                site_bind_retain=lambda x: 1 - x['scale_escape'] * x['mutated']
                )
            .groupby('condition')
            .aggregate(cond_bind_retain=pd.NamedAgg('site_bind_retain',
                                                    'prod')
                       )
            ['cond_bind_retain']
            .pow(self.mutation_escape_strength)
            .reset_index()
            .merge(self.escape_data[['condition', 'site', 'escape']])
            .assign(retained_escape=lambda x: x['cond_bind_retain'] * x['escape'])
            .groupby('site')
            .aggregate(original_escape=pd.NamedAgg('escape', 'sum'),
                       retained_escape=pd.NamedAgg('retained_escape', 'sum'),
                       )
            ) / self._n_conditions
        return df.reset_index()

    def binding_retained(self, mutated_sites):
        """Fraction binding retained after mutating indicated sites.

        Parameters
        ----------
        mutated_sites : array-like of integers
            List of mutated sites, must all be in :attr:`BindingCalculator.sites`.

        Returns
        -------
        float
            The fraction binding retained after these mutations.

        """
        mutated_sites = set(mutated_sites)
        if not mutated_sites.issubset(self.sites):
            raise ValueError(f"invalid sites: {mutated_sites - self.sites}")
        binding_retained = (
            self.escape_data
            .assign(
                mutated=lambda x: x['site'].isin(mutated_sites).astype(int),
                site_bind_retain=lambda x: 1 - x['scale_escape'] * x['mutated']
                )
            .groupby('condition')
            .aggregate(cond_bind_retain=pd.NamedAgg('site_bind_retain',
                                                    'prod')
                       )
            ['cond_bind_retain']
            .pow(self.mutation_escape_strength)
            .sum()
            ) / self._n_conditions
        return binding_retained


if __name__ == '__main__':
    import doctest
    doctest.testmod()
