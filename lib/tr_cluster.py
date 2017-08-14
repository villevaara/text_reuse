
import csv


class TextReuseCluster(object):

    def __init__(self, cluster_id, fragment_list):
        self.cluster_id = cluster_id
        self.fragment_list = fragment_list
        self.fragment_list.sort(key=lambda x: x.year, reverse=False)
        self.group_name = None
        self.group_id = None

    def set_fragment_list(self, fragment_list):
        fragment_list.sort(key=lambda x: x.year, reverse=False)
        self.fragment_list = fragment_list

    def set_cluster_group(self, group_name, group_id):
        self.group_name = group_name
        self.group_id = group_id

    def get_first_year(self):
        first_year = self.fragment_list[0].year
        return first_year

    def get_last_year(self):
        last_year = self.fragment_list[len(self.fragment_list) - 1].year
        return last_year

    def get_length(self):
        length = len(self.fragment_list)
        return length

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

    def get_fragments_filter_out_document_id(self, document_id):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.document_id != document_id:
                retlist.append(fragment)
        return retlist

    def get_fragments_filter_out_year_below(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.year >= year:
                retlist.append(fragment)
        return retlist

    def get_fragments_filter_out_year_above(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.year <= year:
                retlist.append(fragment)
        return retlist

    def get_number_of_authors(self):
        authors = set()
        for fragment in self.fragment_list:
            authors.add(fragment.author)
        return len(authors)

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
                                    'text_before', 'text', 'text_after',
                                    'preceding_header_index',
                                    'start_index', 'end_index',
                                    'find_start_index', 'find_end_index',
                                    'document_length', 'fragment_indices',
                                    'document_collection',
                                    'group_name', 'group_id'])
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
                                    fragment.document_length,
                                    fragment.fragment_indices,
                                    fragment.document_collection,
                                    self.group_name,
                                    self.group_id])
