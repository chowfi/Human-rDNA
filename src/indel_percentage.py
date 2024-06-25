import pandas as pd
import sys
sys.path.append('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/src/')
from individual_reference_genome import *

def merge_csv_files(directory):

    df_list = []
    

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):

            file_path = os.path.join(directory, filename)
            
            df = pd.read_csv(file_path)

            df_list.append(df)

    if df_list:
            
            combined_df = pd.concat(df_list, ignore_index=True)
            return combined_df
    else:
        return pd.DataFrame()

def main():

    file_path = "/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/scripts_outputs/unique_array_jobs_vcf_files.txt"

    success_ids = []
    failed_ids = []

    with open(file_path, 'r') as file:
        for individual_path in file:

            individual_path = individual_path.strip()  
            try:
                individual_df = read_vcf(individual_path)
                
                #deletion instances
                t = individual_df.shape[0]
                d = individual_df[(individual_df['REF'].str.len()) > (individual_df['ALT'].str.len())].shape
                d = d[0]
                d_percentage = d / t * 100

                #insertion instances
                i = individual_df[(individual_df['REF'].str.len()) < (individual_df['ALT'].str.len())].shape
                i = i[0]
                i_percentage = i / t * 100

                #snp instances
                snp = individual_df[(individual_df['REF'].str.len()) == (individual_df['ALT'].str.len())].shape
                snp = snp[0]
                snp_percentage = snp / t * 100

                assert round(d_percentage + i_percentage + snp_percentage, 2) == 100.00

                file_split = individual_path.split('/')
                id_value = file_split[-2]  

                rows = []

                new_row = {
                'id': id_value,
                'total rows': t,
                'deletion instances': d,
                'deletion percentage': d_percentage,
                'insertion instances': i,
                'insertion percentage': i_percentage,
                'snp instances': snp,
                'snp percentage': snp_percentage,
                }

                rows.append(new_row)

                new_df = pd.DataFrame(rows)
                
                output_dir = '/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/src_outputs/indels_stats'
                os.chdir(output_dir)

                new_df.to_csv(f'indelstats_{id_value}.csv', index=False)
                success_ids.append(id_value)

            except Exception as e:
                print(f'Failed to process {id_value}: {str(e)}')
                failed_ids.append(id_value)

    with open('successful_ids.txt', 'w') as f:
        for id in success_ids:
            f.write(f'{id}\n')

    with open('failed_ids.txt', 'w') as f:
        for id in failed_ids:
            f.write(f'{id}\n')

    print(f'Processing individuals complete. Check successful_ids.txt and failed_ids.txt for details.')
    print(f'Aggregating individual files to obtain insertion, deletion and snp percentages...')

    directory = '/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/src_outputs/indels_stats'

    combined_df = merge_csv_files(directory)

    # Calculate the average for insertion/deletion/snp percentages
    avg_deletion_percentage = combined_df['deletion percentage'].mean()
    avg_insertion_percentage = combined_df['insertion percentage'].mean()
    avg_snp_percentage = combined_df['snp percentage'].mean()

    print(f'Average Deletion Percentage: {avg_deletion_percentage:.2f}%')
    print(f'Average Insertion Percentage: {avg_insertion_percentage:.2f}%')
    print(f'Average SNP Percentage: {avg_snp_percentage:.2f}%')

if __name__ == "__main__":
    main()