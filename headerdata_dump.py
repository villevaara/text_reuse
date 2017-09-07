import csv
import os.path
import sys
from requests import Timeout
from time import sleep
from timeit import default_timer as timer

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.tr_fragment import TextReuseFragment


def add_csv_ids_to_set(csvfile_location, destination_set):
    with open(csvfile_location, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for item in csvreader:
            destination_set.add(item[0])


def get_doctext_indexmap(orig_text, method_ascii):
    whitespace_chars = [' ', '\t', '\n', '\r', '\x0b', '\x0c']
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
            # this_char_hit = True
            chars_lost += 1
            save_pending = True
        if orig_text[char_index] in whitespace_chars:
            this_char_wshit = True
        else:
            this_char_wshit = False
        if prev_char_wshit and this_char_wshit:
            chars_lost += 1
            save_pending = True
        prev_char_wshit = this_char_wshit
        if save_pending and not this_char_wshit:
            fragment_index = char_index - chars_lost
            fragment_indices.append(fragment_index)
            chars_lost_list.append(chars_lost)
            # results.append([fragment_index, chars_lost])
            save_pending = False
    if method_ascii:
        method_description = "ascii"
    else:
        method_description = "unicode"
    results = {'method': method_description,
               'fragment_index': fragment_indices,
               'chars_lost': chars_lost_list}
    return results


def get_fragmentlist(cluster_data, document_text_data,
                     docid_indexmap_ascii,
                     docid_indexmap_unicode):
    print("> Getting fragment list ...")
    cluster_data_length = len(cluster_data) - 1
    fragment_list = []
    i = 0
    print("items in list: " + str(cluster_data_length))
    for item in cluster_data:
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
        fragment.set_fragment_encoding(document_text_data=document_text_data)
        if fragment.encoding_type == "ascii":
            fragment.set_octavo_indices(docid_indexmap_ascii)
        else:
            fragment.set_octavo_indices(docid_indexmap_unicode)
        fragment_list.append(fragment)
    print("  >> Done!")
    return fragment_list


def read_processed_ids_from_results_csv(results_csv):
    processed_ids = set()
    with open(results_csv) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        for line in csvreader:
            processed_ids.add(line[0])
    print("Already processed ids: " + str(len(processed_ids)))
    return processed_ids


def write_summary_row(docid, fragments_total, summary_csv):
        with open(summary_csv, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([docid,
                                fragments_total])
            print("docid: " + docid + ' summary written.')


def write_results_csv_header(results_csv):
    results_csv_exists = os.path.exists(results_csv)

    if not results_csv_exists:
        with open(results_csv, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['document_id',
                                'cluster_id',
                                'octavo_start_index',
                                'octavo_end_index'])


def prepare_summary_csv(summary_csv):
    summary_csv_exists = os.path.exists(summary_csv)
    if not summary_csv_exists:
        # writer results csv header
        with open(summary_csv, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['document_id',
                                'fragments_total'])


ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(timeout=600)

fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "clusterID"]

ids_to_process = set()

add_csv_ids_to_set('data/ecco1_ids.csv', ids_to_process)
add_csv_ids_to_set('data/ecco2_ids.csv', ids_to_process)

summary_csv = 'output/octavo_indices/summary.csv'
prepare_summary_csv(summary_csv)

# get processed ids from summary.
processed_ids = read_processed_ids_from_results_csv(summary_csv)

# skip already processed ids

# start with no docid preloaded
# docid_preloaded = ""

for docid in ids_to_process:

    # preload next docid into api cache
    # TODO: package this into function in api_client

    # # forget about the preloading stuff for now
    # print("Preloading docid: " + docid)
    # docid_to_preload = docid
    # preload_request = cluster_api_client.get_cluster_data_for_document_id_url(
    #     docid_to_preload)
    # try:
    #     cluster_api_client.call_api_with_get_and_forget(preload_request)
    # except Timeout:
    #     print("Preloading into API cache...")
    # else:
    #     print("That was fast!")

    # # if there is no docid preloaded, so the loop iteration is first, wait.
    # if docid_preloaded != "":
    #     print("Processing preloaded docid...")
    #     docid_to_process = docid_preloaded
    # else:
    #     # wait 5 minutes, then mark docid as preloaded
    #     print("Preloading first request! 3 mins...")
    #     sleep(180)
    #     docid_preloaded = docid
    #     continue
    docid_to_process = docid

    if docid_to_process in processed_ids:
        print("DocID already processed!?")
        continue

    # try catch here with retry (x10? 20 sec delay)
    retries = 0
    while retries < 11:
        try:
            docid_clusterdata = (
                cluster_api_client.get_cluster_data_for_document_id(
                    docid_to_process))
        except ValueError:
            print("Request probably timed out or something." +
                  " Retrying in 5 secs. Retries: " + str(retries))
            sleep(5)
            retries = retries + 1
            if retries == 11:
                print("That's too many!")
                sys.exit("Aargh! Errors!")
            continue
        else:
            print("Got cluster data...")
            break

    # we should have the good response now. Yay
    # docid_fulltext = ecco_api_client.get_text_for_document_id(docid_to_process)
    # docid_fragments = get_fragmentlist(docid_clusterdata, docid_fulltext)
    # docid_fragments_amount = len(docid_fragments)

    docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid)
    docid_fulltext_text = docid_fulltext_data.get('text')

    # start = timer()
    docid_indexmap_ascii = get_doctext_indexmap(orig_text=docid_fulltext_text,
                                                method_ascii=True)
    docid_indexmap_unicode = get_doctext_indexmap(orig_text=docid_fulltext_text,
                                                  method_ascii=False)
    # end = timer()
    # print("Indexmaps took " + str(round((end - start), 2)) + "s")

    # start = timer()
    docid_fragments = get_fragmentlist(docid_clusterdata,
                                       docid_fulltext_data,
                                       docid_indexmap_ascii,
                                       docid_indexmap_unicode)
    # end = timer()
    # print("Fragments took " + str(round((end - start), 2)) + "s")
    docid_fragments_amount = len(docid_fragments)

    fragment_results = []

    for fragment in docid_fragments:
        fragment_data = {'cluster_id': fragment.cluster_id,
                         'document_id': fragment.ecco_id,
                         'octavo_start_index': fragment.octavo_start_index,
                         'octavo_end_index': fragment.octavo_end_index}
        fragment_results.append(fragment_data)

    # write results into csv file. first 4 digits docid separate files.
    docid_filepart = docid_to_process[:4]
    results_csv = ('output/octavo_indices/' +
                   'actual_octavo_indices_' +
                   docid_filepart +
                   '.csv')

    write_results_csv_header(results_csv)
    with open(results_csv, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        for result in fragment_results:
            csvwriter.writerow([result.get('document_id'),
                                result.get('cluster_id'),
                                result.get('octavo_start_index'),
                                result.get('octavo_end_index')])
        print("docid: " + docid_to_process + ' results written to ' +
              results_csv)

    write_summary_row(docid_to_process, docid_fragments_amount, summary_csv)

    # preloading should have finished while processing previous doc.
    processed_ids.add(docid_to_process)

    # docid_preloaded = docid_to_preload
