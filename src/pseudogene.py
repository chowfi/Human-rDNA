import pandas as pd

pg = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/from_jon/pseudogenecandi-2.csv')

# Extract pseudogene candidates into format
pg_positions = [[row['Start'], row['End'], row['Ref'], row['Alt'], 'pseudogene candidate'] for _, row in pg.iterrows()]

df = pd.DataFrame(pg_positions, columns=['Start', 'End', 'Ref', 'Alt', 'Segment'])
df.to_csv('pg_positions_2.csv', index=False)
