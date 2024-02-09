###########################################################
#
# ---%%%  Class BIMBAMlocation: Convert VCF to bimbam SNP location file  %%%---
#

from .BIMBAMstream import BIMBAMstream

class BIMBAMlocation(BIMBAMstream):
    """The optional SNP location file:

    This file contains SNP information. The first column is SNP id, the second column is its
    base-pair position, and the third column is its chromosome number. The rows are not
    required to be in the same order of the mean genotype file, but must contain all SNPs in that
    file. An example annotation file with four SNPs is as follows:
    rs1, 1200, 1
    rs2, 1000, 1
    rs3, 3320, 1
    rs4, 5430, 1
    
    If an annotation file is not provided, the SNP information columns in the output file will
    have “-9” as missing values.

    From: https://www.haplotype.org/download/bimbam-manual.pdf
    """
    __name__ = "BIMBAMlocation"

    def __init__(self, filename, format_string='%ID, %POS, %CHROM\n', nan="-9", *args, **kwargs):
        """
        filename:      A file with one SNP pr line.
        format_string: Must be set to provide data to match the expectation of __next__
        nan:           Missing must be '-9'
        """
        super().__init__(filename, format_string=format_string, nan=nan, *args, **kwargs)
    

