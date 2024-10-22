log_file="/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/scripts_outputs/coverage_files_error.txt"

grep "No such file or directory" "$log_file" | grep -oE "ERR[0-9]+" | sort | uniq > missing_coverage_ids.txt

count=$(wc -l < missing_coverage_ids.txt)

echo "$count missing ERR IDs have been extracted to missing_coverage_ids.txt"
