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


def get_fragmentlist(cluster_data):
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
        fragment.add_context(window_size=2000, get_octavo_indices=True)
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
    document_id, testing=True, testing_amount=100)
fragment_list = get_fragmentlist(cluster_data)

cluster_ids = set()
for fragment in fragment_list:
    cluster_ids.add(fragment.cluster_id)

clusters = []
for cluster_id in cluster_ids:
    fragments = get_fragments_of_cluster_id(fragment_list, cluster_id)
    cluster = TextReuseCluster(cluster_id, fragments)
    clusters.append(cluster)

# 0672600300
# original_document_fragments = (
#     get_fragments_of_document_id(fragment_list, document_id))

# add cluster groups (=chapter headers)
# could be made method of cluster of main doc_id was saved as object value
for cluster in clusters:
    for fragment in cluster.fragment_list:
        if str(fragment.ecco_id) == document_id:
            cluster.group_name = fragment.preceding_header
            cluster.group_id = fragment.preceding_header_index
            break


# create cluster-header summary:
# 1. find all clusters under same group id
# 2. write those in same csv - name csv by groupid_groupname
clusters_without_author = []
# author_to_filter = "Mandeville, Bernard (1670-1733)"
author_to_filter = "Hume, David (1711-1776)"


for cluster in clusters:
    # cluster_id = cluster.cluster_id
    fragments = cluster.get_fragments_filter_out_author(
        author_to_filter, ignore_id=document_id)
    if len(fragments) > 0:
        cluster_no_author = TextReuseCluster(cluster.cluster_id, fragments)
        cluster_no_author.group_id = cluster.group_id
        cluster_no_author.group_name = cluster.group_name
        clusters_without_author.append(cluster_no_author)

group_ids = set()
for cluster in clusters_without_author:
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
    for cluster in clusters_without_author:
        if cluster.group_id == group_id:
            cluster.write_cluster_csv(outfile, include_header_row=False,
                                      method='a')


outfilepath = "output/" + outpath_prefix + "/first_others/"
create_dir_if_not_exists(outfilepath)
# drop all clusters not starting with fable 1714
for cluster in clusters:
    # first not fable:
    if cluster.fragment_list[0].ecco_id != document_id:
        continue
    # no others than author in
    if cluster.get_number_of_authors() < 2:
        continue
    cluster.write_cluster_csv(outfilepath)


outfilepath = "output/" + outpath_prefix + "/not_first/"
create_dir_if_not_exists(outfilepath)
# drop all clusters starting with fable
for cluster in clusters:
    # first fable:
    if cluster.fragment_list[0].ecco_id == document_id:
        continue
    # no others than mandeville in
    if cluster.get_number_of_authors() < 2:
        continue
    cluster.write_cluster_csv(outfilepath)
