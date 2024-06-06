import re

# Path to your CSV file
file_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/1000data.csv'

# This will hold all matches
matching_entries = []

with open(file_path, 'r') as file:
    for line in file:
        matches = re.findall(r',(ERR\w*)', line)
        matching_entries.extend(matches)
