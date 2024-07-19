import pandas as pd

new_ref = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/1000_genome_new_ref/1000_genome_new_ref_v3.csv')
new_ref = pd.DataFrame(new_ref)
new_ref = new_ref[new_ref['1000_genome_new_ref'] != '0']

# 1. Concatenate all values into a single string
new_ref_string = ''.join(new_ref['1000_genome_new_ref'].tolist())

output_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/1000_genome_new_ref/1000_genome_new_ref_v3_string.txt'
with open(output_path, 'w') as file:
    file.write(new_ref_string)

# 2. Create a new DataFrame with one letter per row and a running POS
with open(output_path, 'r') as file:
    new_ref_string = file.read().strip()

single_chars = list(new_ref_string)

new_data = []
pos = 1
for char in single_chars:
    if len(char) == 1:
        new_data.append({'POS': pos, 'REF': char})
        pos += 1
    elif len(char) > 1:
        for sub_char in char:
            new_data.append({'POS': pos, 'REF': sub_char})
            pos += 1

new_df = pd.DataFrame(new_data)

new_df.to_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/src_outputs/1000_genome_new_ref/1000_genome_new_ref_v3_reindex_df.csv', index=False, encoding='utf-8', line_terminator='\n')





