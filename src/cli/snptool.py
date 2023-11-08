###########################################################
#
# ---%%%  Snptool: Snptool cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import os

from cli.bimbam import bimbam
from cli.extract import extract
import cli.epilog as EPILOG
import cli.options as OPTIONS
from cli.version import __version__
import pklib
import snptool

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Commands  %%--

@click.group(epilog=EPILOG.snptool)
@click.option('--database-path', default=os.getcwd(), help=OPTIONS.database_path, show_default=True)
@click.option('--dbsnp-build', type=click.Choice(['b153','b155','b156'], case_sensitive=False), default='b156', help=OPTIONS.dbsnp_build, show_default=True)
@click.option('--log', default="warning", help=OPTIONS.log, show_default=True)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, dbsnp_build, log, database_path):
    """    
    SNPTOOL is a collection of tools for working with SNPs or SNP-based formats.
    
    Essentially a wrapper around several popular tools such as bcftools, providing a more accessible interface as well
    as expanding or combining some functionalities not directly available in the individual tools. It is optimized for
    resource-efficiency and should be about as efficient as the tools it relies on.

    It is possible to pre-configure most options using environmental variables. Such should use '_' instead of '-' and
    they should carry the 'SNPTOOL_' prefix. Thus: SNPTOOL_DATABASE_PATH will set the 'database-path' option.
    """
    try: log_num = getattr(logging, log.upper())
    except AttributeError:
        raise ValueError(f"Invalid log level: '{log}'")
    logging.basicConfig(level=log_num)
    ctx.obj = snptool.SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")

#@cli.result_callback()
#def cli_callback(dbsnp, dbsnp_build_id, log, snptool_db_path):
#    dbsnp.close()
#    logging.debug(f"cli_callback: Closed database.")

# CLI: Add Bimbam command
cli.add_command(bimbam)

# CLI: Add Extract command
cli.add_command(extract)



@cli.command(no_args_is_help=True, hidden=True)
@click.argument('files', nargs=-1)
@click.option('--build', '--reference-build', default=None, help=OPTIONS.dbbuild)
@click.option('--dbsnp-build', default=None, help=OPTIONS.dbsnp_build)
@click.pass_obj
def builddb(snpdb, files, build, dbsnp_build):
    """
    CURRENTLY FOR DEVELOPMENT USE ONLY. DO NOT USE.

    Used to create various resources, such as the local database.
    """
    if snpdb:
        database_path = snpdb.path
        snpdb.close()
    else:
        database_path = "."
    for fobj in files:
        dbsnp = snptool.Querystream(fobj, '%CHROM\t%POS\t%ID\t%REF\t%ALT\n')
        database_file = dbsnp_build if dbsnp_build else dbsnp.dbsnp_build
        mydb = snptool.SnptoolDatabase(f"{database_path}/{database_file}.db")
        logging.info(f"builddb: Building to file: {database_path}/{database_file}.db")
        mydb.create_table(dbsnp, reference=dbsnp.reference)
        mydb.close()



@cli.command(no_args_is_help=True, hidden=True)
@click.argument('files')
def test(files):
    """TEST COMMAND DO NOT USE"""
    pass

# --%%  END: Commands  %%--
#
##################################################


def main():
    cli(auto_envvar_prefix='SNPTOOL')


