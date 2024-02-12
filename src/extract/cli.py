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
import sys

from docs import OPTIONS
import pklib

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
@click.option('-i', '--rsids', type=pklib.SampleList(mode='rb'), default=[], help=OPTIONS.rsids)
@click.option('-o', '--output', type=click.File('w'), default='-', show_default=True, help=OPTIONS.output)
@click.option('-r', '--regions', type=pklib.BED3(), default=[], help=OPTIONS.regions)
@click.pass_obj
def extract(snpdb, files, build, header, output, rsids, regions):
    """
    Extract one or more entries from one or more bcf/vcf files.

    Entries can be extrated based on chromosomal coordinates or on rsids.

    THIS COMMAND IS STILL EXPERIMENTAL; USE WITH CAUTION
    """
    from pkstreamers import SNPstreamer
    id_coords = list(map(lambda x: "\t".join(str(v) for v in x), list(snpdb.rsid2coords(rsids, build)) + regions))
    header = "--with-header" if header else "--no-header"
    if not id_coords:
        logger.error(f" No (usuable) SNP ids or coordinates found. Either you forgot to give any, or they failed parsing.")
        sys.exit("Terminating due to errors...")
    for fobj in files:
        with SNPstreamer(fobj, command="view", options=header, regions=id_coords) as snps:
            for snp in snps:
                output.writelines(f"{snp}\n")
        header = "--no-header" # Do not print headers of anything but the first file

# --%%  END: Commands  %%--
#
##################################################


def main():
    from pkdbs.SnptoolDatabase import SnptoolDatabase
    try:
        database_path = os.environ['SNPTOOL_DATABASE_PATH']
        dbsnp_build   = os.environ['SNPTOOL_DBSNP_BUILD']
        obj = SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")
    except KeyError:
        obj = None
    extract(auto_envvar_prefix='SNPTOOL', obj=obj)



