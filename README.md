# Human-rDNA

Weekly Updates here: https://docs.google.com/presentation/d/1OQmLHz-VFHUhOgELqBhIQRyfAfHbC0luyfAHhpZx_OY/edit?usp=sharing

9/27 Lab Presentation: https://docs.google.com/presentation/d/1dDxmGy5-T72uO3BKXMyuPYrsKZXvIXdaurrm5zPUgp8/

## Creating reference genome of one person

### Problem

Bases have no positions in the reference file
  
### Solution
  
Step 1: Convert CRAM to BAM format
  
```sh
samtools view -b -T /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa -o ERR3240115_rDNA.bam ERR3240115_rDNA.cram
```
  
CRAM files store only the differences from a reference genome to save space. To reconstruct the full alignment information in BAM format, samtools needs access to the same reference genome that was used during the initial CRAM creation.
  
Step 2: Extracting reference alleles for all positions
  
```sh
samtools mpileup -f /scratch/cgsb/hochwagen/Human_rDNA_project/rDNA_prototype_prerRNA_only.fa ERR3240115_rDNA.bam > ERR3240115_rDNA.mpileup
```
  
Determine what the reference alleles are at each position where reads are aligned, including positions where no variants have been called.

**Later, realized it was way easier to solve problem by enumerating the FASTA reference file. Both methods output the same reference files (See notebook).**

### Additional Information
  
Script for this conversion & extraction: 
  
```
scratch/cgsb/hochwagen/Human_rDNA_project/1000Geno/runthis_fc1132_v2.sh
```
  
Notebook for constructing reference genome of one person: 
  
```
Reference_Genome.ipynb
```

## Estimating copy number of Human rDNA (multi-copy genes)

### Problem

Current Allele Frequency(AF) in Variant Calling Files(VCF) confound coverage and copies

### Solution

Step 1: Calculate Genome Coverage Ratio: Divide the number of base pairs per sample by the total base pairs in the hg38 reference genome (3 billion).

Step 2: Determine Average rDNA Coverage: Compute the average rDNA coverage for each sample

Step 3: Compute estimated copy number: Divide the genome coverage ratio per sample by the average rDNA coverage per sample

Step 4: Normalize AF with estimated copy number for each sample
