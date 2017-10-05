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


# book_index = 0
for filename in filenames:
    book_index = filename.split('/')[0]
    add_filename_to_totals(outfilename, filename, book_index)
