from lib.octavo_api_client import OctavoEccoClusterClient

cluster_api_client = OctavoEccoClusterClient(limit=-1,
                                             timeout=600)

document_id = "1394000110"

cluster_ids = cluster_api_client.get_cluster_ids_list_for_document_id(
    document_id)
cluster_ids_sample = cluster_ids[0:10]
cluster_data = cluster_api_client.get_cluster_data_for_cluster_id_list(
    cluster_ids)


# another test here

# from requests import get
# from lib.text_reuse_common import load_good_metadata


# request = "https://vm0824.kaj.pouta.csc.fi/octavo/eccocluster/search?query=documentID:0145000201&field=clusterID&field=documentID&field=count&field=startIndex&limit=-1&timeout=600&field=author"
# results = get(request).json().get('results').get('docs')

# # cluster_ids = []
# # for result in results:
# #     cluster_ids.append(result.get('clusterID'))
# # cluids_set = set(cluster_ids)


# header470_results = []
# header470_cluids = []
# for result in results:
#     if result.get('startIndex') >= 470 and result.get('startIndex') < 17497:
#         header470_results.append(result)
#         header470_cluids.append(result.get('clusterID'))

# h470_cluids_set = set(header470_cluids)


# h470_all = []
# for cluid in h470_cluids_set:
#     print(str(cluid))
#     request = "https://vm0824.kaj.pouta.csc.fi/octavo/eccocluster/search?query=clusterID:" + str(cluid) + "&field=clusterID&field=documentID&field=count&field=startIndex&limit=-1&timeout=600&field=author"
#     results = get(request).json().get('results').get('docs')
#     h470_all.extend(results)


# good_metadata = load_good_metadata("data/metadata/good_metadata.json")

# nothumebooks = []

# for result in h470_all:
#     if not (good_metadata.get(result.get('documentID')).get('estc_author') == 'Hume, David (1711-1776)'):
#         if ((good_metadata.get(result.get('documentID')).get('estc_publication_year') != 'NA') and
#             int(good_metadata.get(result.get('documentID')).get('estc_publication_year')) >= 1754):
#                 nothumebooks.append(result)

