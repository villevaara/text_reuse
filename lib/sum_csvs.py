import csv
from glob import glob
from lib.author_metadata import read_author_metadata_csv


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


def add_filename_to_totals(outfilename, filename,
                           book_index, documents_meta_dict):
    # document_length = documents_meta_dict[book_index].get('length')
    # document_sequence = documents_meta_dict[book_index].get('sequence')
    # document_description = documents_meta_dict[book_index].get('description')
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        total = 0
        for line in csvreader:
            total += int(line[6])
        outrow = [book_index, total,
                  documents_meta_dict[book_index].get('length'),
                  documents_meta_dict[book_index].get('description'),
                  documents_meta_dict[book_index].get('sequence')]
        with open(outfilename, 'a') as csvoutfile:
            csvwriter = csv.writer(csvoutfile, quoting=csv.QUOTE_ALL)
            csvwriter.writerow(outrow)


def create_csv_summaries(outputpath, documents_meta_dict):

    # def get_filenamesums(filename):
    current_subdirs = glob(outputpath + "*/")
    filenames = []

    for pathpart in current_subdirs:
        filenames.append(pathpart + "header_plotdata.csv")

    outfilename = outputpath + "volume_totals.csv"

    with open(outfilename, 'w') as csvoutfile:
        csvwriter = csv.writer(csvoutfile)
        csvwriter.writerow(['volume', 'fragments', 'length',
                            'description', 'sequence'])

    for filename in filenames:
        book_index = filename.split('/')[2]
        add_filename_to_totals(outfilename, filename,
                               book_index, documents_meta_dict)

    # get author totals
    author_metadata = read_author_metadata_csv(
        "../data-public/authors-metadata/misc/author_metadata.csv")
    author_filenames = []
    for pathpart in current_subdirs:
        author_filenames.append(pathpart + "fragments_per_author.csv")

    outfilename = outputpath + "author_totals.csv"

    author_totals = {}

    for filename in author_filenames:
        add_to_author_totals(author_totals, filename)

    with open(outfilename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['author', 'fragments', 'political_views', 'link'])
        for key, value in author_totals.items():
            if key in author_metadata.keys():
                author_politics = author_metadata.get(key).get(
                    'political_views')
                author_link = author_metadata.get(key).get('link')
            else:
                author_politics = "no_record"
                author_link = "no_record"
            csvwriter.writerow([key, value, author_politics, author_link])

    header_filenames = glob(outputpath + "*/*/*.csv")
    header_author_totals_outfile = (
        outputpath + "reuses_by_author_all_headers.csv")

    with open(header_author_totals_outfile, 'w') as csvout:
        csvwriter = csv.writer(csvout)
        csvwriter.writerow(['author', 'eccoid',
                            'header', 'header_index', 'fragments'])

    for filename in header_filenames:
        bookid = filename.split('/')[2]

        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            # next(csvreader, None)  # skip the headers
            author_totals = {}
            for row in csvreader:
                author = row.get('author')
                # title = row.get('title')
                group_name = row.get('group_name')
                group_id = row.get('group_id')
                if author not in author_totals.keys():
                    author_totals[author] = 1
                else:
                    author_totals[author] += 1

            with open(header_author_totals_outfile, 'a') as csvout:
                csvwriter = csv.writer(csvout)
                for key, value in author_totals.items():
                    csvwriter.writerow([key, bookid, group_name,
                                        group_id, value])

    # sum political views
    pol_filenames = []
    for pathpart in current_subdirs:
        pol_filenames.append(pathpart + "plotdata_politics_sum.csv")

    outfilename = outputpath + "politics_summary.csv"

    with open(outfilename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            'volume', 'whig', 'royalist', 'jacobite', 'parliamentarian',
            'tory', 'unionist', 'no_record',
            'whig_wide', 'tory_wide', 'others_wide'])

        for filename in pol_filenames:
            bookid = filename.split('/')[2]
            with open(filename, 'r') as readfile:
                csvreader = csv.DictReader(readfile)
                for row in csvreader:
                    csvwriter.writerow(
                        [bookid,
                         row.get('whig'),
                         row.get('royalist'),
                         row.get('jacobite'),
                         row.get('parliamentarian'),
                         row.get('tory'),
                         row.get('unionist'),
                         row.get('no_record'),
                         row.get('whig_wide'),
                         row.get('tory_wide'),
                         row.get('others_wide')])
