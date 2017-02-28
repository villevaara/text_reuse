import json
from operator import itemgetter


def load_good_metadata(jsonfile):
    with open(jsonfile) as json_datafile:
        good_metadata = json.load(json_datafile)
        return(good_metadata)


def write_results_txt(hit_clusters, prefix):
    for key, value in hit_clusters.items():
        filename = prefix + "_" + key + ".txt"
        with open(filename, 'w') as txtfile:
            txtfile.write("clust: " + key + "\n")
            txtfile.write("count: " + str(value.get('Count')) + "\n")
            txtfile.write("avgle: " + str(value.get('Avglength')) + "\n\n")
            hits = value.get('Hits')

            for hit in hits:
                txtfile.write(str(hit.get('year')) + " -- " +
                              hit.get('author') + " -- " +
                              hit.get('title') +
                              " -- eccoid: " +
                              str(hit.get('eccoid')) +
                              " -- estcid: " +
                              hit.get('estcid') + "\n")

            txtfile.write("\n-----------\n-----------\n\n")

            for hit in hits:
                eccoid = hit.get('eccoid')
                year = hit.get('year')
                author = hit.get('author')
                title = hit.get('title')
                estcid = hit.get('estcid')
                text = hit.get('text')
                txtfile.write(str(year) + " -- " + author + " -- " + title +
                              " -- eccoid: " + str(eccoid) + " -- estcid: " +
                              estcid + "\n\n")
                txtfile.write(text)
                txtfile.write("\n\n-----\n")


def enrich_cluster(cluster_value, good_metadata):
    hits = cluster_value.get('Hits')
    hits_sorted = []

    for hit in hits:
        eccoid = hit.get('book_id')
        estc_metadata = good_metadata.get(eccoid)
        year = estc_metadata.get('estc_publication_year')
        if year == 'NA' or year == 'ESTC DATA MISSING':
            year = 9999
        else:
            year = int(year)
        author = estc_metadata.get('estc_author')
        if not author:
            author = "NO AUTHOR IN ESTC DATA"
        hit_dict = {'eccoid': eccoid,
                    'year': year,
                    'author': author,
                    'title': estc_metadata.get('estc_title'),
                    'estcid': estc_metadata.get('estc_id'),
                    'text': hit.get('text')}
        hits_sorted.append(hit_dict)

    hits_sorted = sorted(hits_sorted, key=itemgetter('year'))
    ret_dict = {'Hits': hits_sorted,
                'Avglength': cluster_value.get('Avglength'),
                'Count': cluster_value.get('Count')}
    return ret_dict


def process_cluster(cluster_data, good_metadata,
                    search_author, search_title,
                    need_others=True,
                    min_authors=1,
                    min_count=2,
                    primus='any'):

    hit_clusters = dict()
    totalHits = 0

    for key, value in cluster_data.items():
        enriched_value = enrich_cluster(value, good_metadata)
        hits = enriched_value.get('Hits')
        count = int(enriched_value.get('Count'))
        primus_status = False

        if count >= min_count:
            hitsFound = False
            if need_others:
                othersFound = False
            else:
                othersFound = True
            authorlist = []

            for hit in hits:
                author_found = False
                title_found = False
                multi_author = False
                if search_author == "NONE":
                    author_found = True
                elif search_author.lower() in hit.get('author').lower():
                    author_found = True

                if search_title == "NONE":
                    title_found = True
                elif search_title.lower() in hit.get('title').lower():
                    title_found = True

                if (author_found and title_found):
                    hitsFound = True
                else:
                    othersFound = True

                author = hit.get('author')
                authorlist.append(author)
                authorset = set(authorlist)
                if len(authorset) >= min_authors:
                    multi_author = True

            if (primus == 'first' and
                    search_author.lower() in authorlist[0].lower()):
                primus_status = True
            elif (primus == 'notfirst' and
                    search_author.lower() not in authorlist[0].lower()):
                primus_status = True
            elif (primus == 'any'):
                primus_status = True

            if (hitsFound and othersFound and
                    multi_author and primus_status):
                print("hit!")
                print(key)
                hit_clusters[key] = enriched_value
                totalHits = totalHits + 1

    return hit_clusters, totalHits
