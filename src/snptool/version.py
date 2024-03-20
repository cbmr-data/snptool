
__version__ = """0.6.2"""
# v0.1: Basic functionality
# v0.2: Prepared for module integration
# v0.3: Added the BIMBAM command and vcf2bimbam
# v0.4: Fixed some I/O bugs and enabled multi vcf file input
# v0.5: Rewritten the I/O routines. Cleaned code. Fixed bimbam - at least for basic functionality
# v0.6: Are we going to reintroduce the Geno/Info files?
# v0.6.1: Fixed a bug in BIMBAM and recoded the handler to work without shell=True
# v0.6.2: Introduced threading in handler.py. Works (but not with 'head'; meh...)

# TODO: In extract: The header is bogus if you concatinate several vcf files together.
#           Easiest fix is probably to run bcftools concat on the data first. Only way to be sure.
# TODO: Geno/Info
# TODO: BIMBAM Add support for UKB's wonderful partial dosage scores?
# TODO: (But not here...) Add support for phenotype file in phenotool.
# TODO: You could reduce the db size by using: https://github.com/phiresky/sqlite-zstd
