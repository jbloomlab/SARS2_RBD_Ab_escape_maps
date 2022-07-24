"""Process input data to make merged CSVs with all data."""


import os
import string

from dmslogo.utils import AxLimSetter

import pandas as pd

import ruamel.yaml


def valid_year(year):
    """Return `True` if and only if valid year betweeen 2000 and 2030."""
    if not isinstance(year, int):
        raise ValueError(f"invalid {year=}")
    return 2000 <= year <= 2030


def process_study(study_yaml, data_csv):
    """Parse data from specific study."""
    # read YAML file on study
    with open(study_yaml) as f:
        study = ruamel.yaml.YAML(typ='safe').load(f)
    study_keys = {
                  'study_title',
                  'study_first_author',
                  'study_year',
                  'study_journal',
                  'study_url',
                  'lab',
                  'conditions',
                  }
    if study_keys != (set(study) - {'notes'}):
        raise ValueError(f"Invalid key set in {study_yaml}:\n" +
                         str(study_keys.symmetric_difference(study)))

    # Get data frame of conditions
    conditions = []
    for condition, d in study['conditions'].items():
        for key in ['type', 'subtype', 'year']:
            if key not in d:
                raise ValueError(f"Missing {key=} for {condition=} "
                                 f"in {study_yaml}")
        if d['type'] == 'antibody':
            valid_subtypes = {'class 1', 'class 2', 'class 3', 'class 4'}
        elif d['type'] == 'antibody cocktail':
            valid_subtypes = {'none'}
        elif d['type'] == 'serum':
            valid_subtypes = {'convalescent serum', 'Moderna vaccine serum',
                              'Pfizer vaccine serum', 'B.1.351 convalescent plasma'}
        else:
            raise ValueError(f"Invalid {d['type']=} in {study_yaml} "
                             f"for {condition=}")
        if d['subtype'] not in valid_subtypes:
            raise ValueError(f"Invalid {d['subtype']=} in {study_yaml}"
                             f" for {condition=}")
        if not valid_year(d['year']):
            raise ValueError(f"Invalid {d['year']=} in {study_yaml}"
                             f" for {condition=}")
        if 'alias' in d:
            alias = f"({d['alias']})"
        else:
            alias = ''
        if 'eliciting_virus' in d:
            assert isinstance(d["eliciting_virus"], list), d["eliciting_virus"]
            eliciting_virus = ";".join(s.strip() for s in d['eliciting_virus'])
        else:
            eliciting_virus = 'SARS-CoV-2;pre-Omicron SARS-CoV-2'
        if "SARS-CoV-1" in eliciting_virus:
            if "SARS-CoV-2" in eliciting_virus.split(";"):
                raise ValueError(f"{eliciting_virus=} has SARS-CoV-2 and SARS-CoV-1")
        elif "SARS-CoV-2" not in eliciting_virus.split(";"):
            raise ValueError(f"{eliciting_virus=} should have SARS-CoV-2 if not SARS-CoV-1")
        if 'known_to_neutralize' in d:
            assert isinstance(d["known_to_neutralize"], list)
            known_to_neutralize = [s.strip() for [s, _] in d['known_to_neutralize']]
            ic50s = [ic50 for [_, ic50] in d["known_to_neutralize"]]
            assert "any" not in known_to_neutralize
            known_to_neutralize.append("any")
            ic50s.append(min(ic50s))
            known_to_neutralize = ";".join(known_to_neutralize)
            ic50s = ";".join(f"{ic50:.3g}" for ic50 in ic50s)
        else:
            known_to_neutralize = "Wuhan-Hu-1;any"
            ic50s = "NA;NA"
        conditions.append((str(condition), d['type'], d['subtype'], d['year'],
                           alias, eliciting_virus, known_to_neutralize, ic50s))
    conditions = pd.DataFrame(conditions,
                              columns=['condition', 'condition_type',
                                       'condition_subtype', 'condition_year',
                                       'condition_alias', 'eliciting_virus',
                                       'known_to_neutralize', "IC50s"])

    # process the data, dropping any zero mut_escape values
    data = pd.read_csv(data_csv).query("mut_escape != 0")
    if 'condition' not in data.columns:
        raise ValueError(f"{data_csv} lacks column `condition`")
    if set(data['condition']) != set(conditions['condition']):
        raise ValueError(f"conditions in {study_yaml} do not match those in "
                         f"{data_csv}:\n" +
                         str(set(data['condition']).symmetric_difference(
                                set(conditions['condition']))))
    cols = ['condition', 'site', 'wildtype', 'mutation', 'mut_escape']
    for col in cols:
        if col not in data.columns:
            raise ValueError(f"{data_csv} lacks column `{col}`")
    data = data[cols]
    data = conditions.merge(data, on='condition', validate='one_to_many')

    # get general information on study
    first_author = study['study_first_author']
    study_year = study['study_year']
    study_journal = study['study_journal']
    lab = study['lab']
    if lab not in {'Bloom_JD', 'Xie_XS'}:
        raise ValueError(f"invalid {lab=}")
    if not valid_year(study_year):
        raise ValueError(f"invalid `study_year` {study_year} in {study_yaml}")
    url = study['study_url']

    return (first_author, study_year, study_journal, url, lab, data)


def process_data(data_dir='data',
                 study_yaml_base='study.yml',
                 data_csv_base='data.csv',
                 ):
    """Process the input data."""
    print(f"Processing data in {data_dir}...")
    merged_data = []
    studies = []
    subdirs = sorted(os.path.join(data_dir, d) for d in os.listdir(data_dir)
                     if os.path.isdir(os.path.join(data_dir, d)) and
                     not d.startswith('.'))
    for i, subdir in enumerate(subdirs):
        print(f"  {i + 1}/{len(subdirs)}: {subdir}... ", end='')
        study_yaml = os.path.join(subdir, study_yaml_base)
        data_csv = os.path.join(subdir, data_csv_base)
        for f in [study_yaml, data_csv]:
            if not os.path.isfile(f):
                raise IOError(f"Missing file {f}")
        first_author, year, jrnl, url, lab, data = process_study(study_yaml,
                                                                 data_csv)
        # make sure directory has appropriate prefix / suffix
        study = os.path.basename(subdir)
        if not study.startswith(f"{year}_{first_author}_"):
            raise ValueError(f"{subdir} should start with "
                             f"{year}_{first_author} to reflect year "
                             'and first author')
        print(f"{study} has {data['condition'].nunique()} conditions")
        data = data.assign(study=study,
                           lab=lab)
        if study in studies:
            raise ValueError(f"duplicate study {study}")
        studies.append((study, first_author, year, jrnl, url, lab))
        merged_data.append(data)
    merged_data = pd.concat(merged_data, ignore_index=True)

    # ignore antibody cocktail data
    merged_data = merged_data.query('condition_type != "antibody cocktail"')

    # compute site-level escape
    assert len(merged_data) == len(merged_data.groupby(['condition', 'study',
                                                        'site', 'mutation'])) 
    site_data = (
        merged_data
        .groupby(['condition', 'study', 'site'],
                 as_index=False, dropna=False)
        .aggregate(site_total_escape=pd.NamedAgg('mut_escape', 'sum'))
        )

    # Normalize site-level escape, first setting to one for each condition,
    # and then further adjusting so that median value is at no greater than 0.5
    limset = AxLimSetter(datalim_pad=0,
                         min_upperlim=1,
                         include_zero=True,
                         max_from_quantile=(0.5, 0.05),
                         )
    assert len(site_data) == len(site_data.groupby(['condition', 'study', 'site']))
    for col in ['site_total_escape']:
        site_data[col] = site_data[col] / (site_data
                                           .groupby(['condition', 'study'])
                                           [col]
                                           .transform('max')
                                           )
        site_data['norm_max'] = (site_data
                                 .groupby(['condition', 'study'])
                                 [col]
                                 .transform(lambda s: limset.get_lims(s)[1])
                                 )
        site_data[col] = site_data[col] / site_data['norm_max']
        site_data = site_data.drop(columns='norm_max')

    # merge site data into data frame and add other `dms-view` columns
    merged_data = (
        merged_data
        .merge(site_data)
        .assign(label_site=lambda x: x['wildtype'] + x['site'].astype(str),
                protein_site=lambda x: x['site'],
                protein_chain='E',  # for PDB 6moj
                )
        )

    outdir = 'processed_data'
    os.makedirs(outdir, exist_ok=True)
    out_csv = os.path.join(outdir, 'escape_data.csv')
    print(f"\nWriting escape data to {out_csv}")
    merged_data.to_csv(out_csv, index=False, float_format='%.4g')

    out_studies = os.path.join(outdir, 'studies.csv')
    print(f"\nWriting studies to {out_studies}")
    studies_df = (
        pd.DataFrame(studies,
                     columns=['study', 'first_author', 'year', 'journal', 'url', 'lab'])
        .assign(index=lambda x: x.groupby(['first_author', 'year', 'journal'])
                                ['study'].transform('cumcount'),
                n_dup=lambda x: x.groupby(['first_author', 'year', 'journal'])
                                ['study'].transform('count'),
                suffix=lambda x: x.apply(
                                   lambda r:  ('' if r['n_dup'] < 2 else
                                               string.ascii_lowercase[r['index']]),
                                   axis=1),
                citation=lambda x: x['first_author'] + ' et al. ' + x['journal'] +
                                   ' (' + x['year'].astype(str) + x['suffix'] + ')',
                )
        .sort_values(['year', 'citation'])
        [['study', 'citation', 'url']]
        )
    studies_df.to_csv(out_studies, index=False)

    # add studies to end of docs/index.md
    for md in ['docs/index.md', 'docs/escape-calc.md']:
        print(f"\nWriting citations to {md}")
        with open(md) as f:
            md_lines = f.readlines()
        iline = 0
        while iline < len(md_lines):
            if md_lines[iline].startswith('## Citations'):
                break
            else:
                iline += 1
        else:
            raise ValueError('never found line starting with "## Citations"')
        for line in md_lines[iline + 1:]:
            if line.startswith('#'):
                raise ValueError('found another header line after citations')
        with open(md, 'w') as f:
            f.write(''.join(md_lines[: iline]))
            f.write('## Citations for experimental data\n')
            f.write('The experimental data shown here are taken from the following papers:\n')
            for tup in studies_df.itertuples(index=False):
                f.write(f"  - [{tup.citation}]({tup.url})\n")



if __name__ == '__main__':
    process_data()
