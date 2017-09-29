from lib.octavo_api_client import OctavoEccoClusterClient

cluster_api_client = OctavoEccoClusterClient(limit=-1,
                                             timeout=600)

document_id = "1394000110"
cluster_ids = cluster_api_client.get_cluster_ids_list_for_document_id(
    document_id)
cluster_data = cluster_api_client.get_cluster_data_for_cluster_id_list(
    cluster_ids)
