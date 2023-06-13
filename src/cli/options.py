
#
# --%%  Define shared help strings  %%--


build = """
What is the reference build for the VCF files? Primarily used together with '--rsids' for looking up rsids in dbsnp.
"""

database_path = """

"""
dbsnp_build = """
Sets the build version of dbsnp to be used. Only some versions are supported.
"""

dbbuild = """
What is the reference build for the VCF files? Default is to read this from the VCF files if it is stated there.
Properly formatted VCF files from dbSNP will have this information.
"""

log = """
Control logging. Valid levels: 'debug', 'info', 'warning', 'error', 'critical'.
"""

no_header = """
Include or suppress the header in VCF output
"""

output = """
Output file name.
"""

regions = """
Regions can be specified either on command line or in a tab-delimited file. The columns of the tab-delimited file can
contain either positions (two-column format: CHROM, POS) or intervals (three-column format: CHROM, BEG, END). Positions
are 1-based and inclusive. UCSC BED files can be used (trailing columns are ignored), but filename must have the '.bed'
or '.bed.gz' suffix. Note that sequence names must match exactly, "chr20" is not the same as "20".
"""

rsids = """
Extract entries based on RSIDs. RSIDs can be specified either on the command line or in a file with one id pr line. The
ids are translated into genomic coordinates using a dbsnp reference and then extracted by position. The actual ids in
the input files are ignorted completely.
"""

samples = """
File with samples to include in the output. Samples will be outputted in the exact same order as in the sample file
including outputting samples with missing values if no phenotype information was found. The sample file can be a plain
text file with sample names or a VCF file with sample genotypes.
"""
