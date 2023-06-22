###########################################################
#
# ---%%%  SNPtool: Handling Snp-based information  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import logging
import sys

assert sys.version_info >= (3, 10), f"{sys.argv[0]} requires Python 3.8.0 or newer. Your version appears to be: '{sys.version}'."
logger = logging.getLogger(__name__)

from snptool.snptool import Querystream

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Define CLASS  %%--

class BIMBAMstream(Querystream):
    """An object for iterating over SNP-based input and output BIMBAM format."""
    __name__ = "BIMBAMstream"
    def __init__(self, filename, *args, format_string="ignored", header=False, **kwargs):
        """filename: A file with one SNP pr line.
           format_string: The format string. Must be fixed, so user input is ignored.
           header:   Must be False. BIMBAM Doesn't have a header.
        """
        format_string = '%INFO/AF %ID %ALT %REF[ %DS]\n'
        super().__init__(filename, format_string = format_string, header=False, *args, **kwargs)
        BIMBAMstream._validate(self)

    @staticmethod
    def _validate(self):
        """Validate stuff..."""
        super()._validate(self)

    def __iter__(self):
        return self

    def __next__(self):
        cols = next(self.process.stdout).split(" ")
        if float(cols[0]) > 0.5:
            cols[2:4] = (cols[3], cols[2])
            cols[4:] = map(lambda x: str(round(abs(float(x)-2),3)), cols[4:])
        return " ".join(cols[1:])

    def buff(self):
        print(f"Or as genotypes like AC AT GC, etc.")
        print(f"""And then the phenotype file:
                This file contains phenotype information. Each line is a number indicating the phenotype
                value for each individual in turn, in the same order as in the mean genotype file. Notice that
                only numeric values are allowed and characters will not be recognized by the software.
                Missing phenotype information is denoted as “NA”. The number of rows should be equal
                to the number of individuals in the mean genotype file. An example phenotype file with
                five individuals and one phenotype is as follows:
                1.2
                NA
                2.7
                -0.2
                3.3
                One can include multiple phenotypes as multiple columns in the phenotype file, and
                specify a different column for association tests by using “-n [num]”, where “-n 1” uses the
                original first column as phenotypes, and “-n 2” uses the second column, and so on and so
                forth. An example phenotype file with five individuals and three phenotypes is as follows:
                1.2 -0.3 -1.5
                NA 1.5 0.3
                2.7 1.1 NA
                -0.2 -0.7 0.8
                3.3 2.4 2.1
                For prediction problems, one is recommended to list all individuals in the file, but label
                those individuals in the test set as missing. This will facilitate the use of the prediction
                function implemented in DPR.
                """)
        print(f"""And the optional SNP annotation file:
                This file contains SNP information. The first column is SNP id, the second column is its
                base-pair position, and the third column is its chromosome number. The rows are not
                required to be in the same order of the mean genotype file, but must contain all SNPs in that
                file. An example annotation file with four SNPs is as follows:
                9/20
                rs1, 1200, 1
                rs2, 1000, 1
                rs3, 3320, 1
# TODO: And this shit needs a headline! So we must concatinate all input files first or the header gets repeaded (and will be wrong...)
                rs4, 5430, 1
                If an annotation file is not provided, the SNP information columns in the output file will
                have “-9” as missing values.
                """)





class BIMBAMstreamGT(BIMBAMstream):
    """An object for iterating over SNP-based input and output BIMBAM format."""
    __name__ = "BIMBAMstreamGT"
    def __init__(self, filename, *args, format_string="ignored", header=False, **kwargs):
        """filename: A file with one SNP pr line.
           format_string: The format string. Must be fixed, so user input is ignored.
           header:   Must be False. BIMBAM Doesn't have a header.
        """
        format_string = '%ID, %ALT, %REF[, %GT]\n'
        super().__init__(filename, format_string = format_string, header=False, *args, **kwargs)

    def __iter__(self):
# TODO: And this shit needs a headline! So we must concatinate all input files first or the header gets repeaded (and will be wrong...)
        return self

    def __next__(self):
        cols = next(self.process.stdout).split(", ")
        bases = [cols[1], cols[2]]
        genotypes = map(lambda x: x.split("|"), cols[3:])
        out = f"{cols[0]}, " + ", ".join(map(lambda x: bases[int(x[0])] + bases[int(x[1])], genotypes)) + "\n"
        return out


