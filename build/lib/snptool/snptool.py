###########################################################
#
# ---%%%  SNPtool: Handling Snp-based information  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import itertools
import logging
import pandas as pd
import re
import shlex
import subprocess
import sys

assert sys.version_info >= (3, 10), f"{sys.argv[0]} requires Python 3.8.0 or newer. Your version appears to be: '{sys.version}'."
logger = logging.getLogger(__name__)

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Define CLASS  %%--

class SNPstream(object):
    """An object for iterating over SNP-based input."""
    __name__ = "SNPstream"
    def __init__(self, filename, command='view', header=False, options="--output-type v", regions=[]):
        """filename: A file with one SNP pr line.
           header:   Include the header in the output?
           options:  A text string for shlex.split() with extra options for thebcftools call
           regions:  A list which returns text lines suitable for bcftools --regions-file."""
        super().__init__()
        region_str = ""
        for region in regions:
            region_str += str(region)
        self.command = ['bcftools', command] + shlex.split(options)
        self.command += ['--regions-file', '-', filename] if region_str else [filename]
        logger.debug(f"SNPstream: command = {self.command}")
        logger.info(f"SNPstream: Executing command '{' '.join(self.command)}'")
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, text=True)
        self.process.stdin.write(region_str)
        self.process.stdin.close()
        self = self._process_header(header)
        SNPstream._validate(self)

    @staticmethod
    def _validate(self):
        """Validate stuff..."""
#            output, self.error = process.communicate()
#            exit_status = process.returncode
        try:
            line = next(self.process.stdout)
            logger.debug(f"SNPstream: Detected source = {self.source}, build = {self.dbsnp_build}, reference = {self.reference}")
            self.process.stdout = itertools.chain(iter([line]), self.process.stdout)
        except StopIteration:
            if self.process.wait() != 0:
                logger.error(f"SNPstream: Error reading '{self.command[-1]}'. File may not be properly formatted or have invalid header. File skipped.")

    def __iter__(self):
        if self.header:
            self.process.stdout = itertools.chain(iter(self.meta), self.process.stdout)
        return self

    def __next__(self):
        return next(self.process.stdout)

    def _process_header(self, header):
        self.meta = list()
        pat_format = re.compile('##fileformat=(.+)\n')
        self.format = None
        pat_source = re.compile('##source=(.+)\n')
        self.source = None
        pat_dbsnp = re.compile('##dbSNP_BUILD_ID=([0-9]+)\n')
        self.dbsnp_build = None
        pat_reference = re.compile('##reference=([^.]+)([.p0-9]*)\n')
        self.reference = None
        for line in self.process.stdout:
            self.meta.append(line)
            if m := pat_format.fullmatch(line):
                self.format = m.group(1)
                logger.debug(f"SNPstream: Meta analysis found 'fileformat = {self.format}'")
            elif m := pat_source.fullmatch(line):
                self.source = m.group(1)
                logger.debug(f"SNPstream: Meta analysis found 'source = {self.source}'")
            elif m := pat_dbsnp.fullmatch(line):
                self.dbsnp_build = 'b' + m.group(1)
                logger.debug(f"SNPstream: Meta analysis found 'dbSNP_BUILD_ID = {self.dbsnp_build}'")
            elif m := pat_reference.fullmatch(line):
                self.reference = m.group(1)
                logger.debug(f"SNPstream: Meta analysis found 'reference = {self.reference}'")
            if not line.startswith('##'):
                break
        self.header = self.meta[-1] if header else False
        return self

    def concat(self, other):
        """Concatinate VCF streams together."""
        assert isinstance(other, SNPstream), "SNPstream.concat requires 'other' to be a SNPstream object."
        self.process.stdout = itertools.chain(self.process.stdout, other)




##################################################
#
# --%%  RUN: Define CLASS  %%--

class Querystream(SNPstream):
    """An object for iterating over SNP-based input."""
    __name__ = "Querystream"
    def __init__(self, filename, format_string, *args, command="ignored", options="", **kwargs):
        """
        format_string: The format string to use for bcftools query.
        command: Must be 'query' so user input is ignored."""
        super().__init__(*args, filename=filename, command="query", options=f"-H -f '{format_string}' {options}", **kwargs)

    def _process_header(self, header):
        meta = SNPstream(filename=self.command[-1], header=True, options="-h")
        self.meta = meta.meta
        self.format = meta.format
        self.source = meta.source
        self.dbsnp_build = meta.dbsnp_build
        self.reference = meta.reference
        line = next(self.process.stdout)
        self.header = line if header else False
        return self

