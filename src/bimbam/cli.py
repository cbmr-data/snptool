###########################################################
#
# ---%%%  Snptool: Bimbam cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import sys

import snptool.options as OPTIONS

logger = logging.getLogger(__name__)

epilog = """
NOTE: Given the definition, the Basic Genotype format only supports biallelic variants. Therefore '--no-indels' will be
forced in effect when '--genotype' is used.

NOTE: According to the definition in the bimbam manual, then Mean Genotype Files must be sorted according to allelic
frequency with the minor allele going first, and with scores expressing the minor allelic dosage. For this reason the
allelic order of the vcf file will not be retained in output when the alternate is the minor allele, and the dosage
scores will be recalculated accordingly.
"""

@click.command(no_args_is_help=True, epilog=epilog)
@click.argument('files', nargs=-1)
@click.option('--dosage', 'format_flag', flag_value='DS', default=True, help=OPTIONS.dosage)
@click.option('--genotype', 'format_flag', flag_value='GT', help=OPTIONS.genotype)
@click.option('--location', 'format_flag', flag_value='LOC', help=OPTIONS.location)
@click.option('--probability', 'format_flag', flag_value='GP', help=OPTIONS.probability)
@click.option('--indels/--no-indels', default=False, show_default=True, help=OPTIONS.indels)
@click.option('-o', '--output', type=click.File('w'), default='-', show_default=True, help=OPTIONS.output)
@click.pass_obj
def bimbam(snpdb, files, format_flag, indels, output):
    """
    Convert VCF file to BIMBAM Basic or Mean Genotype File.

    A true BIMBAM data set consists of a Genotype File, a Phenotype File, and an optional SNP Location File.
    Only the Genotype File is created here. To build a full BIMBAM dataset the other two files must be created 
    by other means.

    Several types of BIMBAM Genotype Files exists, all with their own distinct formats. Supported here are 'Basic
    Genotype', 'Mean Genotype' and 'Genotype Distribution' via the flags '--genotype', '--dosage' and '--',
    respectively. They each in turn read the 'GT', 'DS' and 'GP' fields in the VCF file and will fail if those fields
    are missing from the VCF file.

    Read about the different formats here:
    https://www.haplotype.org/download/bimbam-manual.pdf

    THIS COMMAND IS STILL EXPERIMENTAL; USE WITH CAUTION
    """
# Should we cross-ref the db for rsids? (There's something being said for using the IDs from the VCF. This should at least be default.)
    if format_flag == 'DS':
        from .BIMBAMstreamDS import BIMBAMstreamDS
        for fobj in files:
            with BIMBAMstreamDS(fobj, indels=indels) as stream:
                for output_line in stream:
                    output.writelines(f"{output_line}\n")

    elif format_flag == 'GT':
        if indels:
            logger.warning(f" Basic Genotype format only supports biallelic variants; option '--indels' ignored.")
        from .BIMBAMstreamGT import BIMBAMstreamGT
        for fobj in files:
            with BIMBAMstreamGT(fobj) as stream:
                for output_line in stream:
                    output.writelines(f"{output_line}\n")

    elif format_flag == 'GP':
        from .BIMBAMstreamGP import BIMBAMstreamGP
        for fobj in files:
            with BIMBAMstreamGP(fobj, indels=indels) as stream:
                for output_line in stream:
                    output.writelines(f"{output_line}\n")

    else:
        logger.error(f" Unrecognized format flag '{format_flag}'")
        sys.exit("Terminating due to errors.")


def main():
    bimbam(auto_envvar_prefix='SNPTOOL')

