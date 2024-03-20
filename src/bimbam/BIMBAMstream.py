###########################################################
#
# ---%%%  Class BIMBAMstream: Convert VCF to bimbam  %%%---
#

#
# -%  Perform Basic Setup  %-

import logging
import re
import select
import subprocess
import sys

from pkstreamers import SubprocessReader, SubprocessHandler

logger = logging.getLogger(__name__)



##################################################
#
# --%%  RUN: Define CLASS BIMBAMstream  %%--

class BIMBAMstream(SubprocessHandler):
    """A core class with common tools between the specialized BIMBAM classes. Cannot be evoked directly (without error)."""
    __name__ = "BIMBAMstream"

    def __init__(self, filename, indels=True, nan="?", sep=", ", format_string='%ID, %POS, %CHROM\\n', *args, **kwargs):
        """filename:        A file with one SNP pr line.
           indels:          Boolean. Should indels (and multiallelic snps) be printed?
           number_variants: Int with number of variants in all input files. Any 'False' value will cause the number to be calculated from current input file only.
           sep:             Separator used in output. Should be one of [", ", " ", "\t", "; "].
        """
        if indels:
            handler_command = ['bcftools', 'query', '--format', f"{format_string}", filename]
        else:
            reader_command  = ['bcftools', 'view', '--min-alleles', '2', '--max-alleles', '2', '--types', 'snps', filename]
            handler_command = ['bcftools', 'query', '--format', f"{format_string}"]

        ps = subprocess.Popen(reader_command, stdout=subprocess.PIPE, text=True)
        super().__init__(handler_command, input_data=ps.stdout, *args, **kwargs)

        self.samples = list(SubprocessReader(['bcftools', 'query', '--list-samples', filename]))
        self.indels = indels
        self.nan = nan
        self.sep = sep
        BIMBAMstream._validate(self)

    def __next__(self):
        """Core next functionality for bimbam. We're esentially just replacing the 'sep' to ensure the users 'sep' choice is respected."""
        line = super().__next__()
        cols = map(lambda x: self.nan if x == "." else x, line.split(", "))
        return self.sep.join(cols)

    @staticmethod
    def _validate(self):
        """Validate stuff... No need to call super() here since the __init__'s super calls validate for the parent class."""
        # Check samples
        logger.debug(f" Samples found [0:10] = {self.samples[0:10] + ['...']}")
        assert self.samples, f"ERROR! No samples found in file!"
        # Check self.nan
        legal_nans = ['?', 'N']
        assert self.nan in legal_nans, f"Illegal missing indicator specified. Indicator must be one of {legal_nans}"
        # Check self.sep
        legal_seps = [' ', ', ', '; ', '\t']
        assert self.sep in legal_seps, f"Illegal seperator specified. Seperator must be one of {legal_seps}"
        logger.debug(f" Successfully validated {self}")
