import csv
import glob
import os.path
import sys
import getopt
from time import sleep
from timeit import default_timer as timer
import json

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.fragmentlists import (
    get_fragmentlist,
    get_doctext_indexmap,
    test_fragment_text)

from lib.utils_common import create_dir_if_not_exists
from lib.headerdata_dump_common import read_docid_asciimap_csv

from collections import OrderedDict
from bisect import bisect_left


# from lib.additional_cluster_data import read_datadir_add_clusterdata


# def get_docid_fragments(docid_to_process, field_eccocluster):
#     docid_clusterdata = (
#         cluster_api_client.get_cluster_data_for_document_id(
#             docid_to_process, fields=field_eccocluster))
#     docid_fulltext_data = ecco_api_client.get_text_for_document_id(
#         docid_to_process)
#     docid_fulltext_text = docid_fulltext_data.get('text')
#     docid_ascii = docids_asciimap.get(docid_to_process)
#     docid_indexmap_ascii = get_doctext_indexmap(
#         orig_text=docid_fulltext_text, method_ascii=True)
#     docid_indexmap_unicode = get_doctext_indexmap(
#         orig_text=docid_fulltext_text, method_ascii=False)
#     docid_fragments = get_fragmentlist(docid_clusterdata,
#                                        docid_fulltext_data,
#                                        docid_indexmap_ascii,
#                                        docid_indexmap_unicode,
#                                        docid_is_ascii=docid_ascii)
#     # revalidate and discard those that do not validate
#     return docid_fragments


# def get_validated_fragmentlist(fragmentlist, docid):
#     validated_fraglist = []
#     docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid)
#     print("validating fragdata")
#     for fragment in fragmentlist:
#         # api_text_slice = docid_fulltext_data.get('text')[
#         #     fragment.octavo_start_index:fragment.octavo_end_index]
#         frag_validation = (
#             test_fragment_text(fragment, docid_fulltext_data.get('text')))
#         if frag_validation:
#             validated_fraglist.append(fragment)
#         else:
#             print("a fragment did not validate. ?!")
#             print("fragment_id: " + str(fragment.cluster_id))
#             print("ecco_id:     " + str(fragment.ecco_id))
#     return validated_fraglist


# transfer <<<

# def get_page_number_for_char_i(first_char_page_index, char_i):
#     indices = list(first_char_page_index.keys())
#     index_number = bisect_left(indices, char_i) - 1
#     page_number = first_char_page_index[indices[index_number]]
#     return page_number


# def get_page_first_char_index(first_char_page_index, pagenumber):
#     return list(first_char_page_index.keys())[pagenumber - 1]


# def get_page_last_char_index(first_char_page_index, pagenumber, fulltext_len):
#     if pagenumber < len(first_char_page_index):
#         return list(first_char_page_index.keys())[pagenumber] - 1
#     else:
#         return fulltext_len - 1


# def get_snippet_data(snip_start, snip_end, fulltext, first_char_page_index):
#     snip_first_page = get_page_number_for_char_i(
#         first_char_page_index, snip_start)
#     snip_last_page = get_page_number_for_char_i(
#         first_char_page_index, snip_end)
#     snip_page_range = list(range(snip_first_page, snip_last_page + 1))
#     snip_page_dict = OrderedDict()
#     fulltext_length = len(fulltext)
#     #
#     for page_number in snip_page_range:
#         page_first_char_index = get_page_first_char_index(
#             first_char_page_index, page_number)
#         page_last_char_index = get_page_last_char_index(
#             first_char_page_index, page_number, fulltext_length)
#         if snip_end < page_last_char_index:
#             page_snip_end = snip_end - 1
#         else:
#             page_snip_end = page_last_char_index
#         if snip_start >= page_first_char_index:
#             page_snip_start = snip_start
#         else:
#             page_snip_start = page_first_char_index
#         page_snip = fulltext[page_snip_start:(page_snip_end + 1)]
#         snip_page_dict[page_number] = {
#             'snip_start': page_snip_start,
#             'snip_end': page_snip_end,
#             'snip_text': page_snip
#         }
#     return snip_page_dict

# transfer >>>


# estc T082481
cluster_api_client = OctavoEccoClusterClient(timeout=600)
ecco_api_client = OctavoEccoClient()

docids_asciimap = read_docid_asciimap_csv('data/eccoids/asciilines.csv')

fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "fragmentID", "text",
                     "startIndex", "endIndex"]

docid_text = ecco_api_client.get_text_for_document_id('0162200200').get('text')

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )
from lib.tr_bookcontainer import BookContainer

ecco_api_client = OctavoEccoClient()
humebook = BookContainer(
    octavo_id='0162200200',
    ecco_api_client=ecco_api_client,
    xml_img_page_datadir="~/projects/comhis/data-own-common/ecco-xml-img/"
    )

# add_cludatadir = "data/tr_data_additional/14_volumes/"
# add_cludata = read_datadir_add_clusterdata(add_cludatadir)
# relevant_add_cludata = filter_add_cludata_with_docid(add_cludata,
#                                                      '0162200200')


# with open('temp/humedump.txt', 'w') as outfile:
#     outfile.write(docid_text)

# gale_url = (
#     "http://gdc.galegroup.com/gdc/artemis/MonographsDetailsPage/" +
#     "MonographsDetailsWindow?disableHighlighting=" +
#     "&displayGroupName=DVI-Monographs&docIndex=&source=&prodId=ECCO" +
#     "&mode=view&limiter=&display-query=&contentModules=&action=e" +
#     "&sortBy=&windowstate=normal&currPage=&dviSelectedPage=&scanId=" +
#     "&query=&search_within_results=&p=ECCO&catId=&u=uhelsink&displayGroups=" +
#     "&documentId=GALE%7CCW0101494465&activityType=AdvancedSearch" +
#     "&failOverType=&commentary=")

# --- start ---
# move over to tr_bookcontainer.py

# docid_text_pages_dir = "data/hume_paginated/0162200200/"

# pagefiles = glob.glob(docid_text_pages_dir + "*_page*.txt")
# pagefiledict = {}
# lastpage = 0
# for pagefile in pagefiles:
#     pagenumber = int(pagefile.split('page')[1].split('.txt')[0])
#     if pagenumber > lastpage:
#         lastpage = pagenumber
#     pagefiledict[pagenumber] = pagefile

# combined_text_list = []
# first_char_page_index = OrderedDict()
# chars_processed = 0
# for pagenumber in list(range(1, (lastpage + 1))):
#     with open(pagefiledict.get(pagenumber), 'r') as pagefile:
#         pagetext = pagefile.read()
#     first_char_page_index[chars_processed] = pagenumber
#     chars_processed += len(pagetext)
#     combined_text_list.append(pagetext)

# combined_text = "".join(combined_text_list).strip()
# if docid_text == combined_text:
#     print("Combined text matches with API text.")

# --- end ---

# for each fragment get pages
# and characters on page for that fragment

test_frags = get_docid_fragments('0162200200', field_eccocluster)
valid_frags = get_validated_fragmentlist(test_frags, '0162200200')
fulltext_len = len(docid_text)

start_i = valid_frags[0].octavo_start_index
end_i = valid_frags[0].octavo_end_index

snippet_data = get_snippet_data(start_i, end_i, docid_text,
                                first_char_page_index)

# get_snippet_data(60, 233, docid_text, first_char_page_index)


def test_results(char_index):
    page_number = get_page_number_for_char_i(first_char_page_index, char_index)
    fchar_i = get_page_first_char_index(first_char_page_index, page_number)
    lchar_i = get_page_last_char_index(
        first_char_page_index, page_number, fulltext_len)
    print("page number: " + str(page_number))
    print("page first char: " + str(fchar_i))
    print("page last char: " + str(lchar_i))


char_index = 1104045
test_results(char_index)


# http://callisto.ggsrv.com/imgsrv/FastFetch/UBER2/016220020000230?legacy=no&format=web&highlight=00ff00+.7+236+246+204+43
# hpos, vpos, width, height
# <wd pos="236,246,440,289">SEVERAL</wd>

# 1. find text in docfulltext
# 2. find text in xml
# 3. find token positions in xml
# 4. find


from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )
from lib.tr_bookcontainer import BookContainer

ecco_api_client = OctavoEccoClient()
humebook = BookContainer(
    octavo_id='0162200200',
    ecco_api_client=ecco_api_client,
    xml_img_page_datadir="/home/vvaara/projects/comhis/data-own-common/ecco-xml-img/"
    )
humebook.set_fulltext_page_char_index()

