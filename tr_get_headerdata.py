import getopt
import sys
import time
from copy import deepcopy

from lib.tr_fragment import TextReuseFragment
from lib.tr_cluster import TextReuseCluster

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.text_reuse_common import (
    load_good_metadata
    )

from lib.headerdata import (
    get_headers_for_document_id,
    get_header_summary_data,
    )

from lib.output_csv import (
    write_cluster_list_results_csv,
    write_cluster_coverage_as_csv,
    write_header_summarydata_csv,
    write_document_text_with_coverage_highlight,
    )

from lib.fragmentlists import FragmentList


def get_multi_id_fragmentlist(cluster_data, get_octavo_indices=False,
                              window_size=0, context_sole_id=""):
    print("> Getting fragment list ...")

    headerdata = None
    if context_sole_id is not "":
        # ecco_api_client = OctavoEccoClient()
        # document_data = ecco_api_client.get_text_for_document_id(
        #     context_sole_id)
        # # document_data = get_text_for_document_id_from_api(context_sole_id)
        # document_text = document_data.get('text')
        headerdata = get_headers_for_document_id(context_sole_id)

    cluster_data_length = len(cluster_data) - 1
    fragment_list = []
    i = 0
    print("items in list: " + str(len(cluster_data)))

    if context_sole_id != "":
        ecco_api_client = OctavoEccoClient()
        document_text_data = (
            ecco_api_client.get_text_for_document_id(context_sole_id))

    for item in cluster_data:
        print("Processing item: " + str(i) +
              " / " + str(cluster_data_length))
        print("itemID: " + item.get('documentID'))
        i = i + 1
        fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                     cluster_id=item.get('clusterID'),
                                     text=item.get('text'),
                                     start_index=item.get('startIndex'),
                                     end_index=item.get('endIndex'))
        fragment.add_metadata(good_metadata)
        if (context_sole_id == "") or (context_sole_id == fragment.ecco_id):
            fragment.add_context(window_size=window_size,
                                 force_octavo_search=True,
                                 get_octavo_indices=get_octavo_indices,
                                 headerdata_source=headerdata,
                                 document_text_data=document_text_data)
        fragment_list.append(fragment)
    print("  >> Done!")
    return fragment_list


def get_fragments_of_document_id(fragment_list, document_id):
    filtered_list = []
    for fragment in fragment_list:
        if fragment.ecco_id == document_id:
            filtered_list.append(fragment)
    return filtered_list


def get_fragments_of_cluster_id(fragment_list, cluster_id):
    filtered_list = []
    for fragment in fragment_list:
        if str(fragment.cluster_id) == str(cluster_id):
            filtered_list.append(fragment)
    return filtered_list


def get_cluster_list(fragment_list, add_cluster_groups=True):
    print("> Getting cluster list ...")
    cluster_ids = fragment_list.get_unique_cluster_ids()
    cluster_ids_length = len(cluster_ids)
    cluster_list = []

    start = time.time()
    whole_start = time.time()
    i = 0
    for cluster_id in cluster_ids:
        i = i + 1
        if i % 100 == 0:
            end = time.time()
            print("  >> Creating cluster objects: " +
                  str(i) + " / " + str(cluster_ids_length) +
                  " -- Took: " + str(round((end - start), 1)) + "s")
            start = time.time()

        fragments = fragment_list.get_fragments_of_cluster_id(cluster_id)
        # # remove found elements to speed up things
        # # shaves off about 1/3 of the time
        # for fragment in fragments:
        #     fragment_list.remove(fragment)
        cluster = TextReuseCluster(document_id, cluster_id, fragments)
        if add_cluster_groups:
            cluster.add_cluster_groups()
        cluster_list.append(cluster)

    print("  >> Done!")
    print("  >> Took: " +
          str(round((time.time() - whole_start), 1)) + "s in total.")
    return cluster_list


def get_cluster_list_with_filters(cluster_list,
                                  require_orig_author_first=False,
                                  filter_out_author="",
                                  author_ignore_id="",
                                  filter_out_year_below=-1,
                                  filter_out_year_above=-1,):
    print("> Filtering cluster list ...")
    cluster_list_results = []

    for cluster in cluster_list:
        results_cluster = deepcopy(cluster)
        if require_orig_author_first:
            if not results_cluster.orig_author_first():
                continue
        if filter_out_author != "":
            results_cluster.filter_out_author(filter_out_author,
                                              author_ignore_id)
        if filter_out_year_above != -1:
            results_cluster.filter_out_year_above(filter_out_year_above)
        if filter_out_year_below != -1:
            results_cluster.filter_out_year_below(filter_out_year_below)

        if len(results_cluster.fragment_list) > 0:
            cluster_list_results.append(results_cluster)

    print("  >> Done!")
    return cluster_list_results


def get_start_params(argv):
    document_id = "0145100107"
    filter_out_author = "Hume, David (1711-1776)"
    author_ignore_id = ""
    require_orig_author_first = False
    filter_out_year_below = -1
    filter_out_year_above = -1
    testing_amount = -1

    try:
        opts, args = getopt.getopt(argv, "",
                                   ["document_id=",
                                    "filter_out_author=",
                                    "author_ignore_id=",
                                    "require_orig_author_first=",
                                    "filter_out_year_below=",
                                    "filter_out_year_above=",
                                    "testing_amount="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--document_id":
            document_id = arg
        elif opt == "--filter_out_author":
            filter_out_author = arg
        elif opt == "--author_ignore_id":
            author_ignore_id = arg
        elif opt == "--require_orig_author_first":
            require_orig_author_first = True
        elif opt == "--filter_out_year_below":
            filter_out_year_below = arg
        elif opt == "--filter_out_year_above":
            filter_out_year_above = arg
        elif opt == "--testing_amount":
            testing_amount = arg

    author_pathpart = filter_out_author.lower()
    author_pathpart = author_pathpart.split('(')[0].strip()
    author_pathpart = author_pathpart.replace(', ', '_')

    if filter_out_year_below != -1:
        year_below_pathpart = ("-" + str(filter_out_year_below) + "_out_below")
    else:
        year_below_pathpart = ""

    if filter_out_year_above != -1:
        year_above_pathpart = ("-" + str(filter_out_year_above) + "_out_above")
    else:
        year_above_pathpart = ""

    if require_orig_author_first:
        require_orig_author_first_pathpart = "-required_first"
    else:
        require_orig_author_first_pathpart = ""

    outpath_prefix = (
        author_pathpart + "-" +
        document_id +
        year_below_pathpart +
        year_above_pathpart +
        require_orig_author_first_pathpart)

    print("params:" + "\n" +
          "document_id: " + str(document_id) + "\n" +
          "filter_out_author: " + str(filter_out_author) + "\n" +
          "require_orig_author_first: " + str(require_orig_author_first) +
          "\n" +
          "filter_out_year_below: " + str(filter_out_year_below) + "\n" +
          "filter_out_year_above: " + str(filter_out_year_above) + "\n" +
          "testing_amount: " + str(testing_amount) + "\n")

    return(document_id,
           filter_out_author,
           author_ignore_id,
           require_orig_author_first,
           filter_out_year_below,
           filter_out_year_above,
           outpath_prefix,
           testing_amount)


def get_cluster_coverage_data(document_id_to_cover,
                              cluster_list,
                              ecco_api_client):
    document_text = ecco_api_client.get_text_for_document_id(
        document_id_to_cover).get('text')
    document_length = len(document_text)

    cluster_coverage = [0] * document_length
    # cluster_text = [""] * document_length

    for cluster in cluster_list:
        start = cluster.group_start_index
        end = cluster.group_end_index
        length = cluster.get_length()
        # print("s: " + str(start) + " e: " +
        #       str(end) + " l: " + str(length))
        for i in range(start, end + 1):
            cluster_coverage[i] = cluster_coverage[i] + length

    return cluster_coverage


def get_document_text_with_coverage_highlight(document_id,
                                              coverage_data,
                                              ecco_api_client):
    document_text = ecco_api_client.get_text_for_document_id(
        document_id).get('text')
    document_text_list = list(document_text)
    document_length = len(document_text_list)

    for char_index in range(0, document_length):
        if coverage_data[char_index] == 0:
            document_text_list[char_index] = (
                document_text_list[char_index].upper())

    document_text_results = "".join(document_text_list)
    return document_text_results


# get fragments with:
# not hume
# after 1761 (last part of original history published)

# create cluster summary with
# find all headers, even without hits
# for each header, count fragments hitting conditions

# below by years:
# both before and after 1761
# group_id, group_name, unique cluster ids, cluster fragments (exl. Hume),
# fragments (exl Hume & NA)

# -----------------------------------
# legacy, params from command line now
# -----------------------------------
# document_id = "0145100107"  # hume history 1778, 5/8 tudor2 elizabeth
# author_to_filter = "Hume, David (1711-1776)"
# filter_out_year_below = -1
# outpath_prefix = "history5_8_not_hume"

# document_id = 1611003000  # madeville fable 1714


(
    document_id,
    author_to_filter,
    author_ignore_id,
    require_orig_author_first,
    filter_out_year_below,
    filter_out_year_above,
    outpath_prefix,
    testing_amount
    ) = get_start_params(sys.argv[1:])


# get metadata
print("> Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)
print("  >> Done!")

# get doc from api

ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(limit=testing_amount)

cluster_data = cluster_api_client.get_wide_cluster_data_for_document_id(
    document_id)

fragment_list = FragmentList(cluster_data, document_id)
fragment_list.add_metadata()

# fragment_list = get_multi_id_fragmentlist(cluster_data,
#                                           get_octavo_indices=True,
#                                           window_size=0,
#                                           context_sole_id=document_id)

cluster_list = get_cluster_list(fragment_list)

cluster_list_filtered = get_cluster_list_with_filters(
    cluster_list=cluster_list,
    filter_out_author=author_to_filter,
    require_orig_author_first=require_orig_author_first,
    author_ignore_id=author_ignore_id,
    filter_out_year_below=filter_out_year_below,
    filter_out_year_above=filter_out_year_above)

coverage_data = get_cluster_coverage_data(document_id, cluster_list_filtered,
                                          ecco_api_client)
doctext_with_coverage_highlight = (
    get_document_text_with_coverage_highlight(document_id, coverage_data,
                                              ecco_api_client))

header_summarydata = get_header_summary_data(cluster_list_filtered,
                                             document_id)


write_cluster_list_results_csv(cluster_list_filtered,
                               outpath_prefix,
                               include_date=True)
write_cluster_coverage_as_csv(coverage_data,
                              outpath_prefix,
                              include_date=True)
write_document_text_with_coverage_highlight(doctext_with_coverage_highlight,
                                            outpath_prefix,
                                            include_date=True)
write_header_summarydata_csv(header_summarydata,
                             outpath_prefix,
                             outfile_suffix="",
                             include_date=True)

# TODO
# * clusterset -class
#   * name, list of tr_clusters (with lists of fragments)
#   * filters used (filter history)
#   * method with which cluster group name was created
#   * method for saving clusterset as csv

# RESULT DATA:
# total coverage of document by character
# by others
# by all editions of hume -> what parts have been revised?
