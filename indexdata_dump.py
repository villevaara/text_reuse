import csv
import os.path
import sys
import getopt
from time import sleep
from timeit import default_timer as timer

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.fragmentlists import (
    get_fragmentlist,
    get_doctext_indexmap)

from lib.utils_common import create_dir_if_not_exists
from lib.headerdata_dump_common import read_docid_asciimap_csv

# usage:
# $ python indexdata_dump.py --inputfile ecco1_ids1.csv


def add_csv_ids_to_set(csvfile_location, destination_set):
    with open(csvfile_location, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for item in csvreader:
            destination_set.add(item[0])


def read_processed_ids_from_results_csv(results_csv):
    processed_ids = set()
    with open(results_csv) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        for line in csvreader:
            processed_ids.add(line[0])
    print("Already processed ids: " + str(len(processed_ids)))
    return processed_ids


def write_summary_row(docid, fragments_total, time_taken, summary_csv):
        with open(summary_csv, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([docid,
                                fragments_total,
                                time_taken])
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
        with open(summary_csv, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['document_id',
                                'fragments_total',
                                'time_taken_s'])


def get_start_params(argv):
    try:
        opts, args = getopt.getopt(argv, "",
                                   ["inputfile="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--inputfile":
            inputfile = arg
    print("inputfile: " + inputfile)
    return inputfile


def write_index_anomaly(bug_report_dict):
    docid = bug_report_dict.get('document_id')
    cluid = bug_report_dict.get('cluster_id')
    find_s = bug_report_dict.get('find_start_index')
    find_e = bug_report_dict.get('find_end_index')
    orig_s = bug_report_dict.get('orig_start_index')
    orig_e = bug_report_dict.get('orig_end_index')
    octa_s = bug_report_dict.get('octavo_start_index')
    octa_e = bug_report_dict.get('octavo_end_index')
    encoding = bug_report_dict.get('encoding')
    text = bug_report_dict.get('text')
    report_fname = ("indexreport_doc" + str(docid) + "-clu" + str(cluid) +
                    ".txt")
    with open(report_fname, 'w') as txtfile:
        txtfile.writelines([
            "docid : " + str(docid) + "\n",
            "cluid : " + str(cluid) + "\n",
            "encod : " + encoding + "\n",
            "find_s: " + str(find_s) + "\n",
            "orig_s: " + str(orig_s) + "\n",
            "find_e: " + str(find_e) + "\n",
            "orig_e: " + str(orig_e) + "\n",
            "octa_s: " + str(octa_s) + "\n",
            "octa_e: " + str(octa_e) + "\n",
            "s_diff: " + str(find_s - orig_s) + "\n",
            "e_diff: " + str(find_e - orig_e) + "\n\n",
            text]
            )


inputfile = get_start_params(sys.argv[1:])
outputprefix = inputfile[:-4]
outputpath = 'output/octavo_indices/' + outputprefix + '/'
create_dir_if_not_exists(outputpath)

ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(timeout=600)

fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "clusterID", "text",
                     "startIndex", "endIndex"]

ids_to_process = set()

add_csv_ids_to_set('data/eccoids/' + inputfile, ids_to_process)
# add_csv_ids_to_set('data/ecco2_ids.csv', ids_to_process)

summary_csv = outputpath + 'summary.csv'
prepare_summary_csv(summary_csv)

# get processed ids from summary.
processed_ids = read_processed_ids_from_results_csv(summary_csv)
docids_asciimap = read_docid_asciimap_csv('data/eccoids/asciilines.csv')

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
    while retries < 21:
        try:
            docid_clusterdata = (
                cluster_api_client.get_cluster_data_for_document_id(
                    docid_to_process, fields=field_eccocluster))
        except ValueError:
            print("Request probably timed out or something." +
                  " Retrying in 5 secs. Retries: " + str(retries) + "/20")
            sleep(5)
            retries += 1
            if retries == 21:
                print("That's too many!")
                sys.exit("Aargh! Errors!")
            continue
        else:
            print("Got cluster data...")
            break

    # we should have the good response now. Yay
    docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid)
    docid_fulltext_text = docid_fulltext_data.get('text')

    # Exactly 1 id is missing from the clusterdata. Go figure.
    if docid == "1563300700":
        docid_ascii = None
    else:
        docid_ascii = docids_asciimap.get(docid)

    # start = timer()
    docid_indexmap_ascii = get_doctext_indexmap(
        orig_text=docid_fulltext_text, method_ascii=True)
    docid_indexmap_unicode = get_doctext_indexmap(
        orig_text=docid_fulltext_text, method_ascii=False)
    # end = timer()
    # print("Indexmaps took " + str(round((end - start), 2)) + "s")

    start = timer()
    docid_fragments = get_fragmentlist(docid_clusterdata,
                                       docid_fulltext_data,
                                       docid_indexmap_ascii,
                                       docid_indexmap_unicode,
                                       docid_is_ascii=docid_ascii)
    end = timer()
    time_taken = round((end - start), 2)
    print("Fragments took " + str(time_taken) + "s")

    docid_fragments_amount = len(docid_fragments)

    fragment_results = []

    for fragment in docid_fragments:
        fragment_data = {'cluster_id': fragment.cluster_id,
                         'document_id': fragment.ecco_id,
                         'octavo_start_index': fragment.octavo_start_index,
                         'octavo_end_index': fragment.octavo_end_index,
                         'orig_start_index': fragment.start_index,
                         'orig_end_index': fragment.end_index,
                         'find_start_index': fragment.find_start_index,
                         'find_end_index': fragment.find_end_index,
                         'encoding': fragment.is_ascii,
                         'encoding_mixup': fragment.encoding_mixup,
                         'fragtext': fragment.text}
        fragment_results.append(fragment_data)

    # write results into csv file. first 4 digits docid separate files.
    docid_filepart = docid_to_process[:4]
    results_csv = (outputpath +
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
            # if (result.get('orig_start_index') -
            #     result.get('find_start_index')) != (
            #     result.get('orig_end_index') -
            #         result.get('find_end_index')):
            # if (result.get('orig_start_index') -
            #     result.get('find_start_index') != 0) or (
            #     result.get('orig_end_index') -
            #         result.get('find_end_index') != 0):
            # if (result.get('encoding_mixup') is True):
            #     print("encoding mixup!")
            #     bug_report_dict = (
            #         {'document_id': result.get('document_id'),
            #          'cluster_id': result.get('cluster_id'),
            #          'find_start_index': result.get('find_start_index'),
            #          'find_end_index': result.get('find_end_index'),
            #          'orig_start_index': result.get('orig_start_index'),
            #          'orig_end_index': result.get('orig_end_index'),
            #          'octavo_start_index': result.get('octavo_start_index'),
            #          'octavo_end_index': result.get('octavo_end_index'),
            #          'encoding': result.get('encoding'),
            #          'text': result.get('fragtext')})
            #     write_index_anomaly(bug_report_dict)
        print("docid: " + docid_to_process + ' results written to ' +
              results_csv)

    write_summary_row(docid_to_process, docid_fragments_amount,
                      time_taken, summary_csv)

    # preloading should have finished while processing previous doc.
    processed_ids.add(docid_to_process)

    # docid_preloaded = docid_to_preload
