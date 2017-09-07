import json
import csv

with open('data/ecco2ids.json') as json_file:
    json_data = json.load(json_file)

results = json_data.get('results').get('docs')

with open('data/ecco2_ids.csv', 'w') as output_file:
    csvwriter = csv.writer(output_file)
    for result in results:
        csvwriter.writerow([result.get('documentID')])
