from requests import get
import csv
from lib.text_reuse_common import (
    get_author_from_estc,
    get_year_from_estc,
    get_estcid_from_estc)
from lib.octavo_api_client import OctavoEccoClusterClient


def get_clusters(data_docs):
    clusters = {}
    for doc in data_docs:
        cluster_id = str(doc.get('fragmentID'))
        document_id = str(doc.get('documentID'))
        if cluster_id in clusters.keys():
            clusters[cluster_id].append(document_id)
        else:
            clusters[cluster_id] = [document_id]
    return clusters


def get_document_length_from_api(document_id):
    api_request = ("https://vm0824.kaj.pouta.csc.fi/octavo/ecco/search" +
                   "?query=<DOCUMENT§documentID:" +
                   str(document_id) +
                   "§DOCUMENT>&pretty&limit=-1&field=documentLength")
    response = get(api_request)
    print("Querying API with: " + api_request)
    document_length = (
        response.json().get('results').get('docs')[0].get('documentLength'))
    return document_length


def enrich_cluster_data(cluster_data, good_metadata):
    returndata = []

    for item in cluster_data:
        item_document_id = str(item.get('documentID'))
        author = get_author_from_estc(item_document_id,
                                      good_metadata)
        year = get_year_from_estc(item_document_id, good_metadata)
        estcid = get_estcid_from_estc(item_document_id, good_metadata)
        new_item = {'document_id': str(item_document_id),
                    'cluster_id': str(item.get('fragmentID')),
                    'title': item.get('title'),
                    'author': author,
                    'year': year,
                    'startIndex': item.get('startIndex'),
                    'endIndex': item.get('endIndex'),
                    'text': item.get('text'),
                    'estc_id': estcid}
        returndata.append(new_item)

    print("return data length:" + str(len(returndata)))
    return returndata


# filtteröi pois entryt jotka klustereissa joissa book_id ei eka
def get_cluster_ids_where_book_id_first(enriched_cluster_data, book_id):
    cluster_first_years = {}
    book_id_cluster_first_years = {}

    for item in enriched_cluster_data:
        cluster_id = item.get('cluster_id')
        item_year = item.get('year')
        document_id = item.get('document_id')

        if cluster_id in cluster_first_years.keys():
            if cluster_first_years.get(cluster_id) > item_year:
                cluster_first_years[cluster_id] = item_year
        else:
            cluster_first_years[cluster_id] = item_year

        if book_id == document_id:
            book_id_cluster_first_years[cluster_id] = item_year

    first_clusters = []
    for key, value in book_id_cluster_first_years.items():
        if value == cluster_first_years[key]:
            first_clusters.append(key)

    print("book first in # clusters: " + str(len(first_clusters)))
    # returndata = []
    # for item in enriched_cluster_data:
    #     if item.get('cluster_id') in first_clusters:
    #         returndata.append(item)

    return first_clusters


def get_start_and_end_indices_for_cluster_and_document(enriched_cluster_data,
                                                       book_id):
    cluster_indices = {}
    book_id = str(book_id)

    for item in enriched_cluster_data:
        if (item.get('document_id') == book_id):
            # print("hit")
            start_i = item.get('startIndex')
            end_i = item.get('endIndex')
            cluster_indices[item.get('cluster_id')] = {
                'start': start_i,
                'end': end_i
            }

    return cluster_indices


def get_cluster_data_for_document_id_from_api_filters(document_id,
                                                      good_metadata,
                                                      not_author=True,
                                                      originals_only=True,
                                                      years_min=-1000,
                                                      years_max=1000,
                                                      testing_amount=-1):

    # data = get_wide_cluster_data_for_document_id_from_api(document_id,
    #                                                       testing_amount)

    api_client = OctavoEccoClusterClient(limit=testing_amount)
    data = api_client.get_wide_cluster_data_for_document_id(document_id)

    print("Orig data length:" + str(len(data)))

    document_id = str(document_id)
    orig_author = get_author_from_estc(document_id, good_metadata)
    orig_year = get_year_from_estc(document_id, good_metadata)

    enriched_cluster_data = enrich_cluster_data(data, good_metadata)

    interesting_clusters = (
        get_cluster_ids_where_book_id_first(enriched_cluster_data,
                                            document_id))

    returndata = []

    for item in enriched_cluster_data:
        author = item.get('author')
        year = item.get('year')

        if not_author:
            if (orig_author == author and
                    item.get('document_id') != document_id):
                continue

        if originals_only:
            if (item.get('cluster_id') not in interesting_clusters):
                continue

        if years_max != 1000:
            if not (year <= (orig_year + years_max)):
                continue

        if years_min != -1000:
            if not (year >= (orig_year + years_min)):
                continue

        returndata.append(item)

    print("Filtered data length:" + str(len(returndata)))

    return returndata


def write_coverage_as_csv(coverage_data):
    output_csvfile = "coverage.csv"
    with open(output_csvfile, 'w') as coverage_file:
        csvwriter = csv.writer(coverage_file)
        csvwriter.writerow(['Coverage'])
        for row in coverage_data:
            csvwriter.writerow([row])
