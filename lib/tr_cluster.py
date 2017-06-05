# get metadatalist of clusters:
# chronologically first fragment in cluster,
# cluster first year,
# cluster last year,
# cluster document_ids,
# cluster_years ?
# cluster first document_id
# cluster length
# books in cluster not original id / by original author


class TextReuseCluster(object):

    def __init__(self, cluster_id, fragment_list):
        self.cluster_id = cluster_id
        self.fragment_list = fragment_list
        self.fragment_list.sort(key=lambda x: x.year, reverse=False)

    def set_fragment_list(self, fragment_list):
        fragment_list.sort(key=lambda x: x.year, reverse=False)
        self.fragment_list = fragment_list

    def get_first_year(self):
        first_year = self.fragment_list[0].year
        return first_year

    def get_last_year(self):
        last_year = self.fragment_list[len(self.fragment_list) - 1].year
        return last_year

    def get_length(self):
        length = len(self.fragment_list)
        return length

    def filter_out_author(self, author):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.author != author:
                retlist.append(fragment)
        self.fragment_list = retlist

    def filter_out_document_id(self, document_id):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.document_id != document_id:
                retlist.append(fragment)
        self.fragment_list = retlist

    def filter_out_year_below(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.year >= year:
                retlist.append(fragment)
        self.fragment_list = retlist

    def filter_out_year_above(self, year):
        retlist = []
        for fragment in self.fragment_list:
            if fragment.year <= year:
                retlist.append(fragment)
        self.fragment_list = retlist
