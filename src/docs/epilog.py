
#
# --%%  Define shared epilog strings  %%--

bimbam = """

FIX HERE!!!!!

BIMBAM Basic Genotype File with genotype calls. Automatically sets
option '--no-indels'.

BIMBAM Genotype Distribution Format with
"""

extract = """
NOTE: While multi-file input is supported, it may not always result in a syntactically valid header. If this is a
problem, use only one input file (you can call 'bcftools concat' or 'bcftools merge' yourself to make one).

KNOWN 'BUG':
Extract retrives SNPs by regional coordinates meaning that overlapping features such as INDELs may get extracted as
well. The same will happen if you use bcftools to fetch snps. Future versions will (try to) improve upon this.
"""

genoinfo = """
NOTE: A Geno file requires unique ids which will be created by using the 'ID' column except when it's '.' (=> no id).
In that case an ID is constructed like this 'CHR:POS:REF:VAR'. Probliems will likely arise if those IDs are not
unique and the script may not report on this. It is up to you as user to ensure your IDs are unique.

NOTE: Because Geno files require the sample genotype matrix to be transposed it scales really poorly with the size of
the vcf file(s). It is recommend to use 'snptool extract' first to get the precise list of variants desired.
"""

snptool = """

"""

