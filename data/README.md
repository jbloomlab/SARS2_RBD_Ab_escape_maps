# Data for antibody escape maps
This directory holds all the input data on the maps of antigenic effects of mutations.

Within this directory, there is a subdirectory for each study.
The study-level subdirectories should be given short names describing the study by year, first author, and a brief descriptions, as in `2021_Starr_REGN`.
Each study-level subdirectory should have two files:

 1. A YAML file named `study.yml` that contains the following required fields (you are free to add additional fields if you'd like although they will be ignored in processing of the data):
  - *study_title*: title of the paper or pre-print from which the data are taken.
  - *study_first_author*: last name of first author of study.
  - *study_year*: year of study.
  - *study_journal*: journal of study.
  - *study_url*: weblink to study.
  - *lab*: lab that performed study.
  - *notes*: any relevant notes, should include specification of how data were extracted from study.
  - *conditions*: map antibodies or sera used (e.g., *CR3022*) to the following keyed attributes:
     + *type*: *antibody*, *antibody cocktail*, or *serum*. Note that data of type *antibody cocktail* are ignored!
     + *subtype*: more details about antibody or sera class:
       - if *type* is *antibody*, should be *class 1*, *class 2*, *class 3*, or *class 4* based on the [Barnes et al classification scheme](https://www.nature.com/articles/s41586-020-2852-1).
       - if type is *antibody cocktail*, should be *none*.
       - if *type* is *serum* can be: *convalescent serum*, *Moderna vaccine serum*, *Pfizer vaccine serum*. Note that *Pfizer vaccine serum* has not been implemented yet and a new color will need to be chosen for this serum type.
     + *year*: year that antibody or serum was isolated.
     + *eliciting_virus*: list of viruses that elicited antibody / sera, if missing default to [SARS-CoV-2, pre-Omicron SARS-CoV-2]`
     + *alias* (optional): another name for the antibody/sera
     + *notes* (optional): any notes on the antibody or serum
     + *known_to_neutralize* (optional): list of viruses the antibody neutralizes. Entries can either by strings giving virus names, or lists of virus and IC50, as in `[[Wuhan-Hu-1, 5.7]]`. Assumed `[Wuhan-Hu-1]` if not specified.

 2. A CSV file named `data.csv` that contains the actual data.
    The required columns are listed below. Sites with no entry for a given condition are assumed to have a *mut_escape* value of 0.
     + *condition*: the antibody or sera name listed under *conditions* in `study.yml`.
     + *site*: the site in the spike protein (use Wuhan-Hu-1 numbering).
     + *wildtype*: the wildtype amino acid at the site.
     + *mutation*: the mutant amino acid.
     + *mut_escape*: the escape fraction for this mutation.
