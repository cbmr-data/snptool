###########################################################
#
# ---%%%  Snptool: Bimbam cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import os

import cli.epilog as EPILOG
import cli.options as OPTIONS
import pklib
import snptool 

logger = logging.getLogger(__name__)

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Commands  %%--

@click.command(no_args_is_help=True, epilog=EPILOG.bimbam)
@click.argument('files', nargs=-1)
#@click.option('--format-tag', type=click.Choice(['DS','GT'], case_sensitive=False), default="DS", show_default=True)
#@click.option('--dosage', 'format_flag', flag_value='DS', default=True, help=OPTIONS.dosage)
#@click.option('--genotype', 'format_flag', flag_value='GT', help=OPTIONS.genotype)
@click.option('-o', '--output', type=click.File('w'), default='-', show_default=True, help=OPTIONS.output)
@click.pass_obj
def bimbam(snpdb, files, output):
    """
    Convert VCF file to BIMBAM Mean Genotype File.

    A true BIMBAM data set consists of a Mean Genotype File, a Phenotype File, and an optional SNP Annotation File.
    Only the Mean Genotype File is created here. To build a full BIMBAM dataset the other two files must be created 
    by other means.

    THIS COMMAND IS STILL EXPERIMENTAL; USE WITH CAUTION
    """
# Should we cross-ref the db for rsids? (There's something being said for using the IDs from the VCF. This should at least be default.
    for fobj in files:
        snps = snptool.BIMBAMstream(fobj)
        output.writelines(snps)

# --%%  END: Commands  %%--
#
##################################################


def main():
    bimbam(auto_envvar_prefix='SNPTOOL')




