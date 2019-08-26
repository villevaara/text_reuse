# TODO
# * clusterset -class
#   * name, list of tr_clusters (with lists of fragments)
#   * filters used (filter history)
#   * method with which cluster group name was created
#   * method for saving clusterset as csv

from lib.text_reuse_octavoapi_common import (
    get_wide_cluster_data_for_document_id_from_api,
    )
from lib.tr_fragment import TextReuseFragment
from lib.text_reuse_common import (
    load_good_metadata
    )
from lib.tr_cluster import TextReuseCluster
import csv
from lib.utils_common import create_dir_if_not_exists
from copy import deepcopy


def get_fragmentlist(cluster_data, get_octavo_indices=False,
                     window_size=0):
    fragment_list = []
    i = 0
    print("items in list: " + str(len(cluster_data)))
    for item in cluster_data:
        print("Processing item: " + str(i))
        print("itemID: " + item.get('documentID'))
        i = i + 1
        fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                     cluster_id=item.get('clusterID'),
                                     text=item.get('text'),
                                     start_index=item.get('startIndex'),
                                     end_index=item.get('endIndex'))
        fragment.add_metadata(good_metadata)
        fragment.add_context(window_size=window_size,
                             get_octavo_indices=get_octavo_indices)
        fragment_list.append(fragment)
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
    cluster_ids = set()
    for fragment in fragment_list:
        cluster_ids.add(fragment.cluster_id)

    cluster_list = []
    for cluster_id in cluster_ids:
        fragments = get_fragments_of_cluster_id(fragment_list, cluster_id)
        cluster = TextReuseCluster(document_id, cluster_id, fragments)
        cluster.add_cluster_groups()
        cluster_list.append(cluster)

    return cluster_list


# get metadata
print("Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)


# get doc from api
# '0163400107'
# document_id = "0429000102"  # hume history, tudor vol2 (elizabeth)
# document_id = "1611003000"  # madeville fable 1714
document_id = "0145100107"  # hume history 1778, 5/8 tudor2 elizabeth

cluster_data = get_wide_cluster_data_for_document_id_from_api(
    document_id, testing=True, testing_amount=1000)

fragment_list = get_fragmentlist(cluster_data,
                                 get_octavo_indices=False,
                                 window_size=0)

cluster_list = get_cluster_list(fragment_list)

# 0672600300
# original_document_fragments = (
#     get_fragments_of_document_id(fragment_list, document_id))

# create cluster-header summary:
# 1. find all cluster_list under same group id
# 2. write those in same csv - name csv by groupid_groupname

# author_to_filter = "Mandeville, Bernard (1670-1733)"
author_to_filter = "Hume, David (1711-1776)"

# get fragments with:
# not hume
# after 1761 (last part of original history published)

# create cluster summary with
# find all headers, even without hits
# for each header, count fragments hitting conditions

# below by years:
# both before and after 1761
# group_id, group_name, unique cluster ids, cluster fragments (exl. Hume), fragments (exl Hume & NA)


# def get_cluster_list_without_author(cluster_list, filter_out_author):
#     cluster_list_results = []

#     for cluster in cluster_list:
#         fragments_results = cluster.get_fragments_filter_out_author(
#             filter_out_author)
#         if len(cluster_list_results) > 0:
#             cluster_results = TextReuseCluster(document_id,
#                                                cluster.cluster_id,
#                                                fragments_results)
#             cluster_results.group_id = cluster.group_id
#             cluster_results.group_name = cluster.group_name
#             cluster_list_results.append(cluster_list_results)

#     return cluster_list_results


def get_cluster_list_with_filters(cluster_list,
                                  filter_out_author="",
                                  filter_out_year_below=-1,
                                  filter_out_year_above=-1,):
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
            cluster_results = TextReuseCluster(document_id,
                                               cluster.cluster_id,
                                               fragments_results)
            cluster_results.group_id = cluster.group_id
            cluster_results.group_name = cluster.group_name
            cluster_list_results.append(cluster_list_results)

    return cluster_list_results


cluster_list_without_author = []

# for cluster in cluster_list:
#     fragments_no_author = cluster.get_fragments_filter_out_author(
#         author_to_filter,
#         # ignore_id=document_id
#         )
#     if len(fragments_no_author) > 0:
#         cluster_no_author = TextReuseCluster(document_id,
#                                              cluster.cluster_id,
#                                              fragments_no_author)
#         cluster_no_author.group_id = cluster.group_id
#         cluster_no_author.group_name = cluster.group_name
#         cluster_list_without_author.append(cluster_no_author)

group_ids = set()
for cluster in cluster_list_without_author:
    group_ids.add(cluster.group_id)


outpath_prefix = "history5_8_not_hume"

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
    for cluster in cluster_list_without_author:
        if cluster.group_id == group_id:
            cluster.write_cluster_csv(outfile, include_header_row=False,
                                      method='a')


outfilepath = "output/" + outpath_prefix + "/first_others/"
create_dir_if_not_exists(outfilepath)
# drop all cluster_list not starting with fable 1714
for cluster in cluster_list:
    # first not fable:
    if cluster.fragment_list[0].ecco_id != document_id:
        continue
    # no others than author in
    if cluster.get_number_of_authors() < 2:
        continue
    cluster.write_cluster_csv(outfilepath)


outfilepath = "output/" + outpath_prefix + "/not_first/"
create_dir_if_not_exists(outfilepath)
# drop all cluster_list starting with fable
for cluster in cluster_list:
    # first fable:
    if cluster.fragment_list[0].ecco_id == document_id:
        continue
    # no others than mandeville in
    if cluster.get_number_of_authors() < 2:
        continue
    cluster.write_cluster_csv(outfilepath)
