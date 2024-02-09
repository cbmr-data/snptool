###########################################################
#
# ---%%%  Class BIMBAMstreamGP: Convert VCF to bimbam Genotype Distribution Format  %%%---
#

import logging

from .BIMBAMstreamDS import BIMBAMstreamDS

logger = logging.getLogger(__name__)


##################################################
#
# --%%  RUN: Define CLASS BIMBAMstreamGP  %%--

class BIMBAMstreamGP(BIMBAMstreamDS):
    """Iterates over VCF input and outputs BIMBAM Genotype Distribution Format.

    This file is similar to the mean genotype file. The first three columns are identical to those of the
    mean genotype file. The only difference is that each SNP represented by two adjacent columns
    instead of one. The first of the two columns denotes the posterior probability of SNP being 0 and
    the second column for probability being 1. An example of genotype distribution file of two SNPs
    and three individuals follows.
    rs1, A, T, 0.98, 0.01, 0.60, 0.38, 0.90, 0.06
    rs2, G, C, 0.80, 0.14, 1.00, 0.00, 0.55, 0.20
    
    From: https://www.haplotype.org/download/bimbam-manual.pdf
    """
    __name__ = "BIMBAMstreamGP"

    def __init__(self, filename, format_string = '%ID, %ALT, %REF[, %DS]\n%ID[, %GP]\n', *args, **kwargs):
        """The idea is that we split it into two lines printing the alleles from the first, and probabilities from the second.
        filename:      A file with one SNP pr line.
        format_string: Must be set to provide two lines so as to match the expectation of __next__
        """
        super().__init__(filename, format_string=format_string, *args, **kwargs)

    def __next__(self):
        """Process each query line and convert to BIMBAM GP format. Use self.nan to specify missing."""
        (rsid1, alt, ref, *_) = super().__next__().split(self.sep)
        (rsid2, *gps) = super(BIMBAMstreamDS, self).__next__().split(self.sep)
        if rsid1 == rsid2:
            first_two = map(lambda x: self.sep.join(x.split(",")[0:2]), gps)
            return f"{self.sep.join([rsid1, alt, ref])}{self.sep}{self.sep.join(first_two)}"
        else:
            import sys
            sys.exit()

