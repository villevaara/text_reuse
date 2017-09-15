import time

from lib.headerdata import get_headers_for_document_id
from lib.octavo_api_client import (OctavoEccoClient,
                                   OctavoEccoClusterClient)
from lib.fragmentlists import FragmentList
from tr_cluster import TextReuseCluster

document_id = "0145100105"  # hume history 1778, 5/8

cluster_api_client = OctavoEccoClusterClient(limit=-1, timeout=600)
ecco_api_client = OctavoEccoClient()
document_data = ecco_api_client.get_text_for_document_id(document_id)
document_text = document_data.get('text')


headerdata = get_headers_for_document_id(document_id)

cluster_data = cluster_api_client.get_wide_cluster_data_for_document_id(
    document_id)

fragment_list = FragmentList(cluster_data, seed_docid=document_id)
fragment_list.add_metadata()
fragment_list.add_headerdata(headerdata, document_id)
unique_authors = fragment_list.get_unique_authors()
unique_cluster_ids = fragment_list.get_unique_cluster_ids()


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

cluster_list = get_cluster_list(fragment_list, add_cluster_groups=True)
