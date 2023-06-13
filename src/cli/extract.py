###########################################################
#
# ---%%%  Snptool: Extract cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import os

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

@click.command(no_args_is_help=True)
@click.argument('files', nargs=-1)
@click.option('--build', '--reference-build', type=click.Choice(['grch37','grch38','hg19','hg38'], case_sensitive=False), default='grch37', help=OPTIONS.build, show_default=True)
@click.option('-h/-H', '--header/--no-header', default=True, show_default=True, help=OPTIONS.no_header)
@click.option('-i', '--rsids', type=pklib.CSVList(), default=[], help=OPTIONS.rsids)
@click.option('-o', '--output', type=click.File('w'), default='-', show_default=True, help=OPTIONS.output)
@click.option('-r', '--regions', type=pklib.CSVList(), default=[], help=OPTIONS.regions)
@click.pass_obj
def extract(snpdb, files, build, header, output, rsids, regions):
    """
    Extract one or more entries from one or more bcf/vcf files.

    Entries can be extrated based on chromosomal coordinates or on rsids.

    THIS COMMAND IS STILL EXPERIMENTAL; USE WITH CAUTION
    """
    try:
        snpdb.reference = build
        id_coords = list(snpdb.rsid2coords(rsids, build)) + regions
    except:
        id_coords = regions
        logger.warning(f"SnptoolDatabase: Unable to obtain rsids for 'reference = {build}'. All rsids will be ignored.")
    for fobj in files:
        snps = snptool.SNPstream(fobj, header=header, regions=pklib.IntervalList(id_coords))
        output.writelines(snps)

# --%%  END: Commands  %%--
#
##################################################


def main():
    try:
        database_path = os.environ['SNPTOOL_DATABASE_PATH']
        dbsnp_build   = os.environ['SNPTOOL_DBSNP_BUILD']
        obj = snptool.SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")
    except:
        logging.warning(f"SNPextractor: Unable to connect to database. Functions requiring the database will not work.")
        obj = None
    extract(auto_envvar_prefix='SNPTOOL', obj=obj)



