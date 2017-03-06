import json
import glob
import sys
import getopt
import gzip
import time
import datetime
from text_reuse_common import (
    load_good_metadata,
    write_results_txt,
    process_cluster
)


def get_start_params(argv):
    test = False
    # search_string = 'Mandeville, Bernard'
    # search_field = 'author'
    savedir = 'mandeville'
    need_others = True
    min_count = 2
    min_authors = 1
    primus = 'any'
    # input_dir = 'min100'
    search_author = 'NONE'
    search_title = 'NONE'
    search_estcid = 'NONE'

    try:
        opts, args = getopt.getopt(argv,
                                   "top:d:m:a:",
                                   ["author=", "title=", "estcid="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            test = True
        elif opt == '-o':
            need_others = False
        elif opt == '-p':
            primus = arg
        elif opt == '-d':
            savedir = arg
        elif opt == '-m':
            min_count = int(arg)
        elif opt == '-a':
            min_authors = int(arg)
        elif opt == "--author":
            search_author = arg
        elif opt == "--title":
            search_title = arg
        elif opt == "--estcid":
            search_estcid = arg
    return(test, search_author, search_title,
           savedir, need_others, min_count,
           min_authors, primus, search_estcid)


def get_elapsed_time_str(start_time):
    elapsed_time = int(time.time() - start_time)
    sensible_elapsed_time = str(
        datetime.timedelta(seconds=elapsed_time))
    return(sensible_elapsed_time)


start_time = time.time()
# sensible_start_time = str(datetime.timedelta(seconds=int(start_time)))

# print("Started at: " + sensible_start_time)

print(get_elapsed_time_str(start_time) +
      " - Loading metadata into memory ... ")

good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)

print(get_elapsed_time_str(start_time) +
      " - Processing command line params ...")

(test, search_author, search_title, savedir, need_others,
 min_count, min_authors, primus,
 search_estcid) = get_start_params(sys.argv[1:])

if (test):
    datadir = "data/testgz/"
    writedir = "output/test/" + savedir
    filenames = glob.glob(datadir + "clusters*")
else:
    datadir = "data/indexed_clusters/"
    subdirs = glob.glob(datadir + "min*" + "/")
    writedir = "output/" + savedir + "/" + savedir
    filenames = []
    for subdir in subdirs:
        filenames.extend(glob.glob(subdir + "clusters*"))

print(get_elapsed_time_str(start_time) + " - Iterating files ...")

# filenames = glob.glob(datadir + "clusters*")
filenames_length = len(filenames)

i = 0
allHits = 0

for filename in filenames:
    with gzip.open(filename, 'rt') as cluster_data_file:
        cluster_data = json.load(cluster_data_file)
        hit_clusters, totalHits = process_cluster(cluster_data, good_metadata,
                                                  search_author, search_title,
                                                  need_others=need_others,
                                                  min_authors=min_authors,
                                                  search_estcid=search_estcid,
                                                  min_count=min_count,
                                                  primus=primus)
        write_results_txt(hit_clusters, writedir)
        allHits = allHits + totalHits
        i = i + 1
        print(get_elapsed_time_str(start_time) +
              " - Processed file (" + str(i) + "/" + str(filenames_length) +
              "): " + filename + " --- total hits: " +
              str(allHits))

# usage:
# python text-reuse-cur.py --author "Hume, David" --title "political discourses" -d min100_hume_notfirst -a 2 -p notfirst
# python text-reuse-cur.py --author "Wallace, Robert" -d min100_wallace_notfirst -a 2 -p notfirst
# python text-reuse-cur.py --estcid T144351 --author "Bayle, Pierre" -d min100_bayleT144351_first -a 2 -p first
# python text-reuse-cur.py --author "Ferguson, Adam" -d adam_ferguson_first -a 1 -p first -o

# primus (-p) options: first, notfirst, any (default)
# min authors (-a) options: 1, 2, 3, ...
