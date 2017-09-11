import re
from bisect import bisect_left

from lib.headerdata import (
    # get_text_for_document_id_from_api,
    # get_headers_from_document_text,
    get_header_and_index_for_textindex,
    )

from lib.text_reuse_common import (
    get_location_from_estc,
    get_author_from_estc,
    get_year_from_estc,
    get_estcid_from_estc,
    get_title_from_estc,
    )

# from lib.octavo_api_client import (
#     OctavoEccoClient)


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
        self.text_before = None
        self.text_after = None
        self.find_start_index = -1
        self.find_end_index = -1
        self.document_length = None
        self.preceding_header = None
        self.preceding_header_index = -1
        self.fragment_indices = None
        self.document_collection = None
        self.encoding = None
        self.encoding_mixup = False
        self.octavo_start_index = None
        self.octavo_end_index = None

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

    # def __context_search(self, search_text, document_text, ascii_search):
    #     if ascii_search:
    #         document_text = re.sub(r'[^\x00-\x7f]', r'', document_text)
    #     document_text_stripped = ' '.join(document_text.split())
    #     fragment_start_index = document_text_stripped.find(search_text)
    #     return [fragment_start_index, document_text_stripped]

    def __context_search(self, search_text, document_text, ascii_search):
        if ascii_search:
            document_text = re.sub(r'[^\x00-\x7f]', r'', document_text)
        document_text_stripped = ' '.join(document_text.split())
        fragment_start_index = document_text_stripped.find(search_text)
        return fragment_start_index

    def set_fragment_encoding(self, document_text_data):

        # always do unicode search first
        document_collection = document_text_data.get('collection')
        document_text = document_text_data.get('text')

        if document_collection == "ecco1":
            ascii_search = True
        else:
            ascii_search = False

        retried = False

        while True:
            fragment_start_index = self.__context_search(self.text,
                                                         document_text,
                                                         ascii_search)

            if fragment_start_index != -1:
                self.find_start_index = fragment_start_index
                self.find_end_index = (fragment_start_index +
                                       len(self.text))
                if ascii_search:
                    self.encoding = "ascii"
                else:
                    self.encoding = "unicode"
                return self.encoding

            elif fragment_start_index == -1 and not retried:
                print(" > Fragment not found." +
                      " Trying the other method (ascii/unicode)")
                self.encoding_mixup = True
                ascii_search = not ascii_search
                retried = True
                continue

            elif fragment_start_index == -1 and retried:
                print(" > !! Fragment still not found." +
                      " No encoding set.")
                return None

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

    def set_octavo_indices(self, octavo_indexmap):
        self.octavo_start_index = (
            self.find_octavo_index(self.find_start_index, octavo_indexmap))
        self.octavo_end_index = (
            self.find_octavo_index(self.find_end_index, octavo_indexmap))

    # REFRACTOR! this is a mess
    # def add_context(self, window_size=2000,
    #                 force_octavo_search=False,
    #                 add_headerdata=True,
    #                 headerdata_source=None,
    #                 get_octavo_indices=False,
    #                 document_text_data=None):

    #     if document_text_data is None:
    #         ecco_api_client = OctavoEccoClient()
    #         document_text_data = (
    #             ecco_api_client.get_text_for_document_id(self.ecco_id))

    #     document_text = document_text_data.get('text')
    #     document_collection = document_text_data.get('collection')
    #     self.document_collection = document_collection

    #     # if collection is ecco1, convert to ascii. else unicode
    #     if (window_size > 0) or force_octavo_search:
    #         if document_collection == "ecco1":
    #             ascii_search = True
    #         else:
    #             ascii_search = False

    #         retried = False
    #         while True:
    #             search_results = self.__context_search(self.text,
    #                                                    document_text,
    #                                                    ascii_search)
    #             fragment_start_index = search_results[0]
    #             document_text_stripped = search_results[1]
    #             if retried is True:
    #                 break
    #             elif fragment_start_index != -1:
    #                 if ascii_search:
    #                     self.encoding = "ascii"
    #                 else:
    #                     self.encoding = "unicode"
    #                 if get_octavo_indices:
    #                     self.octavo_start_index = self.__get_orig_index(
    #                         fragment_start_index, document_text, ascii_search)
    #                     self.octavo_end_index = self.__get_orig_index(
    #                         (fragment_start_index + len(self.text)),
    #                         document_text, ascii_search)
    #                 break
    #             elif fragment_start_index == -1:
    #                 # sometime ecco1 isn't ascii after all! Go figure.
    #                 print(" > Fragment not found." +
    #                       " Trying the other method (ascii/unicode)")
    #                 ascii_search = not ascii_search
    #                 retried = True

    #         if fragment_start_index == -1:
    #             print(
    #                 " >> Fragment text still not found in fulltext!" +
    #                 " Using original reuse cluster data.")
    #             print(" >>> cluster_id: " + str(self.cluster_id))
    #             print(" >>> ecco_id: " + str(self.ecco_id))
    #             self.find_start_index = self.start_index
    #             self.find_end_index = self.end_index
    #             self.fragment_indices = "from clusterdata"
    #         else:
    #             self.find_start_index = fragment_start_index
    #             self.find_end_index = (fragment_start_index +
    #                                    len(self.text))
    #             self.fragment_indices = "searched"

    #         context_before_start_index = self.find_start_index - window_size
    #         if context_before_start_index < 0:
    #             print(" > Fragment context start index before document start.")
    #             context_before_start_index = 0
    #         context_before_end_index = fragment_start_index

    #         self.text_before = (document_text_stripped[
    #             context_before_start_index:context_before_end_index])

    #         document_text_stripped_length = len(document_text_stripped)
    #         self.document_length = document_text_stripped_length

    #         context_after_start_index = self.find_end_index
    #         context_after_end_index = context_after_start_index + window_size
    #         if context_after_end_index > document_text_stripped_length:
    #             print(" > Fragment context end index" +
    #                   "larger than document length.")
    #             context_after_end_index = document_text_stripped_length

    #         self.text_after = (document_text_stripped[
    #             context_after_start_index:context_after_end_index])

    #     if add_headerdata:
    #         if headerdata_source is None:
    #             headerdata = get_headers_from_document_text(document_text)
    #         else:
    #             headerdata = headerdata_source
    #         self.add_headerdata(headerdata)
