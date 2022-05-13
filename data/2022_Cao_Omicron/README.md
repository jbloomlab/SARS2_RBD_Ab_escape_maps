# Data from Cao et al (2021)
Data from [Cao et al (2021)](https://www.biorxiv.org/content/10.1101/2021.12.07.470392v1).

The file [All_NAbs_Mutation.csv](All_NAbs_Mutation.csv) was provided by e-mail by Yunlong Richard Cao (first author) on Dec-15-2021.
Mutations with zero or near-zero escape are not included.

The file [antibodies.csv](antibodies.csv) has the information on individual antibodies provided by Yunlong Richard Cao in an Excel entitled `Supplementary_Table_6.xlsx`.

The file [spike.fasta](spike.fasta) gives the sequence of the Wuhan-Hu-1 spike as taken [from Genbank](https://www.ncbi.nlm.nih.gov/protein/QHD43416.1?report=fasta&log$=seqview).

The notebook [process_data.ipynb](process_data.ipynb) processes that data to create [study.yml](study.yml) and [data.csv](data.csv).
The output of this notebook was later manually edited in a few ways.
