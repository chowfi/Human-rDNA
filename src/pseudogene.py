import pandas as pd

pg = pd.read_csv('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/from_jon/pseudogenecandi.csv')

# Extract pseudogene candidates into format
pg_positions = [[row['Start'], row['End'], 'pseudogene candidate'] for _, row in pg.iterrows()]

# all_positions = [
#     [1, 3656, "5'ETS"],
#     [3657, 5527, '18S'],
#     [5528, 6622, 'ITS1'],
#     [6623, 6779, '5.8S'],
#     [6780, 7934, 'ITS2'],
#     [7935, 12969, '28S'],
#     [12970, 13314, "3'ETS"]
# ]

# Combine with existing all_positions list of lists
# all_positions.extend(pg_positions)

# print(all_positions)
# print(len(all_positions))

df = pd.DataFrame(pg_positions, columns=['Start', 'End', 'Segment'])
df.to_csv('pg_positions.csv', index=False)