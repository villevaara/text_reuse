# import sys
# from copy import deepcopy
# import csv

# from lib.tr_cluster import TextReuseCluster

from lib.octavo_api_client import (
    OctavoEccoClient,
    # OctavoEccoClusterClient
    )

ecco_api_client = OctavoEccoClient()

docids = {
    'carte4': {'id': "0018500104"},
    'guthrie4': {'id': "1679100104"},
    'hume6': {'id': "0145100106"},
    'rapin12': {'id': "1394000112"},
}

for key, value in docids.items():
    document_data = ecco_api_client.get_text_for_document_id(
        value.get('id'))
    document_text = document_data.get('text')
    document_len = len(document_text)
    docids[key]['text'] = document_text
    docids[key]['length'] = document_len
