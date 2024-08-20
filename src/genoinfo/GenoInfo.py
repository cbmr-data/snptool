###########################################################
#
# ---%%%  CLASS GenoInfo: Convert input to Geno/Info files  %%%---
#

from collections.abc import MutableMapping
import logging
import pandas as pd
import sys

logger = logging.getLogger(__name__)

class GenoInfo(MutableMapping):
    """
    Reads subject dosage scores from a VCF file into a pandas DataFrame.

    Parameters:
    vcf_fobj (file object): A fileobject to a VCF file with the variants.

    Returns:
    pd.DataFrame: A DataFrame containing the dosage scores.
    """
    def __init__(self, vcf_fobj, samples=None, data_field='DS'):
        """"""
        from pysam import VariantFile

        # Open the VCF file and get the sample names from the VCF header
        variants = VariantFile(vcf_fobj)
        self.samples = list(variants.header.samples) if samples is None else samples
        if self.samples != list(variants.header.samples):
            logger.error(f" Samples do not match - ERROR!")
            sys.exit("Aborting due to errors.")
        info_dict = {}

        # Iterate over each record in the VCF file
        rows = []
        for record in variants:
            # For simplicity, assume 'DS' (Dosage Score) is in the FORMAT field
            if 'DS' in record.format:
                dosages = record.samples.values()
                row = {}
                info = {
                    'CHROM': record.chrom,
                    'POS': record.pos,
                    'ID': record.id,
                    'REF': record.ref,
                    'ALT': ','.join(str(alt) for alt in record.alts),
                    'QUAL': record.qual,
                    'FILTER': record.filter.keys(),
                }
                snpid = info['ID'] if len(info['ID']) > 1 else f"{info['CHROM']}:{info['POS']}:{info['REF']}:{info['ALT']}"
                if snpid in info_dict:
                    i = 1
                    newid = snpid
                    while newid in info_dict:
                        newid = snpid + f".{i}"
                        i += 1
                    logger.warning(f" Duplicated key detected - Replacing with unique key: '{snpid}' => '{newid}' ")
                    snpid = newid
                info_dict[snpid] = info
                for sample, data in zip(self.samples, dosages):
                    row[sample] = data[data_field]
                rows.append(row)
    
        # Convert list of rows into a DataFrame
        self.info = pd.DataFrame(info_dict).transpose()
        self.geno = pd.DataFrame(rows, index=self.info.index).transpose()

    def __delitem__(self, key):
        del self._store[key]

    def __getattr__(self, attr):
        return getattr(self._store, attr)

    def __getitem__(self, key):
        return self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return self._store.__repr__()

    def __setitem__(self, key, value):
        self._store[key] = value

    @property
    def geno(self):
        return self._store

    @geno.setter
    def geno(self, value):
        self._store = value

    def append(self, obj, *args, axis=1, **kwargs):
        """
        Join two GenoInfo objects together.

        Parameters:
        Axis (ignored): Option is ignored as the concat axis must be fixed
        The rest are forwarded to pd.concat

        Result:
        info, geno updated with pd.concat
        """
        if isinstance(obj, GenoInfo):
            self.info = pd.concat([self.info] + [obj.info], *args, **kwargs)
            self.geno = pd.concat([self.geno] + [obj.geno], *args, axis='columns', **kwargs)
        else:
            logger.error(" ERROR - Trying to merge incompatible types (both objects must be GenoInfo instances)")
            sys.exit("Aborting due to errors.")