import csv
import sys


class TextReuseCluster(object):

    def __init__(self, document_id, cluster_id, fragment_list):
        self.document_id = document_id
        self.cluster_id = cluster_id
        self.fragment_list = fragment_list
        self.fragment_list.sort(key=lambda x: x.year, reverse=False)
        self.group_name = None
        self.group_id = None
        self.group_start_index = None
        self.group_end_index = None

    def set_fragment_list(self, fragment_list):
        fragment_list.sort(key=lambda x: x.year, reverse=False)
        self.fragment_list = fragment_list

    def set_cluster_group(self, group_name, group_id):
        self.group_name = group_name
        self.group_id = group_id

    def get_fragment_seed_uids(self):
        fragment_seed_uids = set()
        for fragment in self.fragment_list:
            fragment_seed_uids.add(fragment.seed_uid)
        return fragment_seed_uids

    def filter_non_unique_seed_uids(self, used_seed_uids):
        new_fragment_list = []
        # print("old fragment list lenght: " + str(len(self.fragment_list)))
        for fragment in self.fragment_list:
            if fragment.seed_uid in used_seed_uids:
                continue
            else:
                new_fragment_list.append(fragment)
                used_seed_uids.add(fragment.seed_uid)
        self.fragment_list = new_fragment_list
        # print("new fragment list lenght: " + str(len(self.fragment_list)))
        return used_seed_uids

    def get_first_year(self):
        first_year = self.fragment_list[0].year
        return first_year

    def get_last_year(self):
        last_year = self.fragment_list[len(self.fragment_list) - 1].year
        return last_year

    def get_years(self):
        all_years = []
        for fragment in self.fragment_list:
            all_years.append(fragment.year)
        return all_years

    def get_length(self):
        length = len(self.fragment_list)
        return length

    def get_orig_author(self):
        for fragment in self.fragment_list:
            if fragment.ecco_id == self.document_id:
                return fragment.author
        return None

    def orig_author_first(self):
        orig_author = self.get_orig_author()
        first_year = self.get_first_year()
        first_year_fragments = (
            self.get_fragments_filter_out_year_above(first_year))
        first_year_authors = set()
        for fragment in first_year_fragments:
            first_year_authors.add(fragment.author)
        if orig_author in first_year_authors:
            return True
        else:
            return False

    def get_fragments_filter_out_author(self, author, ignore_id=""):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.author != author:
                retlist.append(fragment)
        if (ignore_id != "") and (len(retlist) > 0):
            for fragment in self.fragment_list:
                if str(fragment.ecco_id) == str(ignore_id):
                    retlist.append(fragment)
        return retlist

    def get_fragments_with_author(self, author):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.author == author:
                retlist.append(fragment)
        return retlist

    def filter_out_author(self, author, ignore_id=""):
        self.fragment_list = (
            self.get_fragments_filter_out_author(author, ignore_id))

    def get_fragments_filter_out_document_id(self, document_id):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.document_id != document_id:
                retlist.append(fragment)
        return retlist

    def get_fragments_filter_out_year_below(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if int(fragment.year) >= int(year):
                retlist.append(fragment)
        return retlist

    def filter_out_year_below(self, year):
        self.fragment_list = (
            self.get_fragments_filter_out_year_below(year))

    def get_lowest_first_ed_year_guess(self):
        first_ed_years = []
        for fragment in self.fragment_list:
            first_ed_years.append(fragment.first_ed_year_guess)
        if len(first_ed_years) > 0:
            first_year = min(first_ed_years)
        else:
            first_year = -1
        return first_year

    def get_fragments_filter_out_firts_ed_year_not(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if int(fragment.first_ed_year_guess) == int(year):
                retlist.append(fragment)
        return retlist

    def filter_only_one_book_per_author(self):
        authors_included = set()
        retlist = []
        for fragment in self.fragment_list:
            if fragment.author in authors_included:
                continue
            else:
                retlist.append(fragment)
                authors_included.add(fragment.author)
        self.fragment_list = retlist

    def filter_out_firts_ed_year_not(self, year):
        self.fragment_list = (
            self.get_fragments_filter_out_firts_ed_year_not(year))

    def get_fragments_filter_out_year_above(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if int(fragment.year) <= int(year):
                retlist.append(fragment)
        return retlist

    def filter_out_year_above(self, year):
        self.fragment_list = (
            self.get_fragments_filter_out_year_above(year))

    def get_authors(self):
        authors = set()
        for fragment in self.fragment_list:
            authors.add(fragment.author)
        return authors

    def get_number_of_authors(self):
        authors = self.get_authors()
        return len(authors)

    def get_titles(self):
        titles = set()
        for fragment in self.fragment_list:
            titles.add(fragment.title)
        return titles

    def add_cluster_groups(self):
        for fragment in self.fragment_list:
            # Find "seed" document, add metadata
            if str(fragment.ecco_id) == self.document_id:
                self.group_name = fragment.preceding_header
                self.group_id = fragment.preceding_header_index
                if fragment.octavo_start_index is None:
                    sys.exit("No octavo start index!")
                self.group_start_index = fragment.octavo_start_index
                self.group_end_index = fragment.octavo_end_index
                break
        for fragment in self.fragment_list:
            fragment.set_seed_data(
                seed_data={
                    'seed_document_id': self.document_id,
                    'seed_header_id': self.group_id,
                    'seed_header_text': self.group_name,
                    'seed_header_start_index': self.group_start_index,
                    'seed_header_end_index': self.group_end_index,
                })

    def write_cluster_csv(self, outfilepath, include_header_row=True,
                          method='w'):
        if method == 'w':
            outfile = (outfilepath + "cluster_" +
                       str(self.cluster_id) + ".csv")
        else:
            outfile = outfilepath
        with open(outfile, method) as output_file:
            csvwriter = csv.writer(output_file)
            if include_header_row:
                csvwriter.writerow(['cluster_id',
                                    'ecco_id',
                                    'estc_id',
                                    'author',
                                    'title',
                                    'preceding_header',
                                    'year',
                                    'location',
                                    'text_before',
                                    'text',
                                    'text_after',
                                    'preceding_header_index',
                                    'start_index',
                                    'end_index',
                                    'find_start_index',
                                    'find_end_index',
                                    'octavo_start_index',
                                    'octavo_end_index',
                                    'document_length',
                                    'document_collection',
                                    'group_name',
                                    'group_id',
                                    'group_start_index',
                                    'group_end_index'])
            for fragment in self.fragment_list:
                csvwriter.writerow([fragment.cluster_id,
                                    fragment.ecco_id,
                                    fragment.estc_id,
                                    fragment.author,
                                    fragment.title,
                                    fragment.preceding_header,
                                    fragment.year,
                                    fragment.location,
                                    fragment.text_before,
                                    fragment.text,
                                    fragment.text_after,
                                    fragment.preceding_header_index,
                                    fragment.start_index,
                                    fragment.end_index,
                                    fragment.find_start_index,
                                    fragment.find_end_index,
                                    fragment.octavo_start_index,
                                    fragment.octavo_end_index,
                                    fragment.document_length,
                                    fragment.document_collection,
                                    self.group_name,
                                    self.group_id,
                                    self.group_start_index,
                                    self.group_end_index])
