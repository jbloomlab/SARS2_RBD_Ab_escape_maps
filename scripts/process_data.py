"""Process input data to make merged CSVs with all data."""


import os

import ruamel.yaml

import pandas as pd


def valid_year(year):
    """Returns `True` if and only if valid year betweeen 2000 and 2030."""
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
                  'experimental_system',
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
            valid_subtypes = {'clinical', None}
        elif d['type'] == 'serum':
            valid_subtypes = {'convalescent', 'Moderna vaccine',
                              'Pfizer vaccine'}
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
                              columns=['condition', 'condition_subtype',
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
        raise ValueError(f"invalid `study_year` of {year} in {study_yaml}")
    url = study['study_url']
    experimental_system = study['experimental_system']
    if experimental_system not in {'yeast display',
                                   'lentiviral pseudotype',
                                   'VSV pseudotype',
                                   'SARS-CoV-2',
                                   }:
        raise ValueError(f"invalid {experimental_system=} in {study_yaml}")
    else:
        data['experimental_system'] = experimental_system

    return (first_author, study_year, url, data_type, data)


def process_data(data_dir='data',
                 study_yaml_base='study.yml',
                 data_csv_base='data.csv',
                 ):
    """Main function to process data."""
    print(f"Processing data in {data_dir}...")
    subdirs = sorted(os.path.join(data_dir, d) for d in os.listdir(data_dir)
                     if os.path.isdir(os.path.join(data_dir, d)) and
                     not d.startswith('.'))
    for i, subdir in enumerate(subdirs):
        print(f"  {i + 1}/{len(subdirs)}: {subdir}")
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


if __name__ == '__main__':
    process_data()
