# Disease-Human-rRNA

## Creating Reference Genome ##

**Problem:**

Looked at the reference file and bases have no positions.

**Solution:**

- Convert CRAM to BAM format

`samtools view -b -T /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa -o ERR3240115_rDNA.bam ERR3240115_rDNA.cram`

CRAM files store only the differences from a reference genome to save space. To reconstruct the full alignment information in BAM format, samtools needs access to the same reference genome that was used during the initial CRAM creation.

- Extracting Reference Alleles for Non-Variant Positions

`samtools mpileup -f /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa ERR3240115_rDNA.bam > ERR3240115_rDNA.mpileup`

Determine what the reference alleles are at each position where reads are aligned, including positions where no variants have been called.



Script for this conversion & extraction: 

_scratch/cgsb/hochwagen/Human_rDNA_project/1000Geno/runthis_fc1132_v2.sh_

Notebook for constructing reference genome of 1 person: 

_Reference_Genome.ipynb_
