"""Process input data to make merged CSVs with all data."""


import os
import string

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
    study_keys = {'data_type',
                  'study_title',
                  'study_first_author',
                  'study_year',
                  'study_url',
                  'spike',
                  'notes',
                  'conditions',
                  }
    if study_keys != set(study):
        raise ValueError(f"Invalid key set in {study_yaml}:\n" +
                         str(study_keys.symmetric_difference(study)))

    # Get data frame of conditions
    conditions = []
    for condition, d in study['conditions'].items():
        for key in ['type', 'subtype', 'year']:
            if key not in d:
                raise ValueError(f"Missing {key=} for {condition=} "
                                 f"in {study_yaml}")
        if d['type'] in {'antibody', 'antibody cocktail'}:
            valid_subtypes = {'clinical antibody', 'not clinical antibody'}
        elif d['type'] == 'serum':
            valid_subtypes = {'convalescent serum', 'Moderna vaccine serum',
                              'Pfizer vaccine serum'}
        else:
            raise ValueError(f"Invalid {d['type']=} in {study_yaml} "
                             f"for {condition=}")
        if d['subtype'] not in valid_subtypes:
            raise ValueError(f"Invalid {d['subtype']=} in {study_yaml}"
                             f" for {condition=}")
        if not valid_year(d['year']):
            raise ValueError(f"Invalid {d['year']=} in {study_yaml}"
                             f" for {condition=}")
        conditions.append((condition, d['type'], d['subtype'], d['year']))
    conditions = pd.DataFrame(conditions,
                              columns=['condition', 'condition_type',
                                       'condition_subtype', 'condition_year'])

    # process the data
    data = pd.read_csv(data_csv)
    if 'condition' not in data.columns:
        raise ValueError(f"{data_csv} lacks column `condition`")
    if set(data['condition']) != set(conditions['condition']):
        raise ValueError(f"conditions in {study_yaml} do not match those in "
                         f"{data_csv}:\n" +
                         set(data['condition'].symmetric_difference(
                                set(conditions['condition']))))
    data_type = study['data_type']
    if data_type == 'yeast_RBD_DMS':
        cols = ['condition', 'site', 'wildtype', 'mutation', 'mut_escape']
        for col in cols:
            if col not in data.columns:
                raise ValueError(f"{data_csv} lacks column `{col}`")
        data = data[cols]
    else:
        raise ValueError(f"invalid {data_type=} in {study_yaml}")
    data = conditions.merge(data, on='condition', validate='one_to_many')

    # get general information on study
    first_author = study['study_first_author']
    study_year = study['study_year']
    if not valid_year(study_year):
        raise ValueError(f"invalid `study_year` {study_year} in {study_yaml}")
    url = study['study_url']

    return (first_author, study_year, url, data_type, data)


def process_data(data_dir='data',
                 study_yaml_base='study.yml',
                 data_csv_base='data.csv',
                 ):
    """Process the input data."""
    print(f"Processing data in {data_dir}...")
    merged_data = {}
    studies = {}
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
            extras = [f for f in os.listdir(subdir)
                      if not f.startswith('.') and f not in
                      {study_yaml_base, data_csv_base}]
            if extras:
                raise IOError(f"extra files in {subdir}: {extras}")
        first_author, year, url, data_type, data = process_study(study_yaml,
                                                                 data_csv)
        # make sure directory has appropriate prefix / suffix
        study = os.path.basename(subdir)
        if not study.startswith(f"{year}_{first_author}_"):
            raise ValueError(f"{subdir} should start with "
                             f"{year}_{first_author} to reflect year "
                             'and first author')
        print(f"{study} has {data['condition'].nunique()} conditions")
        data = data.assign(study=study)
        if data_type in merged_data:
            if study in studies[data_type]:
                raise ValueError(f"duplicate {study} for {data_type}")
            assert study not in merged_data[data_type]['study'].unique()
            studies[data_type].append((study, url))
            merged_data[data_type] = merged_data[data_type].append(data)
        else:
            merged_data[data_type] = data
            studies[data_type] = [(study, url)]

    outdir = 'results/merged_data'
    os.makedirs(outdir, exist_ok=True)
    for data_type, df in merged_data.items():
        out_csv = os.path.join(outdir, f"{data_type}_data.csv")
        print(f"Writing merged {data_type} data to {out_csv}")
        df.to_csv(out_csv, index=False, float_format='%.4g')
        out_studies = os.path.join(outdir, f"{data_type}_studies.csv")
        print(f"Writing {data_type} studies to {out_studies}")
        (pd.DataFrame(studies[data_type],
                      columns=['study', 'url'])
         .to_csv(out_studies, index=False)
         )


if __name__ == '__main__':
    process_data()
