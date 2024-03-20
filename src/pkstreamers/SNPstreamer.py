###########################################################
#
# ---%%%  PKStreams: Basic Handling of Streams  %%%---
#

# -%  Perform Basic Setup  %-

import logging
import re
import shlex
import sys

from .handler import SubprocessHandler
from .reader import SubprocessReader

logger = logging.getLogger(__name__)

# TODO: Finish the 'region' part of the streamer

class SNPstreamer(SubprocessHandler):
    """An object for iterating over SNP-based input."""
    __name__ = "SNPstreamer"

    def __init__(self, filename, command='view', options="--output-type v", regions=[], *args, **kwargs):
        """filename: A file with one SNP pr line.
           command:  The command to send to bcftools.
           header:   Currently ignorred and that is probably a BUG!
           options:  A text string for shlex.split() with extra options for thebcftools call
           regions:  A list which returns text lines suitable for bcftools --regions-file."""
        command = ['bcftools', command] + shlex.split(options)
        command += ['--regions-file', '-', filename] if regions else [filename]
        super().__init__(command, input_data=regions, *args, **kwargs)
        self = self._process_header(filename)

        SNPstreamer._validate(self)

    @staticmethod
    def _validate(self):
        """Validate stuff..."""
        # Looks like we made it. Let's report we're ready to read.
        logger.debug(f"SNPstream: Detected source = {self.source}, build = {self.dbsnp_build}, reference = {self.reference}")

    def _process_header(self, filename):
        """Scan through the VCF header and extract information.
           filename: The name of the file whose header we should scan."""
        self.header = list()                
        pat_format = re.compile('##fileformat=(.+)')
        self.format = None
        pat_source = re.compile('##source=(.+)')
        self.source = None
        pat_dbsnp = re.compile('##dbSNP_BUILD_ID=([0-9]+)')
        self.dbsnp_build = None
        pat_reference = re.compile('##reference=([^.]+)([.p0-9]*)')
        self.reference = None
        with SubprocessReader(['bcftools', 'view', '--header-only', filename]) as header:
            for line in header:
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
            if header.check_errors():
                sys.exit("Terminating due to errors")
        return self

    def append(self, other):
        """Append 'other' into self.
        Other: An instance of this class or similar
        ...This approach may not work...
        """
        import sys
        sys.exit("Not Implemented yet! And it may indeed never work...")
        return self
