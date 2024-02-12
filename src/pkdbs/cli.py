###########################################################
#
# ---%%%  PKDBS: Pookies Database Tools CLI  %%%---
#

import click
import logging

import snptool.src.docs.options as OPTIONS

logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True, hidden=True)
@click.argument('files', nargs=-1)
@click.option('--build', '--reference-build', default=None, help=OPTIONS.dbbuild)
@click.option('--dbsnp-build', default=None, help=OPTIONS.dbsnp_build)
@click.pass_obj
def builddb(snpdb, files, build, dbsnp_build):
    """
    CURRENTLY FOR DEVELOPMENT USE ONLY. DO NOT USE.

    Used to create various resources, such as the local database.
    """
    from pkdbs import SnptoolDatabase
    from pkstreamers import SNPstreamer
    if snpdb:
        database_path = snpdb.path
        snpdb.close()
    else:
        database_path = "."
    for fobj in files:
        with SNPstreamer(fobj, command = 'query', options='--format "%CHROM\t%POS\t%ID\t%REF\t%ALT\n"') as dbsnp:
            database_file = dbsnp_build if dbsnp_build else dbsnp.dbsnp_build
            reference = build if build else dbsnp.reference
            mydb = SnptoolDatabase(f"{database_path}/{database_file}.db")
            logger.info(f" Building to file '{database_path}/{database_file}.db'")
            mydb.create_table(dbsnp, reference=reference)
            mydb.close()

