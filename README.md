# Disease-Human-rRNA

## Creating Reference Genome of one person

### Problem

Bases have no positions in the reference file
  
### Solution
  
Convert CRAM to BAM format
  
```sh
samtools view -b -T /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa -o ERR3240115_rDNA.bam ERR3240115_rDNA.cram
```
  
CRAM files store only the differences from a reference genome to save space. To reconstruct the full alignment information in BAM format, samtools needs access to the same reference genome that was used during the initial CRAM creation.
  
Extracting Reference Alleles for Non-Variant Positions
  
```sh
samtools mpileup -f /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa ERR3240115_rDNA.bam > ERR3240115_rDNA.mpileup
```
  
Determine what the reference alleles are at each position where reads are aligned, including positions where no variants have been called.

### Additional Information
  
Script for this conversion & extraction: 
  
```
scratch/cgsb/hochwagen/Human_rDNA_project/1000Geno/runthis_fc1132_v2.sh
```
  
Notebook for constructing reference genome of one person: 
  
```
Reference_Genome.ipynb
```
