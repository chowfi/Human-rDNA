import pandas as pd
import os
import glob

vcf_folder_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/original_vcf_all'
filtered_pop_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/others/1000data - Filtered Pop.csv'

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

        header_lines = [line for line in lines if line.startswith('#')]
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

        updated_data_lines = []
        for _, row in df.iterrows():
            updated_line = (
                f"{row['CHROM']}\t{row['POS']}\t{row['ID']}\t{row['REF']}\t{row['ALT']}\t"
                f"{row['QUAL']}\t{row['FILTER']}\t{row['AF']}\t{row['estimated copy number']}\t{row['normalized AF']}"
            )
            updated_data_lines.append(updated_line)

        with open(file_path, 'w') as file:
            file.writelines(header_lines)
            file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tAF\testimated_copy_number\tnormalized_AF\n")
            file.write("\n".join(updated_data_lines) + "\n")
    else:
    
        skipped_files.append(run_key)


if skipped_files:
    skipped_df = pd.DataFrame(skipped_files, columns=['Run'])
    skipped_df.to_csv(os.path.join(vcf_folder_path, 'skipped_files.csv'), index=False)

print("Process completed. Skipped files saved to 'skipped_files.csv' if any.")
