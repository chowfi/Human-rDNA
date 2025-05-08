#!/bin/bash

USER="fc1132"
HPC_HOST="greene.hpc.nyu.edu"
TXT_FILE="/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/scripts_outputs/vcf_files_fix.txt"
LOCAL_DIR="/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/original_vcf_fix"

if [ ! -f "$TXT_FILE" ]; then
    echo "File $TXT_FILE does not exist on the local system."
    exit 1
fi

while IFS= read -r file_path; do
    scp "${USER}@${HPC_HOST}:${file_path}" "${LOCAL_DIR}"
done < "$TXT_FILE"

echo "File transfer completed."




