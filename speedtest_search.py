from timeit import default_timer as timer

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

# from lib.tr_fragment import TextReuseFragment

from lib.fragmentlists import (
    get_fragmentlist,
    get_doctext_indexmap)

from lib.headerdata_dump_common import read_docid_asciimap_csv


def compare_octavo_text_for_fragment(fragment, octavo_text):
    print("Fragment text:\n")
    print(fragment.text)
    print("Octavo text:\n")
    print(octavo_text[fragment.octavo_start_index:fragment.octavo_end_index])


ecco_api_client = OctavoEccoClient()
cluster_api_client = OctavoEccoClusterClient(timeout=600)

fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "clusterID", "text",
                     "startIndex", "endIndex"]

# docid = "1042800201"  # 220
# docid = "1529201400"  # 49
docids_asciimap = read_docid_asciimap_csv('data/eccoids/asciilines.csv')

start = timer()
docid = "1275801800"
# docid = "0459801102"
docid_clusterdata = (
    cluster_api_client.get_cluster_data_for_document_id(
        docid, field_eccocluster))
end = timer()
print("Clusterdata took " + str(round((end - start), 2)) + "s")

# testing:
# start = timer()
# get(api_request)
# end = timer()
# print("Clusterdata took " + str(round((end - start), 2)) + "s")


docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid)
docid_fulltext_text = docid_fulltext_data.get('text')
docid_ascii = docids_asciimap.get(docid)

start = timer()
docid_indexmap_ascii = get_doctext_indexmap(orig_text=docid_fulltext_text,
                                            method_ascii=True)
docid_indexmap_unicode = get_doctext_indexmap(orig_text=docid_fulltext_text,
                                              method_ascii=False)
end = timer()
print("Indexmaps took " + str(round((end - start), 2)) + "s")


start = timer()
docid_fragments = get_fragmentlist(docid_clusterdata,
                                   docid_fulltext_data,
                                   docid_indexmap_ascii,
                                   docid_indexmap_unicode,
                                   docid_ascii)
end = timer()
print("Fragments took " + str(round((end - start), 2)) + "s")

# compare_octavo_text_for_fragment(docid_fragments[0], docid_fulltext_text)

i = 0
for docid in docid_fragments:
    # print("from_api:  " + str(docid.start_index))
    # print("from_find: " + str(docid.find_start_index))
    if (docid.cluster_id) == 8727062:
        print(str(i))
    i += 1
