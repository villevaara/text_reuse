# text_reuse_cluster_char_map.py

from collections import OrderedDict

from lib.tr_fragment import TextReuseFragment
from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )
from lib.fragmentlists import (
    FragmentList,
    get_doctext_indexmap,
    get_document_text_splitjoined)
from lib.headerdata import (get_headers_for_document_id,
    get_headers_from_document_text)
from lib.author_metadata import read_author_metadata_csv
from lib.text_reuse_common import (
    load_good_metadata
    )


def read_txt_file_to_string(file_path):
    with open(file_path, 'r') as txtfile:
        str_data = txtfile.read()
        return str_data


# document_id = document_id_dict.get('id')

# get doc from api
# api_limit = -1
ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(
    limit=-1, timeout=60)

document_id = "0175300500"
document_text = ecco_api_client.get_text_for_document_id(document_id)['text']
# document_text = document_data.get('text')
document_meta = ecco_api_client.get_document_id_metadata(document_id)

# test_text_loc = "/media/vvaara/uh-villevaara-ext1/eccotxt/ECCO_I/ECCO_2of2/RelAndPhil/0010800104/xml/0010800104.txt"
# test_text = read_txt_file_to_string(test_text_loc)


headerdata = get_headers_for_document_id(document_id, document_text)
print("> Fetching clusterIDs ...")
cluster_ids = cluster_api_client.get_cluster_ids_list_for_document_id(
    document_id)
print("  >> Done!")
print("> Getting cluster data ...")
cluster_data = cluster_api_client.get_cluster_data_for_cluster_id_list(
    cluster_ids)
print("  >> Done!")


author_metadata = read_author_metadata_csv(
    "../data-public/authors-metadata/misc/author_metadata.csv")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)


fragment_list = FragmentList(cluster_data, seed_document_id=document_id)
fragment_list.add_metadata(author_metadata, good_metadata=good_metadata)
fragment_list.set_octavo_indices()
fragment_list.remove_fragments_missing_correct_indices()
fragment_list.add_headerdata(headerdata, document_id)

# fragment_list.fragments_by_ecco_id

# get text and meta for each ecco id in ecco_id list, get length of text


# def get_document_text_without_headers(this_ecco_text, this_ecco_headers):
#     this_ecco_text_stripped = this_ecco_text
#     for header in this_ecco_headers:
#         this_ecco_text_stripped = "".join(
#             this_ecco_text_stripped.split(header['full_header_text']))
#     return this_ecco_text_stripped


# def get_stripped_text_index(this_ecco_headers):
#     stripped_text_index = []
#     chars_removed = 0
#     for header in this_ecco_headers:
#         stripped_header_index = header['index'] - chars_removed
#         chars_removed += len(header['full_header_text'])
#         stripped_text_index.append(
#             {'index': stripped_header_index,
#              'chars_removed': chars_removed,
#              'header_text': header['full_header_text']})
#     # index is the character index by which
#     # chars_removed number of characters in headers have been removed
#     return stripped_text_index


# def verify_header_embedding_index(
#         ecco_octavo_text, fragment_text, missing_index):
#     full_text_subset = ecco_octavo_text[
#         missing_index['start_index']:
#         missing_index['end_index']]
#     full_text_subset_minus_headers = full_text_subset
#     for header in missing_index['headers_within']:
#         full_text_subset_minus_headers = (
#             "".join(full_text_subset_minus_headers.split(header)))
#     verifies = full_text_subset_minus_headers == fragment_text
#     return {
#         'full_text_subset': full_text_subset,
#         'full_text_subset_minus_headers': full_text_subset_minus_headers,
#         'fragment_text': fragment_text,
#         'verifies': verifies
#     }


# def get_missing_fragment_index(
#         fragment_text, stripped_text, stripped_text_index):
#     stripped_frag_index_start = stripped_text.find(fragment_text)
#     # if fragment text is not found in the stripped text, return -1
#     if stripped_frag_index_start == -1:
#         return {
#             'start_index': -1,
#             'end_index': -1}
#     stripped_frag_index_end = stripped_frag_index_start + len(fragment_text)
#     start_add = 0
#     end_add = 0
#     headers_within = []
#     for item in stripped_text_index:
#         if item['index'] <= stripped_frag_index_start:
#             start_add += len(item['header_text'])
#         if item['index'] <= stripped_frag_index_end:
#             end_add += len(item['header_text'])
#             if item['index'] > stripped_frag_index_start:
#                 headers_within.append(item['header_text'])
#         else:
#             break
#     return {
#         'start_index': stripped_frag_index_start + start_add,
#         'end_index': stripped_frag_index_end + end_add,
#         'headers_within': headers_within}


# def get_index_for_header_enclosing_fragment(this_ecco_text, fragment_text):
#     this_ecco_headers = get_headers_from_document_text(this_ecco_text)
#     stripped_text_index = get_stripped_text_index(this_ecco_headers)
#     stripped_text = get_document_text_without_headers(
#         this_ecco_text, this_ecco_headers)
#     missing_index = get_missing_fragment_index(
#         fragment_text, stripped_text, stripped_text_index)
#     index_verifies = verify_header_embedding_index(
#         this_ecco_text, fragment_text, missing_index)
#     if index_verifies:
#         return {
#             'start_index': missing_index['start_index'],
#             'end_index': missing_index['end_index']
#         }
#     else:
#         return {
#             'start_index': None,
#             'end_index': None
#         }


# process just one id for starters
this_ecco_id = "1352700100"
frag_id = 5713590
# this_ecco_id = list(fragment_list.fragments_by_ecco_id.keys())[0]
this_ecco_textdata = ecco_api_client.get_text_for_document_id(this_ecco_id)
this_ecco_text = this_ecco_textdata['text']
# this_ecco_meta = ecco_api_client.get_document_id_metadata(this_ecco_id)
this_ecco_headers = get_headers_from_document_text(this_ecco_text)
stripped_text_index = get_stripped_text_index(this_ecco_headers)
stripped_text = get_document_text_without_headers(
    this_ecco_text, this_ecco_headers)
fragment_text = "g~land, by the conquest, gained likewise·\n\nnaturalr right to the dominion of the Channe\nwhich had be~fore been acquired only by di\n\nreat naval power of Edgar, and other Saxon\nlongs. But the dominion of the narrow f'eas\n.fems naturally to belong, like that of rivers, to\n·those who pe.ffefs the bankss or coasts, on both\n[Mdes, and to to have firengthened the former\ngfle by so long a coast, as that of Normandy on,\n-orie fide, and' of England on the other fide o"
missing_index = get_missing_fragment_index(fragment_text, stripped_text, stripped_text_index)

# # can prob now use document text directly
# # package in function(s)
# docid_indexmap_ascii = get_doctext_indexmap(
#     orig_text=this_ecco_textdata['text'], method_ascii=True)
# docid_indexmap_unicode = get_doctext_indexmap(
#     orig_text=this_ecco_textdata['text'], method_ascii=False)
# docid_indexmap = get_doctext_indexmap(
#     orig_text=this_ecco_textdata['text'], method_ascii=False)

# text_splitjoined_unicode = (
#     get_document_text_splitjoined(
#         this_ecco_textdata.get('text'),
#         ascii_search=False))
# text_splitjoined_ascii = (
#     get_document_text_splitjoined(
#         this_ecco_textdata.get('text'),
#         ascii_search=True))
# this_ecco_textdata['splitjoined_unicode'] = (text_splitjoined_unicode)
# this_ecco_textdata['splitjoined_ascii'] = (text_splitjoined_ascii)

# for fragment in fragment_list.fragments_by_ecco_id[this_ecco_id]:
#     fragment.set_simple_find_index(this_ecco_textdata['text'])



# # set fragment octavo indices
# for fragment in fragment_list.fragments_by_ecco_id[this_ecco_id]:
#     is_ascii = fragment.set_fragment_encoding(this_ecco_textdata)
#     if is_ascii:
#         fragment.set_octavo_indices(docid_indexmap_ascii, False)
#     else:
#         fragment.set_octavo_indices(docid_indexmap_unicode, False)

# # set raw text lengths
# this_ecco_textdata['raw_length'] = len(
#     this_ecco_textdata['splitjoined_unicode'])
# this_ecco_textdata['octavo_length'] = len(
#     this_ecco_textdata['text'])

# char_in_fragment_dict = OrderedDict()
# for char_ind in range(0, (this_ecco_textdata['octavo_length'] - 1)):
#     char_in_fragment_dict[char_ind] = {
#         'char': this_ecco_textdata['text'][char_ind],
#         'fragment_ids': [],
#         'in_fragment': False}

# for fragment in fragment_list.fragments_by_ecco_id[this_ecco_id]:
#     for char_ind in range(
#             fragment['octavo_start_index'],
#             (fragment['octavo_end_index'] - 1)):
#         char_in_fragment_dict[char_ind]['fragment_ids'].append(
#             fragment.cluster_id)
#         char_in_fragment_dict[char_ind]['in_fragment'] = False



# * fragmenlist has fragments by ecco id
# * order those fragments by 'octavo_start_index'

# * for each character check if they are in a fragment or not. create 
#   new list of fragments that do not overlap.
# * create a dict with char index as key:
#   * char, list of fragment indices, in fragment or not

# get:
#   -> number of chars of original work reused in another work
#   -> locations of reused text in that another work
#   -> 



# documents_meta_dict[document_id] = {
#     'id': document_id,
#     'length': len(document_text),
#     'sequence': document_id_dict.get('sequence'),
#     'description': document_id_dict.get('description')
# }


# # below copied from main.py
# def get_cluster_coverage_data(document_id_to_cover,
#                               cluster_list,
#                               ecco_api_client):
#     document_text = ecco_api_client.get_text_for_document_id(
#         document_id_to_cover).get('text')
#     document_length = len(document_text)
#     cluster_coverage = [0] * document_length
#     # cluster_text = [""] * document_length
#     for cluster in cluster_list:
#         start = cluster.group_start_index
#         end = cluster.group_end_index
#         length = cluster.get_length()
#         # print("s: " + str(start) + " e: " +
#         #       str(end) + " l: " + str(length))
#         for i in range(start, end + 1):
#             cluster_coverage[i] = cluster_coverage[i] + length
#     return cluster_coverage

