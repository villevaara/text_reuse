import csv
from glob import glob


current_subdirs = glob("*/")
filenames = []

for pathpart in current_subdirs:
    filenames.append(pathpart + "header_plotdata.csv")

outfilename = "volume_totals.csv"


# def get_filenamesums(filename):
def add_filename_to_totals(outfilename, filename, book_index):
    # book_index = 1
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        total = 0
        for line in csvreader:
            total += int(line[6])
        outrow = [book_index, total]
        with open(outfilename, 'a') as csvoutfile:
            csvwriter = csv.writer(csvoutfile)
            csvwriter.writerow(outrow)


for filename in filenames:
    book_index = filename.split('/')[0]
    add_filename_to_totals(outfilename, filename, book_index)


# book_index = 0
def add_to_author_totals(author_totals, filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        # file_authors = {}
        for line in csvreader:
            if line[0] not in author_totals.keys():
                author_totals[line[0]] = int(line[1])
            else:
                author_totals[line[0]] = (
                    author_totals[line[0]] + int(line[1]))


author_filenames = []
for pathpart in current_subdirs:
    author_filenames.append(pathpart + "fragments_per_author.csv")

outfilename = "author_totals.csv"

author_totals = {}

for filename in author_filenames:
    add_to_author_totals(author_totals, filename)

with open(outfilename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['author', 'fragments'])
    for key, value in author_totals.items():
        csvwriter.writerow([key, value])


header_filenames = glob("*/*/*.csv")
header_author_totals_outfile = "reuses_by_author_all_headers.csv"
with open(header_author_totals_outfile, 'w') as csvout:
    csvwriter = csv.writer(csvout)
    csvwriter.writerow(['author', 'eccoid',
                        'header', 'header_index', 'fragments'])

for filename in header_filenames:
    bookid = filename.split('/')[0]

    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # next(csvreader, None)  # skip the headers
        author_totals = {}
        for row in csvreader:
            author = row.get('author')
            title = row.get('title')
            group_name = row.get('group_name')
            group_id = row.get('group_id')
            if author not in author_totals.keys():
                author_totals[author] = 1
            else:
                author_totals[author] += 1

        with open(header_author_totals_outfile, 'a') as csvout:
            csvwriter = csv.writer(csvout)
            for key, value in author_totals.items():
                csvwriter.writerow([key, bookid, group_name, group_id, value])
