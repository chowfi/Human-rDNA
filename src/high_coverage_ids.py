import re
import csv

def main():
    file_path = '/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/original reference/1000data.csv'

    matching_entries = []

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r',(ERR\w*)', line)
            if match:  
                matching_entries.append(match.group(1)) 

    print("Found matches:", matching_entries)
    print("Number of matches:", len(matching_entries))

    with open('/Users/fionachow/Documents/NYU/CDS/Summer 2024/Human rDNA Research/Project/Human-rDNA/outputs/high_coverage_ids.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['High Coverage Entries'])
        # Write each match on a new line
        for match in matching_entries:
            csvwriter.writerow([match])
            
if __name__ == "__main__":
    main()