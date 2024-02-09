###########################################################
#
# ---%%%  Class BIMBAMstreamDS: Convert VCF to bimbam dosage format  %%%---
#

import logging

from .BIMBAMstream import BIMBAMstream

logger = logging.getLogger(__name__)



##################################################
#
# --%%  RUN: Define CLASS BIMBAMstreamDS  %%--

class BIMBAMstreamDS(BIMBAMstream):
    """Iterates over VCF input and outputs BIMBAM Mean Genotype File Format.

    This file has a different form from the genotype input file. There are no number of individual line
    or number of SNPs line. The first column of the mean genotype files is the SNP ID, the second and
    third columns are allele types with minor allele first. The rest columns are the mean genotypes of
    different individuals - numbers between 0 and 2 that represents the (posterior) mean genotype, or
    dosage of the minor allele.
    
    From: https://www.haplotype.org/download/bimbam-manual.pdf
    """
    __name__ = "BIMBAMstreamDS"

    def __init__(self, filename, format_string='%ID, %ALT, %REF[, %DS]\n', *args, **kwargs):
        """filename: A file with one SNP pr line.
        """
        super().__init__(filename, format_string=format_string, *args, **kwargs)

    def __next__(self):
        """Process each query line and convert to BIMBAM DS format. Use minor allele first and self.nan to specify missing."""
        out = super().__next__()

        # All this just to print the minor allele first...
        valid_numbers = []
        invers_dosage = []
        cols = out.split(self.sep)
        for value in cols[3:]:
            try:
                # Attempt to convert each value to a float and add it to the list if successful
                valid_numbers.append(float(value))
                invers_dosage.append(str(round(2 - float(value), 3)))
            except ValueError:
                # If the conversion fails (invalid number), do not sum value, but save it for output.
                invers_dosage.append(self.nan)
                continue
        try: 
            if (sum(valid_numbers) / len(valid_numbers)) > 1:
                out = self.sep.join(([cols[0], cols[2], cols[1]] + invers_dosage))
        except ZeroDivisionError:
            pass

        return out


