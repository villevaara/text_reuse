from lib.text_reuse_octavoapi_common import (
    get_wide_cluster_data_for_document_id_from_api,
    )
from lib.tr_fragment import TextReuseFragment
from lib.text_reuse_common import (
    load_good_metadata
    )


def get_fragmentlist(cluster_data):
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
    return fragment_list


def get_fragments_of_document_id(fragment_list, document_id):
    filtered_list = []
    for fragment in fragment_list:
        if fragment.ecco_id == document_id:
            filtered_list.append(fragment)
    return filtered_list


# get metadata
print("Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)


# get doc from api
document_id = "0429000102"  # hume history, tudor vol2 (elizabeth)
# document_text = get_text_for_document_id_from_api(document_id)
cluster_data = get_wide_cluster_data_for_document_id_from_api(
    document_id, testing=True)
fragment_list = get_fragmentlist(cluster_data)

original_document_fragments = (
    get_fragments_of_document_id(fragment_list, document_id))


# get metadatalist of clusters:
# chronologically first fragment in cluster,
# cluster first year,
# cluster last year,
# cluster document_ids,
# cluster_years ?
# cluster first document_id
# cluster length
# books in cluster not original id / by original author
# ???
