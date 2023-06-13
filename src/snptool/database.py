###########################################################
#
# ---%%%  Database: Handling sqlite3 functionality  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import logging
import sqlite3
import sys

assert sys.version_info >= (3, 10), f"{sys.argv[0]} requires Python 3.10.0 or newer. Your version appears to be: '{sys.version}'."
logger = logging.getLogger(__name__)



##################################################
#
# --%%  RUN: Define CLASS  %%--

class SnptoolDatabase(object):
    """Class for translating rsids using a database with a sqlite table created from dbsnp. Can hold more than one
       table, but only if they contain the same columns, but with data from different reference builds."""
    __SYNONYMS = {"grch37": "grch37",
                  "hg19":   "hg19",
                  "grch38": "grch38",
                  "hg38":   "hg38"}

    def __init__(self, db_path, reference="GRCh37"):
        """db_path: Path to the database"""
        logging.debug(f"SnptoolDatabase: Attempting to connect to sqlite database at '{db_path}'.")
        self.conn = sqlite3.connect(db_path)
        (self.path, self.file) = db_path.rsplit("/", maxsplit=1)
        self.reference = reference
        logging.debug(f"SnptoolDatabase: Connected to sqlite database at path = '{self.path}', file = '{self.file}', table = '{self.table}'")

    def close(self):
        """Close the database connection"""
        self.conn.close()

    def create(self, dbsnp, reference):
        """Create a table in the database and populate it with values
        reference: Name of the reference used in the table to create."""
        self.reference = reference
        logger.info(f"SnptoolDatabase: Building database '{self.file}', table '{self.table}'")
    
        # Create a table with an index on the 'id' column and commit
        c = self.conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table}
                      (key INTEGER PRIMARY KEY, chrom INTEGER, pos INTEGER, id TEXT, ref TEXT, alt TEXT)''')
        for snp in dbsnp:
            snplist = snp.split()
            snplist[0] = int(snplist[0].removeprefix("NC_0000").removeprefix("chr").split(".")[0])
            c.execute(f"INSERT INTO {self.table} (chrom, pos, id, ref, alt) VALUES (?, ?, ?, ?, ?)", snplist)
        c.execute(f"CREATE INDEX IF NOT EXISTS idx_name ON {self.table} (id)")
        self.conn.commit()

    def rsid2coords(self, rsid, reference):
        """rsid: Some kind of iterable with rsids to translate into genomic coordinates"""
        logging.debug(f"SnptoolDatabase: Searching for ids[0:10] = {rsid[0:10]}...")
        self.reference = reference
        c = self.conn.cursor()
        try: return SnptoolDatabaseIterator(c.execute(f"SELECT chrom,pos FROM {self.table} WHERE id IN ({', '.join('?'*len(rsid))})", rsid))
        except:
            logger.warning(f"SnptoolDatabase: Unable to obtain rsids for 'reference = {self.reference}'. All rsids will be ignored.")
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




##################################################
#
# --%%  RUN: Define CLASS  %%--

class SnptoolDatabaseIterator(object):
    def __init__(self, cursor):
        self.c = cursor

    def __iter__(self):
        return self

    def __next__(self):
        if result := self.c.fetchone():        
            logging.debug(f"{result}")
            return [result[0], result[1], result[1]]
        else:
            raise StopIteration


