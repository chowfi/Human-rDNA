
import pandas as pd
import sys
import os
sys.path.append('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/src/')
from individual_reference_genome import *

def merge_dfs(og_ref, individual_df, new_ref):
    """
    Merge the three dfs into one to show columns: POS, og_ref, REF_vcf, AF_old, ALT_old, new_ref
    """
    individual_df['AF'] = individual_df['INFO'].apply(extract_af)
    individual_df = individual_df[['POS', 'REF', 'ALT', 'AF']]  
    merged_df = pd.merge(og_ref, individual_df, on='POS', how='left', suffixes=('_og', '_vcf'))
    merged_df.rename(columns={'REF_og':'ALT_og', 'ALT':'ALT_vcf'}, inplace=True)

    merged_df = pd.merge(merged_df, new_ref, on='POS', how='left')
    merged_df.drop(columns=['Unnamed: 0'], inplace=True)
    merged_df.rename(columns={'1000_genome_new_ref': 'new_ref'}, inplace=True)

    return merged_df

def update_dfs(merged_df):
    """
    1) Get full sequence of individual
    2) Get ALT_new and AF_new if there is a different base reference at each position
    """
    #Combine the ALT_og column and ALT_vcf into ALT_combined, and set AF to 0 where variant did not exist
    merged_df['ALT_combined'] = merged_df.apply(lambda x: x['ALT_vcf'] if pd.notna(x['ALT_vcf']) else x['ALT_og'], axis=1)
    merged_df['AF'] = merged_df['AF'].fillna(0) 
    merged_df.drop(columns=['ALT_vcf','Type'], inplace=True)
    merged_df.rename(columns={'ALT_og': 'og_ref', 'AF':'AF_old', 'ALT_combined':'ALT_old'}, inplace=True)

    #using ALT_old unless reference changed and AF_old != 0
    merged_df['ALT_new'] = merged_df.apply(lambda x: x['og_ref'] if (x['AF_old'] != 0) and (x['og_ref'] != x['new_ref']) else x['ALT_old'], axis=1)

    #using AF_old unless reference changed 
    merged_df['AF_new'] = merged_df.apply(lambda x: 1 - float(x['AF_old']) if (x['og_ref'] != x['new_ref']) else float(x['AF_old']), axis=1) #note: 'AF_new' is all in float, 'AF_old' was in string and 0 was integer

    return merged_df

def deletions_insertions(merged_df, individual_df):
    """
    1) Deal with deletions by creating a new dataframe new_df so that it expands each deletion event into separate rows
    2) Deal with insertions with duplicate rows
    """
    #Adjust for first row of every deletion event
    merged_df['AF_new'] = merged_df.apply(lambda x: 0 if (x['new_ref'] == x['ALT_new']) else x['AF_new'], axis=1)
    
    merged_df['AF_old'] = pd.to_numeric(merged_df['AF_old'], errors='raise')

    copy_del_df = merged_df[merged_df['REF_vcf'].str.len() > 1].copy()

    #Calculate additional length add_len for each record
    copy_del_df['add_len'] = copy_del_df['REF_vcf'].str.len() - 1
    #Calculate inverse allele frequency inv_AF for each record
    copy_del_df['inv_AF'] = 1 - copy_del_df['AF_old']

    rows = []

    for _, row in copy_del_df.iterrows():
        for i in range(1, row['add_len'] + 1):
            new_row = {
                'scenario': '>0.5' if row['AF_old'] > 0.5 else '<=0.5',
                'POS': row['POS'] + i,
                'add_len': row['add_len'],
                'AF': row['AF_old'],
                'inv_AF': row['inv_AF'],
            }
            rows.append(new_row)

    new_df = pd.DataFrame(rows)

    merged_updated_df = pd.merge(merged_df, new_df[['scenario', 'POS', 'AF', 'inv_AF']], on='POS', how='left')

    #Update AF_new based on new_ref and inv_AF
    merged_updated_df.loc[merged_updated_df['new_ref'] == '0', 'AF_new'] = merged_updated_df['inv_AF']
    #Update ALT_new based on inv_AF and new_ref
    merged_updated_df['ALT_new'] = merged_updated_df.apply(lambda x: '0' if pd.notna(x['inv_AF']) and x['new_ref']!='0' else x['ALT_new'], axis=1)
    #Update AF_new based on inv_AF and ALT_new
    merged_updated_df['AF_new'] = merged_updated_df.apply(lambda x: x['AF'] if pd.notna(x['inv_AF']) and x['ALT_new']=='0' else x['AF_new'], axis=1)

    #dealing with insertions with duplicate rows here
    temp = individual_df[(individual_df['REF'].str.len()) < (individual_df['ALT'].str.len())]
    duplicates = temp.duplicated(subset='POS', keep=False)
    duplicate_rows = temp[duplicates]
    duplicate_rows['Duplicate'] = 'Y'
    duplicate_rows = duplicate_rows[['POS','Duplicate']]
    unique_rows = duplicate_rows.drop_duplicates()

    #if insertion w duplicate rows in original vcf, and new_ref != ALT_old, then make ALT_new = ALT_old
    #Motivation: otherwise there would be two identical rows but w different AF which would not make sense
    merged_updated_df = pd.merge(merged_updated_df, unique_rows, on='POS', how='left')
    #if Duplicate is not missing and new_ref != ALT_old
    merged_updated_df['ALT_new'] = merged_updated_df.apply(lambda x: x['ALT_old'] if pd.notna(x['Duplicate']) and x['new_ref']!=x['ALT_old'] else x['ALT_new'] , axis=1)
    merged_updated_df['AF_new'] = merged_updated_df.apply(lambda x: x['AF_old'] if pd.notna(x['Duplicate']) and x['new_ref']!=x['ALT_old'] else x['AF_new'] , axis=1)

    merged_updated_df.drop(columns=['scenario','AF', 'inv_AF'], inplace=True)

    return merged_updated_df

def get_snp_df(merged_updated_df):
    """
    Isolate SNPs only
    """
    snp = ['C', 'A', 'G', 'T']

    snp_df = merged_updated_df[
    (merged_updated_df['new_ref'].isin(snp)) &
    (merged_updated_df['ALT_new'].isin(snp)) &
    ((merged_updated_df['REF_vcf'].isna()) | (merged_updated_df['REF_vcf'].str.len() == 1))
]
    
    snp_df.drop(columns=['Duplicate','REF_vcf', 'og_ref', 'AF_old', 'ALT_old'], inplace=True)

    snp_df = snp_df[snp_df['AF_new']!=0]

    return snp_df

def main():
    file_path = "/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/scripts_outputs/vcf_files_all.txt"
    og_ref = pd.read_csv('/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/src_outputs/og_ref.csv')
    new_ref = pd.read_csv('/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/src_outputs/1000_genome_new_ref/1000_genome_new_ref_v3.csv')

    success_ids = []
    failed_ids = []

    output_dir = '/scratch/cgsb/hochwagen/Human_rDNA_project/Human-rDNA/outputs/src_outputs/new_vcf'
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r') as file:
        for individual_path in file:

            individual_path = individual_path.strip()  
            file_split = individual_path.split('/')
            id_value = file_split[-2]  
            output_file_path = os.path.join(output_dir, f'new_vcf_{id_value}.csv')

            if os.path.exists(output_file_path):
                print(f'{output_file_path} already exists, skipping...')
                success_ids.append(id_value)
                continue

            try:
                individual_df = read_vcf(individual_path)
                merged_df = merge_dfs(og_ref, individual_df, new_ref)
                merged_df = update_dfs(merged_df)
                merged_updated_df = deletions_insertions(merged_df, individual_df)
                snp_df = get_snp_df(merged_updated_df)

                snp_df.to_csv(output_file_path, index=False)
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

    print(f'Processing complete. Check successful_ids.txt and failed_ids.txt for details.')

    # og_ref = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/og_ref.csv')
    # new_ref = new_ref = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/1000_genome_new_ref/1000_genome_new_ref_v2.csv')
    # individual_path = '/Users/fionachow/Documents/NYU/CDS/Spring 2024/Research Fair/Hochwagen/Individual Data/ERR3240115/ERR3240115_rDNA.vcf'
    # snp_check = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/notebooks/snp_df_test.csv')

    # individual_df = read_vcf(individual_path)
    # merged_df = merge_dfs(og_ref, individual_df, new_ref)
    # merged_df = update_dfs(merged_df)
    # merged_updated_df = deletions_insertions(merged_df, individual_df)
    # snp_df = get_snp_df(merged_updated_df)

    # assert snp_check['POS'].equals(snp_df['POS']) and snp_check['new_ref'].equals(snp_df['new_ref']) and snp_check['ALT_new'].equals(snp_df['ALT_new']) and snp_check['AF_new'].equals(snp_df['AF_new'])

    
if __name__ == "__main__":
    main()