import pandas as pd
import os
import glob

vcf_folder_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/original_vcf_all'
filtered_pop_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/others/1000data - Filtered Pop.csv'
output_folder_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/modified_original_reference/'

os.makedirs(output_folder_path, exist_ok=True)

copy_number_df = pd.read_csv(filtered_pop_path)
copy_number_dict = dict(zip(copy_number_df['Run'], copy_number_df['Estimated Copy #']))

skipped_files = []

for file_path in glob.glob(os.path.join(vcf_folder_path, 'ERR*_rDNA.vcf')):
    file_name = os.path.basename(file_path)
    run_key = file_name.split('_')[0]

    if run_key in copy_number_dict:
        estimated_copy_number = copy_number_dict[run_key]

        with open(file_path, 'r') as file:
            lines = file.readlines()

        data_lines = [line for line in lines if not line.startswith('#')]

        data = []
        for line in data_lines:
            parts = line.strip().split('\t')
            info_dict = dict(item.split('=') for item in parts[7].split(';') if '=' in item)
            af_value = float(info_dict.get('AF', 0))
            data.append(parts[:7] + [af_value])

        df = pd.DataFrame(data, columns=['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'AF'])
        df['estimated copy number'] = estimated_copy_number
        df['normalized AF'] = df['AF'] * estimated_copy_number

        updated_data_lines = [
            f"{row['CHROM']}\t{row['POS']}\t{row['ID']}\t{row['REF']}\t{row['ALT']}\t"
            f"{row['QUAL']}\t{row['FILTER']}\t{row['AF']}\t{row['estimated copy number']}\t{row['normalized AF']}"
            for _, row in df.iterrows()
        ]

        output_file_path = os.path.join(output_folder_path, file_name)

        with open(output_file_path, 'w') as file:
            file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tAF\testimated_copy_number\tnormalized_AF\n")
            file.write("\n".join(updated_data_lines) + "\n")
    else:
        skipped_files.append(run_key)

if skipped_files:
    skipped_df = pd.DataFrame(skipped_files, columns=['Run'])
    skipped_df.to_csv(os.path.join(output_folder_path, 'skipped_files.csv'), index=False)

print("Process completed. Modified files saved in the output directory.")
