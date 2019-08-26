import csv
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


ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(timeout=600)

docids_asciimap = read_docid_asciimap_csv('data/eccoids/asciilines.csv')

fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "fragmentID", "text",
                     "startIndex", "endIndex"]


docid_to_process = "0162900301"

docid_clusterdata = (
    cluster_api_client.get_cluster_data_for_document_id(
        docid_to_process, fields=field_eccocluster))

docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid_to_process)
docid_fulltext_text = docid_fulltext_data.get('text')

docid_ascii = docids_asciimap.get(docid_to_process)
docid_indexmap_ascii = get_doctext_indexmap(
    orig_text=docid_fulltext_text, method_ascii=True)
docid_indexmap_unicode = get_doctext_indexmap(
    orig_text=docid_fulltext_text, method_ascii=False)

docid_fragments = get_fragmentlist(docid_clusterdata,
                                   docid_fulltext_data,
                                   docid_indexmap_ascii,
                                   docid_indexmap_unicode,
                                   docid_is_ascii=docid_ascii)

docid_fragments_amount = len(docid_fragments)

fragment_results = []

for fragment in docid_fragments:
    api_text_slice = docid_fulltext_text[
        fragment.octavo_start_index:fragment.octavo_end_index]
    frag_validation = (
        test_fragment_text(fragment, docid_fulltext_text))
    fragment_data = {'cluster_id': fragment.cluster_id,
                     'document_id': fragment.ecco_id,
                     'octavo_start_index': fragment.octavo_start_index,
                     'octavo_end_index': fragment.octavo_end_index,
                     'orig_start_index': fragment.start_index,
                     'is_ascii': fragment.is_ascii,
                     'frag_text': fragment.text,
                     'octavo_text': api_text_slice,
                     'frag_validates': frag_validation
                     }
    fragment_results.append(fragment_data)

with open('test_data.json', 'w') as outfile:
    json.dump(fragment_results, outfile, indent=4)
    outfile.write("\n") # json dump does not end with newline

# test_fragment_text(docid_fragments[0], docid_fulltext_text)


