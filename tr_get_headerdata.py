
from lib.text_reuse_octavoapi_common import (
    get_wide_cluster_data_for_document_id_from_api,
    get_headers_from_document_text,
    get_text_for_document_id_from_api
    )
from lib.tr_fragment import TextReuseFragment
from lib.text_reuse_common import (
    load_good_metadata
    )
from lib.tr_cluster import TextReuseCluster
import csv
from lib.utils_common import create_dir_if_not_exists
from copy import deepcopy
import getopt
import sys


def get_fragmentlist(cluster_data, get_octavo_indices=False,
                     window_size=0, context_sole_id=""):
    print("> Getting fragment list ...")

    headerdata = None
    if context_sole_id is not "":
        document_data = get_text_for_document_id_from_api(context_sole_id)
        document_text = document_data.get('text')
        headerdata = get_headers_from_document_text(document_text)

    cluster_data_length = len(cluster_data) - 1
    fragment_list = []
    i = 0
    print("items in list: " + str(len(cluster_data)))
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
                                 get_octavo_indices=get_octavo_indices,
                                 headerdata_source=headerdata)
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
    cluster_ids = set()
    fragment_list_length = len(fragment_list)
    i = 0
    for fragment in fragment_list:
        i = i + 1
        if i % 100 == 0:
            print(str(i) + " / " + str(fragment_list_length))
        cluster_ids.add(fragment.cluster_id)

    cluster_ids_length = len(cluster_ids)
    i = 0
    cluster_list = []
    # this is really slow!
    # -what about taking out values in list that already
    # got caught?
    for cluster_id in cluster_ids:
        i = i + 1
        if i % 100 == 0:
            print(str(i) + " / " + str(cluster_ids_length))
        fragments = get_fragments_of_cluster_id(fragment_list, cluster_id)
        cluster = TextReuseCluster(document_id, cluster_id, fragments)
        cluster.add_cluster_groups()
        cluster_list.append(cluster)

    print("  >> Done!")
    return cluster_list


def get_cluster_list_with_filters(cluster_list,
                                  filter_out_author="",
                                  filter_out_year_below=-1,
                                  filter_out_year_above=-1,):
    print("> Filtering cluster list ...")
    cluster_list_results = []

    for cluster in cluster_list:
        results_cluster = deepcopy(cluster)
        if filter_out_author != "":
            results_cluster.filter_out_author(filter_out_author)
        if filter_out_year_above != -1:
            results_cluster.filter_out_year_above(filter_out_year_above)
        if filter_out_year_below != -1:
            results_cluster.filter_out_year_below(filter_out_year_below)

        if len(results_cluster.fragment_list) > 0:
            cluster_list_results.append(results_cluster)

    print("  >> Done!")
    return cluster_list_results


def write_cluster_list_results_csv(cluster_list, outpath_prefix):
    print("> Writing cluster list as csv ...")
    group_ids = set()
    for cluster in cluster_list:
        group_ids.add(cluster.group_id)

    for group_id in group_ids:
        outfilepath = "output/" + outpath_prefix + "/by_header/"
        create_dir_if_not_exists(outfilepath)
        outfile = outfilepath + str(group_id) + ".csv"
        with open(outfile, 'w') as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow(['cluster_id',
                                'ecco_id',
                                'estc_id',
                                'author',
                                'title',
                                'preceding_header',
                                'year',
                                'location',
                                'text_before', 'text', 'text_after',
                                'preceding_header_index',
                                'start_index', 'end_index',
                                'find_start_index', 'find_end_index',
                                'document_length', 'fragment_indices',
                                'document_collection',
                                'group_name', 'group_id'])
        for cluster in cluster_list:
            if cluster.group_id == group_id:
                cluster.write_cluster_csv(outfile, include_header_row=False,
                                          method='a')
    print("  >> Done!")


def get_start_params(argv):
    document_id = "0145100107"
    filter_out_author = "Hume, David (1711-1776)"
    filter_out_year_below = 1761

    try:
        opts, args = getopt.getopt(argv, "",
                                   ["document_id=",
                                    "filter_out_author=",
                                    "filter_out_year_below="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--document_id":
            document_id = arg
        elif opt == "--filter_out_author":
            filter_out_author = arg
        elif opt == "--filter_out_year_below":
            filter_out_year_below = arg

    author_pathpart = filter_out_author.lower()
    author_pathpart = author_pathpart.split('(')[0].strip()
    author_pathpart = author_pathpart.replace(', ', '_')
    year_below_pathpart = (str(filter_out_year_below) + "_below")
    outpath_prefix = (
        author_pathpart + "-" + document_id + "-" + year_below_pathpart)

    return(document_id,
           filter_out_author,
           filter_out_year_below,
           outpath_prefix)


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

document_id = "0145100107"  # hume history 1778, 5/8 tudor2 elizabeth
author_to_filter = "Hume, David (1711-1776)"
filter_out_year_below = 1761
outpath_prefix = "history5_8_not_hume"

(
    document_id,
    author_to_filter,
    filter_out_year_below,
    outpath_prefix) = get_start_params(sys.argv[1:])


# get metadata
print("> Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)
print("  >> Done!")

# get doc from api

cluster_data = get_wide_cluster_data_for_document_id_from_api(
    document_id, testing=False, testing_amount=1000)

fragment_list = get_fragmentlist(cluster_data,
                                 get_octavo_indices=False,
                                 window_size=0,
                                 context_sole_id=document_id)

cluster_list = get_cluster_list(fragment_list)

cluster_list_filtered = get_cluster_list_with_filters(
    cluster_list=cluster_list,
    filter_out_author=author_to_filter,
    filter_out_year_below=1761)

write_cluster_list_results_csv(cluster_list_filtered, outpath_prefix)

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

# outfilepath = "output/" + outpath_prefix + "/first_others/"
# create_dir_if_not_exists(outfilepath)
# # drop all cluster_list not starting with fable 1714
# for cluster in cluster_list:
#     # first not fable:
#     if cluster.fragment_list[0].ecco_id != document_id:
#         continue
#     # no others than author in
#     if cluster.get_number_of_authors() < 2:
#         continue
#     cluster.write_cluster_csv(outfilepath)


# outfilepath = "output/" + outpath_prefix + "/not_first/"
# create_dir_if_not_exists(outfilepath)
# # drop all cluster_list starting with fable
# for cluster in cluster_list:
#     # first fable:
#     if cluster.fragment_list[0].ecco_id == document_id:
#         continue
#     # no others than mandeville in
#     if cluster.get_number_of_authors() < 2:
#         continue
#     cluster.write_cluster_csv(outfilepath)
