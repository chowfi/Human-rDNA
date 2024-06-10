grep -E '/array_jobs/' vcf_files.txt | grep -v '/array_jobs_old/' | awk -F/ '{print $(NF-1),$0}' | sort -u -k1,1 | cut -d' ' -f2- > unique_array_jobs_vcf_files.txt

