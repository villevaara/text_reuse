
import glob
import gzip
import json
import csv
# import operator
from text_reuse_common import write_single_cluster_txt


def get_cluster(cluster_index, gz_filename):
    with gzip.open(gz_filename, 'rt') as cluster_data_file:
        cluster_group_data = json.load(cluster_data_file)
        cluster_data = cluster_group_data.get(cluster_index)
        return {'cluster_index': cluster_index,
                'gz_filename': gz_filename,
                'cluster_data': cluster_data}


# create index of clusters
# cluster_id, avglength, count, directory, gzfile

# datadir = "data/testgz/"
# clusterdir = "min-test"
clusterdir = "min1000"
datadir = "data/indexed_clusters/" + clusterdir + "/"
filenames = glob.glob(datadir + "clusters*")
# datadir = "data/indexed_clusters/"
# subdirs = glob.glob(datadir + "min*" + "/")
# filenames = []
# for subdir in subdirs:
#     filenames.extend(glob.glob(subdir + "clusters*"))
writedir = "output/index/"
outfile = writedir + "index_" + clusterdir + ".csv"
sorted_outfile = writedir + "index_" + clusterdir + "_sorted_top1000.csv"
sorted_outfile2 = writedir + "index_" + clusterdir + "_sorted_len_top1000.csv"

filenames_length = len(filenames)

i = 0

for filename in filenames:
    with gzip.open(filename, 'rt') as cluster_data_file:
        cluster_data = json.load(cluster_data_file)

        with open(outfile, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            # csvwriter.writerow(['cluster_id', 'count', 'length', 'filename'])

            for key, value in cluster_data.items():
                cluster_id = str(key)
                count = str(value.get('Count'))
                length = str(value.get('Avglength'))
                filename = str(filename)
                csvwriter.writerow([cluster_id, count, length, filename])

        i = i + 1
        print("Processed file (" + str(i) + "/" + str(filenames_length) +
              "): " + filename)


print("sorting data, taking top 1000 by count")

csvreader = csv.reader(open(outfile, 'r', newline=''), delimiter=',')
sorted_csvdata = sorted(csvreader,
                        key=lambda row: int(row[1]),
                        reverse=True)
sorted_csvdata = sorted_csvdata[0:1000]

print("writing sorted data by count")

with open(sorted_outfile, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['cluster_id', 'count', 'length', 'filename'])

    for row in sorted_csvdata:
        csvwriter.writerow(row)


print("sorting data, taking top 1000 by length")

csvreader = csv.reader(open(outfile, 'r', newline=''), delimiter=',')
sorted_csvdata_len = sorted(csvreader,
                            key=lambda row: int(row[2]),
                            reverse=True)
sorted_csvdata_len = sorted_csvdata_len[0:1000]

print("writing sorted data")

with open(sorted_outfile2, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['cluster_id', 'count', 'length', 'filename'])

    for row in sorted_csvdata_len:
        csvwriter.writerow(row)


top20 = sorted_csvdata[0:20]

for row in top20:
    cluster_data_dict = get_cluster(row[0], row[3])
    # print(cluster_data_dict)
    write_filename = ("output/index/top20" +
                      clusterdir + "/" + str(row[0]) + ".txt")
    write_single_cluster_txt(cluster_data_dict, write_filename)


top20_len = sorted_csvdata_len[0:20]

for row in top20_len:
    cluster_data_dict = get_cluster(row[0], row[3])
    # print(cluster_data_dict)
    write_filename = ("output/index/top20len" +
                      clusterdir + "/" + str(row[0]) + ".txt")
    write_single_cluster_txt(cluster_data_dict, write_filename)
