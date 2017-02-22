import json
import glob
import csv
import time
from meta_clusters import MetaCluster
from text_reuse_common import (
    load_good_metadata
)


def get_meta_cluster(single_cluster_key, single_cluster_value, good_metadata):
    # single_cluster = dict_keys(['Avglength', 'Hits', 'Count'])
    cluster_hits = single_cluster_value.get('Hits')

    estc_ids = set()
    for hit in cluster_hits:
        eccoid = hit.get('book_id')
        hit_metadata = good_metadata.get(eccoid)
        estc_id = hit_metadata.get('estc_id')
        estc_ids.add(estc_id)

    cluster_ids = set([single_cluster_key])
    meta_cluster = MetaCluster(estc_ids, cluster_ids)
    return meta_cluster


def update_metacluster_dict(new_metacluster, metaclusters_dict):

    meta_cluster_key = new_meta_cluster.get_meta_cluster_id()

    if (meta_cluster_key not in metaclusters_dict.keys()):
        metaclusters_dict[meta_cluster_key] = new_meta_cluster
        # print("Adding new cluster: ")
        # print(new_meta_cluster)

    else:
        existing_meta_cluster = metaclusters_dict[meta_cluster_key]
        existing_meta_cluster.cluster_ids.update(
            new_meta_cluster.cluster_ids)
        # print("Key found, augmenting cluster:")
        # print(existing_meta_cluster)

    return metaclusters_dict


start_time = time.time()

good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)

datadir = "data/test/"
filenames = glob.glob(datadir + "clusters_0")
filenames_length = len(filenames)

meta_clusters = {}


for filename in filenames:
    print(filename)
    with open(filename) as cluster_data_file:
        cluster_data = json.load(cluster_data_file)

        for key, value in cluster_data.items():

            new_meta_cluster = get_meta_cluster(key, value, good_metadata)
            meta_clusters = update_metacluster_dict(new_meta_cluster,
                                                    meta_clusters)


print(len(meta_clusters))


meta_clusters2 = meta_clusters
meta_clusters3 = meta_clusters
intersected_clusters = dict(meta_clusters)
i = 0

for long_meta_cluster in meta_clusters2.values():

    if i % 100 == 0:
        print("processing meta cluster: " + str(i))
        print(long_meta_cluster)

    i = i + 1

    for intersection_target in meta_clusters3.values():

        # print(intersection_target)

        if len(long_meta_cluster.estc_ids.intersection(
               intersection_target.estc_ids)) > 0:

            new_meta_cluster_estc_ids = (
                long_meta_cluster.estc_ids.intersection(
                    intersection_target.estc_ids))
            # print(long_meta_cluster.cluster_ids)
            # print(intersection_target.cluster_ids)
            new_meta_cluster_cluster_ids = (
                long_meta_cluster.cluster_ids.union(
                    intersection_target.cluster_ids))
            # print(new_meta_cluster_cluster_ids)

            new_meta_cluster = MetaCluster(new_meta_cluster_estc_ids,
                                           new_meta_cluster_cluster_ids)
            # print(new_meta_cluster)

            intersected_clusters = (
                update_metacluster_dict(new_meta_cluster,
                                        intersected_clusters))


print(len(intersected_clusters))


with open('meta_clusters.json', 'w') as outfile:
    dump_list = []
    for meta_cluster in intersected_clusters.values():
        dump_list.append(meta_cluster.get_dict_for_dump())
    json.dump(dump_list, outfile)


def write_meta_clusters_dict_as_csv(meta_clusters_dict, filename):
    with open(filename, 'w') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['key', 'estc_ids', 'cluster_ids',
                             'estc_id_amount',
                             'cluster_id_amount'])
        for meta_cluster in meta_clusters_dict.values():
            csv_writer.writerow([meta_cluster.get_meta_cluster_id(),
                                 meta_cluster.get_estc_ids_str(),
                                 meta_cluster.get_cluster_ids_str(),
                                 meta_cluster.get_book_amount(),
                                 meta_cluster.get_cluster_amount()])


write_meta_clusters_dict_as_csv(intersected_clusters, 'meta_clusters.csv')

end_time = time.time()
print("time elapsed: " + str(end_time - start_time))
