import re
import sys

from lib.tr_fragment import TextReuseFragment
from lib.text_reuse_common import load_good_metadata


def test_fragment_text(fragment, document_text):
    fragment_text = fragment.text
    fragment_text = fragment_text.strip()
    octavo_text = document_text[fragment.octavo_start_index:
                                fragment.octavo_end_index]
    if fragment.is_ascii:
        octavo_text = re.sub(r'[^\x00-\x7f]', r'', octavo_text)
    octavo_text = ' '.join(octavo_text.split())
    if fragment_text == octavo_text:
        return True
    else:
        # print(fragment_text)
        # print("\n")
        # print(octavo_text)
        return False


def get_document_text_splitjoined(document_text, ascii_search):
    if ascii_search:
        document_text = re.sub(r'[^\x00-\x7f]', r'', document_text)
    document_text_stripped = ' '.join(document_text.split())
    return document_text_stripped


def get_fragmentlist(cluster_data, document_text_data,
                     docid_indexmap_ascii,
                     docid_indexmap_unicode,
                     docid_is_ascii):
    print("> Getting fragment list ...")
    cluster_data_length = len(cluster_data) - 1
    fragment_list = []
    doctext_splitjoined_unicode = None
    doctext_splitjoined_ascii = None

    i = 0
    print("items in list: " + str(cluster_data_length))

    for item in cluster_data:
        if i % 50 == 0:
            print("Processing item: " + str(i) +
                  " / " + str(cluster_data_length))
            print("documentID: " + item.get('documentID'))
            print("clusterID:  " + str(item.get('clusterID')))
        i = i + 1
        fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                     cluster_id=item.get('clusterID'),
                                     text=item.get('text'),
                                     start_index=item.get('startIndex'),
                                     end_index=item.get('endIndex'))

        if docid_is_ascii is None:
            use_orig = False
        else:
            use_orig = True

        text_validates = False

        # set octavo indices
        while not text_validates:
            if use_orig:
                fragment.is_ascii = docid_is_ascii
            else:
                # only do splitjoin once.
                if doctext_splitjoined_unicode is None:
                    print("splitjoining doctext unicode")
                    doctext_splitjoined_unicode = (
                        get_document_text_splitjoined(
                            document_text_data.get('text'),
                            ascii_search=False))
                if doctext_splitjoined_ascii is None:
                    print("splitjoining doctext ascii")
                    doctext_splitjoined_ascii = (
                        get_document_text_splitjoined(
                            document_text_data.get('text'),
                            ascii_search=True))
                document_text_data['splitjoined_unicode'] = (
                    doctext_splitjoined_unicode)
                document_text_data['splitjoined_ascii'] = (
                    doctext_splitjoined_ascii)
                fragment.set_fragment_encoding(
                    document_text_data=document_text_data)
                # print("fragment.is_ascii: " + str(fragment.is_ascii))

            if fragment.is_ascii is None:
                print("     >> Octavo indices not found for fragment" +
                      " clu: " + fragment.cluster_id +
                      " doc: " + fragment.ecco_id +
                      "\n      >> moving on with life.")
                fragment.octavo_start_index = -1
                fragment.octavo_end_index = -1
                sys.exit("ERROR!")
                break
            if fragment.is_ascii:
                # print("indexes: ascii")
                # print("use_orig: " + str(use_orig))
                fragment.set_octavo_indices(docid_indexmap_ascii,
                                            orig_index=use_orig)
            else:
                # print("indexes: unicode")
                # print("use_orig: " + str(use_orig))
                fragment.set_octavo_indices(docid_indexmap_unicode,
                                            orig_index=use_orig)

            if test_fragment_text(fragment, document_text_data.get('text')):
                text_validates = True
            else:
                # print(" !!ERRORERROR!! fragment text does not match!")
                use_orig = False

        fragment_list.append(fragment)

    print("  >> Done!")
    return fragment_list


def get_doctext_indexmap(orig_text, method_ascii):
    whitespace_chars = ['\t', '\n', '\x0b', '\x0c', '\r', '\x1c', '\x1d',
                        '\x1e', '\x1f', ' ', '\x85', '\xa0', '\u1680',
                        '\u2000', '\u2001', '\u2002', '\u2003', '\u2004',
                        '\u2005', '\u2006', '\u2007', '\u2008', '\u2009',
                        '\u200a', '\u2028', '\u2029', '\u202f', '\u205f',
                        '\u3000']
    orig_text_length = len(orig_text)
    # results to return. array (list) of fragmenttext_index,chars_lost
    fragment_indices = []
    chars_lost_list = []
    # cumlative index of characters lost
    chars_lost = 0
    # set flags
    # start with prev_char_hit -flag set to account for leading zeros
    prev_char_wshit = True
    this_char_wshit = False
    save_pending = False
    # iterate every char in text.
    # add entry to index if previous char was lost, and current isn't
    for char_index in range(0, orig_text_length):
        if method_ascii and ord(orig_text[char_index]) > 127:
            # getting non-ascii: if ord(char) is > 127
            chars_lost += 1
            save_pending = True
            continue
        if orig_text[char_index] in whitespace_chars:
            this_char_wshit = True
        else:
            this_char_wshit = False
        if prev_char_wshit and this_char_wshit:
            chars_lost += 1
            save_pending = True
        prev_char_wshit = this_char_wshit
        # save also at last char
        if (save_pending and not this_char_wshit) or \
           (save_pending and char_index == orig_text_length - 1):
            fragment_index = char_index - chars_lost
            fragment_indices.append(fragment_index)
            chars_lost_list.append(chars_lost)
            save_pending = False
    if method_ascii:
        method_description = "ascii"
    else:
        method_description = "unicode"
    results = {'method': method_description,
               'fragment_index': fragment_indices,
               'chars_lost': chars_lost_list}
    return results


class FragmentList(object):

    def __init__(self, cluster_data, seed_docid):

        self.seed_docid = seed_docid  # not used ...
        self.fragment_list = (
            self.get_initial_fragment_list(cluster_data))
        self.cluster_id_index = dict()
        self.document_id_index = dict()

    def get_initial_fragment_list(self, cluster_data):
        print("  > Initializing fragment list ...")
        cluster_data_length = len(cluster_data)
        fragment_list = []
        print("items in list: " + str(cluster_data_length))
        for item in cluster_data:
            fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                         cluster_id=item.get('clusterID'),
                                         text=item.get('text'),
                                         start_index=item.get('startIndex'),
                                         end_index=item.get('endIndex'))
            fragment_list.append(fragment)
        return fragment_list

    def set_cluster_id_index(self):
        i = 0
        for fragment in self.fragment_list:
            cluid = fragment.cluster_id
            fragment_index = i
            if cluid in self.cluster_id_index.keys():
                self.cluster_id_index[cluid].append(fragment_index)
            else:
                self.cluster_id_index[cluid] = [fragment_index]
            i += 1

    def __verify_cluster_index_built(self):
        if len(self.cluster_id_index) == 0:
            print("Building cluster id index.")
            self.set_cluster_id_index()

    def set_document_id_index(self):
        i = 0
        for fragment in self.fragment_list:
            docid = fragment.document_id
            fragment_index = i
            if docid in self.document_id_index.keys():
                self.document_id_index[docid].append(fragment_index)
            else:
                self.document_id_index[docid] = [fragment_index]
            i += 1

    def __verify_document_index_built(self):
        if len(self.document_id_index) == 0:
            print("Building document id index.")
            self.set_document_id_index()

    def add_metadata(self, author_metadata, good_metadata=None):
        if good_metadata is None:
            good_metadata_jsonfile = "data/metadata/good_metadata.json"
            good_metadata = load_good_metadata(good_metadata_jsonfile)
        print("  > Adding metadata to fragments.")
        for fragment in self.fragment_list:
            fragment.add_metadata(good_metadata, author_metadata)

    def add_headerdata(self, headerdata, document_id):
        print("  > Adding headerdata to matching fragments.")
        for fragment in self.fragment_list:
            if fragment.ecco_id == document_id:
                fragment.add_headerdata(headerdata)

    def get_unique_authors(self):
        unique_authors = set()
        for fragment in self.fragment_list:
            unique_authors.add(fragment.author)
        return unique_authors

    def get_unique_cluster_ids(self):
        self.__verify_cluster_index_built()
        unique_cluster_ids = self.cluster_id_index.keys()
        return unique_cluster_ids

    def get_fragments_of_cluster_id(self, cluster_id):
        self.__verify_cluster_index_built()
        filtered_list = []
        for fragment_index in self.cluster_id_index[cluster_id]:
            filtered_list.append(self.fragment_list[fragment_index])
        return filtered_list

    def get_unique_document_ids(self):
        self.__verify_document_index_built()
        unique_document_ids = self.document_id_index.keys()
        return unique_document_ids

    def get_fragments_of_document_id(self, document_id):
        self.__verify_document_index_built()
        filtered_list = []
        for fragment_index in self.document_id_index[document_id]:
            filtered_list.append(self.fragment_list[fragment_index])
        return filtered_list

    def get_length(self):
        return len(self.fragment_list)
