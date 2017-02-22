import json


def load_good_metadata(jsonfile):
    with open(jsonfile) as json_datafile:
        good_metadata = json.load(json_datafile)
        return(good_metadata)


def write_results_txt(hit_clusters, prefix, good_metadata):
    for key, value in hit_clusters.items():
        filename = prefix + "_" + key + ".txt"
        with open(filename, 'w') as txtfile:
            txtfile.write("clust: " + key + "\n")
            txtfile.write("count: " + str(value.get('Count')) + "\n")
            txtfile.write("avgle: " + str(value.get('Avglength')) + "\n\n")
            hits = value.get('Hits')

            for hit in hits:
                eccoid = hit.get('book_id')
                estc_metadata = good_metadata.get(eccoid)
                year = estc_metadata.get('estc_publication_year')
                author = estc_metadata.get('estc_author')
                if not author:
                    author = "NO AUTHOR IN ESTC DATA"
                title = estc_metadata.get('estc_title')
                estcid = estc_metadata.get('estc_id')
                txtfile.write(str(year) + " -- " + author + " -- " + title +
                              " -- eccoid: " + str(eccoid) + " -- estcid: " +
                              estcid + "\n")

            txtfile.write("\n-----------\n-----------\n\n")

            for hit in hits:
                eccoid = hit.get('book_id')
                estc_metadata = good_metadata.get(eccoid)
                year = estc_metadata.get('estc_publication_year')
                author = estc_metadata.get('estc_author')
                if not author:
                    author = "NO AUTHOR IN ESTC DATA"
                title = estc_metadata.get('estc_title')
                estcid = estc_metadata.get('estc_id')
                text = hit.get('text')
                txtfile.write(str(year) + " -- " + author + " -- " + title +
                              " -- eccoid: " + str(eccoid) + " -- estcid: " +
                              estcid + "\n\n")
                txtfile.write(text)
                txtfile.write("\n\n-----\n")


def process_cluster(cluster_data, good_metadata,
                    look_for_text, look_for_field):

    hit_clusters = dict()
    totalHits = 0

    for key, value in cluster_data.items():
        hits = value.get('Hits')
        # count = value.get('Count')
        # avglength = value.get('Avglength')
        # print(count)
        hitsFound = False
        othersFound = False

        for hit in hits:
            eccoid = hit.get('book_id')
            # print(eccoid)
            estc_metadata = good_metadata.get(eccoid)
            searchField = estc_metadata.get(look_for_field)
            if look_for_text in searchField and searchField is not None:
                hitsFound = True
            if (look_for_text not in searchField) and searchField is not None:
                othersFound = True

        if hitsFound and othersFound:
            print("hit!")
            print(key)
            hit_clusters[key] = value
            totalHits = totalHits + 1

    return hit_clusters, totalHits
