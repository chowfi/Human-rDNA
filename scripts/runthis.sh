#!/bin/bash

USER="fc1132"
HPC_HOST="greene.hpc.nyu.edu"
TXT_FILE="/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/scripts_outputs/vcf_files_all.txt"
LOCAL_DIR="/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/original_vcf_all"

# Check if the TXT_FILE exists
if [ ! -f $TXT_FILE ]; then
    echo "File $TXT_FILE does not exist."
    exit 1
fi

# Read each line from the TXT_FILE and use scp to download the files
while IFS= read -r file_path; do
    scp "${USER}@${HPC_HOST}:${file_path}" "${LOCAL_DIR}"
done < "$TXT_FILE"



