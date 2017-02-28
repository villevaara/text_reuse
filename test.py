import json
from text_reuse_common import (
    load_good_metadata,
    write_results_txt,
    process_cluster
)

search_string = 'Hume, David'
search_field = 'estc_author'
savedir = 'hume'
need_others = True
min_count = 2
min_authors = 1
datadir = "data/test/"
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)
cluster_data_file = open(datadir + "clusters_0")
cluster_data = json.load(cluster_data_file)
hit_clusters, totalHits = process_cluster(cluster_data, good_metadata,
                                          search_string, search_field,
                                          need_others=need_others,
                                          case_sensitive=False,
                                          min_authors=min_authors,
                                          min_count=min_count)

