###########################################################
#
# ---%%%  Class BIMBAMstreamGT: Convert VCF to bimbam basic genotype file  %%%---
#

#
# -%  Perform Basic Setup  %-

import itertools
import logging
import re

from .BIMBAMstream import BIMBAMstream

logger = logging.getLogger(__name__)



##################################################
#
# --%%  RUN: Define CLASS BIMBAMstreamGT  %%--

class BIMBAMstreamGT(BIMBAMstream):
    """Iterates over VCF input and outputs BIMBAM Basic Genotype File Format.

    Genotypes should be for bi-allelic SNPs, all on the same chromosome. The number on the first line
    indicates the number of individuals; the number in the second line indicates the number of SNPs.
    Optionally, the third row can contain individual ID: this line should begin with the string IND, with
    subsequent strings indicating the identifier for each individual in turn. Subsequent rows contain
    the genotype data for each SNP, with one row per SNP. In each row the first column gives the
    SNP ID (which can be any string, but might typically be an rs number), and subsequent columns
    give the genotypes for each individual in turn. Genotypes must be coded in ACGT while missing
    genotypes can be indicated by NN or ??.
    
    From: https://www.haplotype.org/download/bimbam-manual.pdf
    """
    __name__ = "BIMBAMstreamGT"

    def __init__(self, filename, *args, **kwargs):
        """Handles things slightly different since we now need to load everything into memory.
        Everything is a chani over variants and header, and we close the subprocesses already in init.
        filename:        A file with one SNP pr line.
        """
        super().__init__(filename, format_string = "%ID, %ALT, %REF[, %GT]\\n", indels=False, *args, **kwargs)
        self.variants = list(self.process.stdout)
        self.header = [self.count_variants()]
        self.header.append(self.count_subjects())
        self.header.append(self.sep.join(["IND"] + self.samples))
        self.close()

    def __iter__(self):
        """Attach the header if needed to stdout"""
        self = super().__iter__()
        self.process.stdout = itertools.chain(self.header, self.variants)
        return self

    def __next__(self):
        """Process each query line and convert to BIMBAM GT format. Use self.nan to specify missing.
        Do not super() but handle local because self.process.stdout is now a chain object."""
        line = next(self.process.stdout)
        if line:
            line = line.strip()
        else:
            raise StopIteration
        try:
            (out, b1, b2, *genotypes) = line.split(self.sep)
            alleles = map(lambda x: re.split("[|/]", x), genotypes)
            for gt in alleles:
                try:
                    out += f"{self.sep}{(b1, b2)[int(gt[0])] + (b1, b2)[int(gt[1])]}"
                except ValueError:
                    out += f"{self.sep}{2 * self.nan}"
        except (IndexError, ValueError):
            return line
        return out

    def close(self):
        """Handle the fact that self.process.stdout can be a chain without a close method."""
        if self.process.stdout:
            try:
                self.process.stdout.close()
                super().close()
            except AttributeError:
                self.process.stdout = None

    def count_variants(self):
        """Calculate the number of snps/variants in the vcf file using 'bcftools | wc'."""
        return str(len(self.variants))

    def count_subjects(self):
        """Calculate the number of subjects/samples in the vcf file using self.samples."""
        return str(len(self.samples))

    def append(self, other):
        """Append 'other' into self.
        Other: An instance of class BIMBAMstreamGT or similar
        """
        import sys
        sys.exit("Not Implemented yet! And it may indeed never work...")
        return self