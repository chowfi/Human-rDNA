import os
import pandas as pd

directory_path = "/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/original_coverage_all"

output_file_path = "/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/avg_rDNA_coverage.txt"

results = []

for filename in os.listdir(directory_path):
    if filename.endswith("_rDNA_coverage.txt"):
        file_path = os.path.join(directory_path, filename)

        df = pd.read_csv(file_path, sep='\t', header=None, names=["Human", "Column2", "Coverage"])

        mean_coverage = df["Coverage"].mean()

        run_id = filename.split('_')[0]

        results.append({"run": run_id, "avg": mean_coverage})

results_df = pd.DataFrame(results)
results_df.to_csv(output_file_path, sep='\t', index=False)
