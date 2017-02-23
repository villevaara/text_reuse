import json
import glob
import sys
import getopt
from text_reuse_common import (
    load_good_metadata,
    write_results_txt,
    process_cluster
)


def get_start_params(argv):
    test = False
    search_string = 'Mandeville, Bernard'
    search_field = 'estc_author'
    savedir = 'mandeville'
    need_others = True
    min_count = 2
    min_authors = 1
    try:
        opts, args = getopt.getopt(argv, "tos:f:d:m:a:", [])
        # "test", "search_string=", "search_field=", "savedir="
    except getopt.GetoptError:
        # usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            test = True
        elif opt == '-o':
            need_others = False
        elif opt == '-s':
            search_string = arg
        elif opt == '-f':
            search_field = arg
        elif opt == '-d':
            savedir = arg
        elif opt == '-m':
            min_count = int(arg)
        elif opt == '-a':
            min_authors = int(arg)
    return(test, search_string, search_field, savedir, need_others, min_count, min_authors)

# usage:
# python text-reuse-cur.py -t -s "Hobbes, Thomas" -d hobbes


good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)
test, search_string, search_field, savedir, need_others, min_count, min_authors = get_start_params(sys.argv[1:])
# print(min_count)
# print(type(min_count))

if (test):
    datadir = "data/test/"
    writedir = "output/test/" + savedir
else:
    datadir = "data/min1200/"
    writedir = "output/" + savedir + "/" + savedir

filenames = glob.glob(datadir + "clusters*")
filenames_length = len(filenames)

i = 0
allHits = 0

for filename in filenames:
    with open(filename) as cluster_data_file:
        cluster_data = json.load(cluster_data_file)
        hit_clusters, totalHits = process_cluster(cluster_data, good_metadata,
                                                  search_string, search_field,
                                                  need_others=need_others,
                                                  case_sensitive=False,
                                                  min_authors=min_authors,
                                                  min_count=min_count)
        write_results_txt(hit_clusters, writedir, good_metadata)
        allHits = allHits + totalHits
        i = i + 1
        print("Processed file (" + str(i) + "/" + str(filenames_length) +
              "): " + filename + " --- hits so far: " +
              str(allHits))


# process_cluster(cluster_data)

# print(len(hit_clusters))
# print(hit_clusters.keys())

# TODO
# 'Locke, John'
# 'Smith, Adam'
# 'Grotius, Hugo'
# 'Temple, William'

# DONE
# 'Mandeville, Bernard'
# 'Montesquieu, Charles'
# 'Hobbes, Thomas'
# 'Bayle, Pierre'
