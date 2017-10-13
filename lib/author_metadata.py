import csv


def read_author_metadata_csv(authors_csv):
    authors_metadata = {}
    with open(authors_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            name = row['name']
            authors_metadata[name] = {
                'name': row['name'],
                'nationality': row['nationality'],
                'political_views': row['political_views'],
                'religion': row['religion'],
                'notes': row['notes'],
                'profession': row['profession'],
                'description_original': row['description_original'],
                'link': row['odnb_link'],
            }
    return authors_metadata
