import csv


# not used anymore. delete?
# def read_docid_asciimap_csv(csvfile_location):
#     docids_ascii = {}
#     with open(csvfile_location, 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         next(csvreader, None)
#         for row in csvreader:
#             docid = row[0]
#             is_ascii = not bool(int(row[1]))
#             docids_ascii[docid] = is_ascii
#     return docids_ascii
