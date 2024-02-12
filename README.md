# SNPtool

SNPTOOL is a collection of tools for working with SNPs or SNP-based formats.
  
Essentially a wrapper around several popular tools such as bcftools, providing a more accessible interface as well
as expanding or combining some functionalities not directly available in the individual tools. It is optimized for
resource-efficiency and should be about as efficient as the tools it relies on.

It is possible to pre-configure most options using environmental variables. Such should use '_' instead of '-' and
they should carry the 'SNPTOOL_' prefix. Thus: SNPTOOL_DATABASE_PATH will set the 'database-path' option.


Should be possible to install with:

```
pip install git+https://github.com/carsten0202/snptool
```

