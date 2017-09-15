from bisect import bisect_left

from lib.headerdata import (
    get_header_and_index_for_textindex,
    )

from lib.text_reuse_common import (
    get_location_from_estc,
    get_author_from_estc,
    get_year_from_estc,
    get_estcid_from_estc,
    get_title_from_estc,
    )


class TextReuseFragment(object):

    def __init__(self, ecco_id, cluster_id,
                 text, start_index, end_index):
        self.estc_id = None
        self.ecco_id = ecco_id
        self.cluster_id = cluster_id
        self.title = None
        self.author = None
        self.year = None
        self.text = text
        self.location = None
        self.start_index = start_index
        self.end_index = end_index
        self.find_start_index = -1
        self.find_end_index = -1
        self.octavo_start_index = None
        self.octavo_end_index = None
        self.text_before = None
        self.text_after = None
        self.document_length = None
        self.preceding_header = None
        self.preceding_header_index = -1
        # self.fragment_indices = None
        self.document_collection = None
        self.is_ascii = None

    def add_metadata(self, good_metadata):
        self.location = get_location_from_estc(
            self.ecco_id, good_metadata)
        self.author = get_author_from_estc(
            self.ecco_id, good_metadata)
        self.estc_id = get_estcid_from_estc(
            self.ecco_id, good_metadata)
        self.year = get_year_from_estc(
            self.ecco_id, good_metadata)
        self.title = get_title_from_estc(
            self.ecco_id, good_metadata)

    def add_headerdata(self, headerdata):
        if self.octavo_start_index is not None:
            header_search_index = self.octavo_start_index
        elif self.find_start_index != -1:
            header_search_index = self.find_start_index
        else:
            header_search_index = self.start_index
        header_ti = get_header_and_index_for_textindex(
            header_search_index, headerdata)
        self.preceding_header = header_ti.get('text')
        self.preceding_header_index = header_ti.get('index')

    def __context_search(self, search_text, document_text_data, ascii_search):
        if ascii_search:
            document_text = document_text_data.get('splitjoined_ascii')
        else:
            document_text = document_text_data.get('splitjoined_unicode')
        # document_text_stripped = ' '.join(document_text.split())
        fragment_start_index = document_text.find(search_text)
        return fragment_start_index

    def set_fragment_encoding(self, document_text_data):

        document_collection = document_text_data.get('collection')

        if document_collection == "ecco1":
            ascii_search = True
        else:
            ascii_search = False

        retried = False

        while True:
            fragment_start_index = self.__context_search(self.text,
                                                         document_text_data,
                                                         ascii_search)

            if fragment_start_index != -1:
                self.find_start_index = fragment_start_index
                self.find_end_index = (fragment_start_index +
                                       len(self.text))
                if ascii_search:
                    self.is_ascii = True
                else:
                    self.is_ascii = False
                return self.is_ascii
            elif (fragment_start_index == -1) and (retried is True):
                print(" > !! Fragment still not found." +
                      " No encoding set.")
                return None
            elif (fragment_start_index == -1) and (retried is False):
                print(" > docid: " + str(self.ecco_id) +
                      " cluid: " + str(self.cluster_id) +
                      " Fragment not found." +
                      " Trying the other method (ascii/unicode)")
                ascii_search = not ascii_search
                retried = True

    def find_octavo_index(self, index, octavo_indexmap):
        fragment_indices = octavo_indexmap.get('fragment_index')
        chars_lost = octavo_indexmap.get('chars_lost')

        index_find_pos = bisect_left(fragment_indices, index)

        # if fragment index is the last index
        if index_find_pos == len(fragment_indices):
            return index + chars_lost[index_find_pos - 1]
        # if index found is before first addition
        if index_find_pos == 0 and fragment_indices[index_find_pos] > index:
            return index
        if fragment_indices[index_find_pos] == index:
            return index + chars_lost[index_find_pos]
        if fragment_indices[index_find_pos] > index:
            return index + chars_lost[index_find_pos - 1]

        print("Index not found! WTF.")
        return -1

    def set_octavo_indices(self, octavo_indexmap, orig_index=True):
        if orig_index:
            start_i = self.start_index
            end_i = self.end_index
        else:
            start_i = self.find_start_index
            end_i = self.find_end_index
        self.octavo_start_index = (
            self.find_octavo_index(start_i, octavo_indexmap))
        self.octavo_end_index = (
            self.find_octavo_index(end_i, octavo_indexmap))
