###########################################################
#
# ---%%%  Class SnptoolDatabase: Handling sqlite3 functionality  %%%---
#

import logging
import sqlite3
import sys

from .SnptoolDbIterator import SnptoolDbIterator

assert sys.version_info >= (3, 10), f"{sys.argv[0]} requires Python 3.10.0 or newer. Your version appears to be: '{sys.version}'."
logger = logging.getLogger(__name__)

# TODO: The table and reference names suck!

class SnptoolDatabase(object):
    """Class for translating rsids using a database with a sqlite table created from dbsnp. Can hold more than one
       table, but only if they contain the same columns, but with data from different reference builds."""
    __SYNONYMS = {"grch37": "grch37",
                  "hg19":   "hg19",
                  "grch38": "grch38",
                  "hg38":   "hg38"}

    def __init__(self, db_path, reference="GRCh37"):
        """db_path: Path to the database"""
        logger.info(f" Attempting to connect to sqlite database at '{db_path}'.")
        (self.path, self.file) = db_path.rsplit("/", maxsplit=1)
        self.reference = reference
        try:
            self.conn   = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            logger.info(f" Connected to sqlite database at path = '{self.path}', file = '{self.file}', table = '{self.table}'")
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") # Getting all tables from sqlite_master
            logger.debug(f" sqlite tables = {self.cursor.fetchall()}")
        except sqlite3.Error as error: 
            logger.warning(f" Unable to connect to database at '{db_path}'. Functions requiring the database will not work.")
            logger.error(f" ERROR - {error}")
            self.close()

    def close(self):
        """Close the database connection."""
        self.conn.commit()
        self.conn.close()

    def create_table(self, dbsnp, reference):
        """Create a table in the database and populate it with values
        dbsnp: An iter with snps used to populate table
        reference: Name of the reference used to create the table."""
        self.reference = reference
        c = self.conn.cursor()
        logger.info(f" Building table = '{self.table}' in database file = '{self.file}'")

        # Create a table with an index on the 'id' column and commit
        for i in range(0,2):
            try:
                c.execute(f"CREATE TABLE {self.table} (key INTEGER PRIMARY KEY, chrom TEXT, pos INTEGER, id TEXT, ref TEXT, alt TEXT)")
                logger.info(f" Table '{self.table}' created")
                break
            except sqlite3.OperationalError:
                c.execute(f"DROP TABLE IF EXISTS {self.table}")
                logger.warning(f" Already existing table '{self.table}' was dopped...")

        # Append values to the table. Could be an independent 'append' method so that we could extend an existing table?
        for snp in dbsnp:
            snplist = snp.split()
            try:
                snplist[0] = int(snplist[0].removeprefix("NC_0000").removeprefix("chr").split(".")[0])
            except ValueError:
                pass
            c.execute(f"INSERT INTO {self.table} (chrom, pos, id, ref, alt) VALUES (?, ?, ?, ?, ?)", snplist)
        c.execute(f"CREATE INDEX IF NOT EXISTS idx_name ON {self.table} (id)")
        logger.debug(f" Done building table.")
        self.conn.commit()

    def rsid2coords(self, rsid, reference):
        """rsid: Some kind of iterable with rsids to translate into genomic coordinates"""
        logger.debug(f" Searching for ids[0:10] = {rsid[0:10]}...")
        self.reference = reference
        c = self.conn.cursor()
        logger.debug(f" SELECT chrom, pos FROM {self.table} WHERE id IN ({', '.join(rsid)})")
        try: return SnptoolDbIterator(c.execute(f"SELECT chrom,pos FROM {self.table} WHERE id IN ({', '.join('?'*len(rsid))})", rsid))
        except sqlite3.Error as error:
            logger.warning(f" Unable to obtain rsids for 'reference = {self.reference}'. All rsids will be ignored.")
            logger.debug(f" ERROR - {error}")
            return iter([])

    @property
    def table(self):
        """This is not *the* (only) table. It is not even the table you're looking for. But it is the last table you
        accessed. (Really just exists to help ensure access is consistent)."""
        return f"dbsnp_{self.reference}"

    @property
    def reference(self):
        """This is not *the* reference. It is the last reference that you accessed. It's about changing modes, not
        record-keeping."""
        return self._reference

    @reference.setter
    def reference(self, value):
        """Change the reference to access other tables in the database. Remember: It's about changing modes."""
        self._reference = None if value is None else self.__SYNONYMS[str(value).casefold()]

