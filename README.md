# TuBa-seq Analysis Pipeline #

Command-line data analysis tools for tumor size profiling by **Tu**mor-**Ba**rcoded deep sequencing. Please refer to our publication in [Nature Methods](http://www.nature.com/nmeth/index.html) for details. 

**Currently, the "Unadulterated" version is working, while the base version is _incomplete_. This pipeline and its installation and usage will be simplified in the coming months.**

OVERVIEW
--------
This pipeline uses the [DADA2](https://github.com/benjjneb/dada2) de-noising and sample inference algorithm to identify unique DNA barcodes. Sequencing error rates are estimated from the non-degenerate regions of DNA barcodes using a novel approach. 

INSTALLATION & USAGE
--------------------
While *DADA2* is written in R, the pre-processing and post-processing scripts, and utilities are written in Python. Both require Python 3.2 and R 3.2 or later (what a fun coincidence). _DADA2_ should install from **Bioconductor** as follows: 

```
## try http:// if https:// URLs are not supported
source("https://bioconductor.org/biocLite.R")
biocLite("dada2")
## Other R packages used for summarizing output to install:
biocLite("shortRead")
biocLite("ggplot2")
```
See [DADA2 Installation](https://benjjneb.github.io/dada2/dada-installation.html) for details. 

A pip installer for the python package is pending. For now, dependencies can be met with the following command: 

```
pip3 install numpy scipy pandas rpy2 matplotlib biopython
```

CONTACT
-------
Feedback is most appreciated. Please contact me at cmcfarl2 [at] stanford [dot] edu with any questions or suggestions. 

WEBSITE
-------
Documentation and source code can be found at https://github.com/petrov-lab/tuba-seq


## FILE MANIFEST
----------------
    
Often two versions of files exist: a base version and a version with an "_unadulterated" suffix. Base versions are recommended for general use, while unadulterated versions replicate results published in [Rodgers et al. (2017)](http://www.nature.com/nmeth/index.html). Behavior of these two versions should remain similar, however we want to provide users a way to reproduce our published findings, while also developing a more generic pipeline that incorporates evolving best practices. Unadulterated versions are un-maintained. 

### params.py

Module that combines all scientifically-relevant *python* script parameters. Individual scripts often have additional command-line arguments, but these arguments define input/output directories, logging or multi-threading, *not* parameters that affect tumor calls. 

### preprocess.py

Filters raw FASTQ files from deep sequencing using a template of the intended barcode setup. Outputs training files for *DADA2* estimation of error rates and clutering files for *DADA2* barcode clustering. Uses [Needleman-Wunsch](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) alignment of reads to the barcode template for filtering & trimming. 

### DADA2_error_training.R

Estimates a model of sequencing errors from the region of reads that flank the barcodes. Uses output of preprocess.py. 

### DADA2_clustering.R

Clusters unique read pileups into putative tumors based on the *DADA2* amplicon denoising algorithm. Uses output of preprocess.py and DADA2_error_training.R. For samples exceeding 2M reads, I recommend broadcasting this task to a distributed computing array. 

### postprocess.py

Consolidates *DADA2* clustering outputs. Annotates sgRNAs and DNA benchmarks, and isolates the barcode region of reads. Clusters in separate sequencing runs, belonging to the same mouse, and clusters known to derive from the same DNA barcode (by virtue of the DNA template) are consolidated. Summary statistics are provided. 

### final_processing.py

Creates the final estimates of tumor sizes used in this study. These steps are application specific, and we have converged upon best practices for generic tuba-seq experiments. Mice are annotated by their germ-line genotype, their time of sacrifice, and by the viral pool used to initiate tumors. Viral infections not belonging to the intended pool used are removed (these are very rare events). Estimates any bias in PCR amplification that is correlated with the GC content of barcodes and subtracts this bias.

### DADA2_derep.R

De-replicates training & clustering files for *DADA2*. Separating this first step from the algorithm saves space and time (when runs are repeated). This file has been deprecated in the base version.


### test/

Test suite. 

### tuba_seq/

Directory of shared python modules.
