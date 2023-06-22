
#
# --%%  Define shared epilog strings  %%--

bimbam = """
A BIMBAM dataset consists of three files, a genotype file, a phenotype file, and an optional annotation file. The
genotype file has two versions: 'Basic Genotype' which contains alleles (), or 'Mean Genotype' which contains allelic
dosage scores. This script currently only converts to the Mean Genotype file, but future versions will likely provide
more options.
"""

extract = """
KNOWN BUGS:

While multi-file input is supported, it is likely a little buggy. If possible, use only one input file.

Extract retrives SNPs by regional coordinates meaning that overlapping features such as INDELs may get extracted as
well. Future versions will improve upon this.
"""

snptool = """

"""

