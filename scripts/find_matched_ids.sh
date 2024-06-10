grep -Fxf vcf_ids.txt <(tail -n +2 high_coverage_ids.csv) > matched_ids.txt

