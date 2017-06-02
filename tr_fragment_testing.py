from text_reuse_octavoapi_common import (
    get_text_for_document_id_from_api,
    get_cluster_data_for_document_id_from_api_filters,
    get_wide_cluster_data_for_document_id_from_api)
from tr_fragment import TextReuseFragment
from text_reuse_common import (
    load_good_metadata
    )


# get metadata
print("Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)


# get doc from api
document_id = "0429000102"  # hume history, tudor vol2 (elizabeth)
# document_text = get_text_for_document_id_from_api(document_id)

cluster_data = get_wide_cluster_data_for_document_id_from_api(
    document_id, testing=True)

fragment_list = []
i = 0
print("items in list: " + str(len(cluster_data)))
for item in cluster_data:
    print("Processing item:" + str(i))
    i = i + 1
    fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                 cluster_id=item.get('clusterID'),
                                 text=item.get('text'),
                                 start_index=item.get('startIndex'),
                                 end_index=item.get('endIndex'))
    fragment.add_metadata(good_metadata)
    fragment.add_context(window_size=2000)
    fragment_list.append(fragment)


# enriched_cluster_data = (
#     get_cluster_data_for_document_id_from_api_filters(document_id,
#                                                       good_metadata,
#                                                       not_author=False,
#                                                       # years_min=0,
#                                                       # years_max=20,
#                                                       testing=True))

# hume1 = enriched_cluster_data[0]

# hume_fragment = TextReuseFragment(estc_id=hume1.get('estc_id'),
#                                   ecco_id=hume1.get('document_id'),
#                                   cluster_id=hume1.get('cluster_id'),
#                                   title=hume1.get('title'),
#                                   author=hume1.get('author'),
#                                   year=hume1.get('year'),
#                                   text=hume1.get('text'),
#                                   start_index=hume1.get('startIndex'),
#                                   end_index=hume1.get('endIndex'))

# hume_fragment.add_context(window_size=2000)

