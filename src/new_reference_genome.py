import os
import pandas as pd
from functools import reduce

def merge_csv_files(directory):

    df_list = []
    

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):

            file_path = os.path.join(directory, filename)
            

            err_number = filename.split('_')[1].split('.')[0]  # Assumes format "reference_ERRXXXX.csv"
            
            df = pd.read_csv(file_path)
            

            if 'POS' in df.columns and 'REF' in df.columns:

                df = df[['POS', 'REF']]
                
                # Set the index to 'POS'
                df.set_index('POS', inplace=True)
                
                
                df.rename(columns={'REF': err_number}, inplace=True)
                
                
                df_list.append(df)
            else:
                print(f"No 'POS' or 'REF' column in {filename}")
        else:
            continue

    # Merge all dataframes on the index 'POS'
    if df_list:
        # Use reduce to merge all dataframes in the list on their index
        combined_df = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), df_list)
        
        return combined_df
    else:
        return pd.DataFrame()

def main():
    
    directory = "/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/indiv_ref_genome/v2_indels"

    combined_df = merge_csv_files(directory)

    if 'POS' in combined_df.index.names:
        combined_df.reset_index(inplace=True)

    # Calculate the mode for each position
    combined_df['1000_genome_new_ref'] = combined_df.mode(axis=1).iloc[:, 0]

    most_common_patterns = combined_df[['POS', '1000_genome_new_ref']]

    most_common_patterns.to_csv("1000_genome_new_ref_v2.csv")


if __name__ == "__main__":
    main()