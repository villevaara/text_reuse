from requests import get
import csv
from text_reuse_common import (
    load_good_metadata,
    get_author_from_estc,
    get_year_from_estc,
    get_estcid_from_estc)
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as po


def get_nodes(data_docs, good_metadata):
    nodes = {}
    for doc in data_docs:
        document_id = str(doc.get('documentID'))
        if document_id not in nodes.keys():
            title = doc.get('title')
            cluster_id = doc.get('clusterID')
            author = get_author_from_estc(document_id, good_metadata)
            year = get_year_from_estc(document_id, good_metadata)
            nodes[document_id] = {'document_id': document_id,
                                  'title': title,
                                  'cluster_id': cluster_id,
                                  'author': author,
                                  'year': year}
    return nodes


def write_nodes_csv(nodes, csv_prefix):
    output_csvfile = "nodes_" + csv_prefix + ".csv"
    with open(output_csvfile, 'w') as nodes_file:
        csvwriter = csv.writer(nodes_file)
        csvwriter.writerow(['Id', 'Cluster', 'Title', 'Author', 'Year'])
        for row in nodes.values():
            csvwriter.writerow([row.get('document_id'),
                                row.get('cluster_id'),
                                row.get('title'),
                                row.get('author'),
                                row.get('year')
                                ])


def get_clusters(data_docs):
    clusters = {}
    for doc in data_docs:
        cluster_id = str(doc.get('clusterID'))
        document_id = str(doc.get('documentID'))
        if cluster_id in clusters.keys():
            clusters[cluster_id].append(document_id)
        else:
            clusters[cluster_id] = [document_id]
    return clusters


def get_edges(clusters):
    edges = []
    for key, value in clusters.items():
        cluster_id = "cid_" + str(key)
        last_doc = len(value) - 1
        for i in range(0, last_doc):
            doc_id = value[i]
            other_ids = value[i + 1:len(value)]
            for other_id in other_ids:
                cluster_dict = {'source': doc_id,
                                'target': other_id,
                                'cluster': cluster_id}
                edges.append(cluster_dict)

    print("Edges: " + str(len(edges)))
    return edges


def write_edges_csv(edges):
    output_csvfile = "edges.csv"
    with open(output_csvfile, 'w') as nodes_file:
        csvwriter = csv.writer(nodes_file)
        csvwriter.writerow(['Source', 'Target', 'Weight', 'Type'])
        for edge in edges:
            csvwriter.writerow([edge.get('source'),
                                edge.get('target'),
                                edge.get('count'),
                                'Undirected'])


def write_edges_with_clusterids_csv(edges, csv_prefix):
    output_csvfile = "edges_" + csv_prefix + ".csv"
    with open(output_csvfile, 'w') as nodes_file:
        csvwriter = csv.writer(nodes_file)
        csvwriter.writerow(['Source', 'Target', 'Type', 'Cluster'])
        for edge in edges:
            csvwriter.writerow([edge.get('source'),
                                edge.get('target'),
                                'Undirected',
                                edge.get('cluster')])


def get_document_length_from_api(document_id):
    api_request = ("https://vm0542.kaj.pouta.csc.fi/ecco_octavo_api/search" +
                   "?query=<DOCUMENT§documentID:" +
                   str(document_id) +
                   "§DOCUMENT>&pretty&limit=-1&field=documentLength")
    response = get(api_request)
    document_length = (
        response.json().get('results').get('docs')[0].get('documentLength'))
    return document_length


def get_cluster_data_for_document_id_from_api(document_id):
    api_request = (
        "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search" +
        "?query=documentID:" +
        str(document_id) +
        "&field=documentID&field=title&field=clusterID&field=startIndex" +
        "&field=endIndex&field=avgLength&field=text" +
        "&limit=-1&timeout=-1")
    response = get(api_request)
    data = response.json().get('results').get('docs')
    return data


def get_wide_cluster_data_for_document_id_from_api(document_id):
    api_request = (
        "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search" +
        "?query=<CLUSTER§<CLUSTER§documentID:" +
        str(document_id) +
        "§clusterID>§CLUSTER>" +
        "&field=documentID&field=title&field=clusterID&field=startIndex" +
        "&field=endIndex&field=text" +
        "&limit=-1&timeout=-1")
    response = get(api_request)
    data = response.json().get('results').get('docs')
    return data


def enrich_cluster_data(cluster_data, good_metadata):
    returndata = []

    for item in cluster_data:
        item_document_id = str(item.get('documentID'))
        author = get_author_from_estc(item_document_id,
                                      good_metadata)
        year = get_year_from_estc(item_document_id, good_metadata)
        estcid = get_estcid_from_estc(item_document_id, good_metadata)
        new_item = {'document_id': str(item_document_id),
                    'cluster_id': str(item.get('clusterID')),
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


def get_cluster_data_for_document_id_from_api_filters(document_id,
                                                      good_metadata,
                                                      not_author=True,
                                                      later=True):

    # api_request = (
    #     "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search" +
    #     "?query=<CLUSTER§<CLUSTER§documentID:" +
    #     str(document_id) +
    #     "§clusterID>§CLUSTER>" +
    #     "&field=documentID&field=title&field=clusterID&field=startIndex" +
    #     "&field=endIndex&field=text" +
    #     "&limit=-1&timeout=-1")

    # response = get(api_request)
    # data = response.json().get('results').get('docs')
    data = get_wide_cluster_data_for_document_id_from_api(document_id)
    print("Orig data length:" + str(len(data)))

    document_id = str(document_id)
    orig_author = get_author_from_estc(document_id, good_metadata)
    # orig_year = get_year_from_estc(document_id, good_metadata)

    enriched_cluster_data = enrich_cluster_data(data, good_metadata)
    interesting_clusters = (
        get_cluster_ids_where_book_id_first(enriched_cluster_data,
                                            document_id))

    returndata = []

    for item in enriched_cluster_data:
        # item_document_id = str(item.get('documentID'))
        # author = get_author_from_estc(item_document_id,
        #                               good_metadata)
        # year = get_year_from_estc(item_document_id, good_metadata)
        # new_item = {'document_id': item_document_id,
        #             'cluster_id': item.get('clusterID'),
        #             'title': item.get('title'),
        #             'author': author,
        #             'year': year,
        #             'startIndex': item.get('startIndex'),
        #             'endIndex': item.get('endIndex')}
        author = item.get('author')
        if (orig_author == author):
            continue
        if (item.get('cluster_id') not in interesting_clusters):
            continue
        returndata.append(item)

    print("Filtered data length:" + str(len(returndata)))

    return returndata


def get_cluster_coverage_for_document(document_api_data, document_length):
    docs_data = document_api_data
    cluster_coverage = [0] * document_length

    max_end_i = 0
    for result in docs_data:
        cluster_end_i = result.get('endIndex')
        if (max_end_i < cluster_end_i):
            max_end_i = cluster_end_i
    if (max_end_i != 0):
        cluster_coverage = [0] * max_end_i
        print("new length: " + str(max_end_i))

    # fix indices when good data available!!
    for result in docs_data:  # this stuff might easily be off by one.
        cluster_start_i = int(result.get('startIndex'))
        cluster_end_i = int(result.get('endIndex'))
        # print(cluster_end_i)
        for i in range(cluster_start_i, cluster_end_i):
            cluster_coverage[i] = cluster_coverage[i] + 1
    return cluster_coverage


# in cache:
# https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search?query=%3CCLUSTER%C2%A7%3CCLUSTER%C2%A7documentID:0352600600%C2%A7clusterID%3E%C2%A7CLUSTER%3E&limit=-1&field=documentID&field=title&timeout=-1
# https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search?query=%3CCLUSTER%C2%A7%3CCLUSTER%C2%A7documentID:0352600600%C2%A7clusterID%3E%C2%A7CLUSTER%3E&limit=100&field=documentID&field=title&timeout=-1

# mandeville hypo T061379 1399900400
# mandeville fable 1714 1611003000
# hume history 1313600106
# 1772 -- Hume, David (1711-1776) -- The history of England, from the invasion of Julius Cæsar to the revolution in 1688. In eight volumes. By David Hume, Esq; A new edition, corrected. To which is added, a complete index -- eccoid: 1313600106 -- estcid: T167537
# request_address = "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search?query=%3CCLUSTER%C2%A7%3CCLUSTER%C2%A7documentID:1313600106%C2%A7clusterID%3E%C2%A7CLUSTER%3E&limit=1000&field=documentID&field=title&field=clusterID"
# cluster_request_address = "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search?query=%3CCLUSTER%C2%A7%3CCLUSTER%C2%A7documentID:0352600600%C2%A7clusterID%3E%C2%A7CLUSTER%3E&limit=-1&field=documentID&field=title&field=clusterID&timeout=-1"

# -------------------------------------------------------
# ESTC metadata
# -------------------------------------------------------

print("Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)

# -------------------------------------------------------
# network stuff
# -------------------------------------------------------

# cluster_request_start = "https://vm0542.kaj.pouta.csc.fi/eccocluster_octavo_api/search?query="
# cluster_request_query_start = "%3CCLUSTER%C2%A7%3CCLUSTER%C2%A7documentID:"
# cluster_request_query_id = "1611003000"
# cluster_request_query_end = "%C2%A7clusterID%3E%C2%A7CLUSTER%3E"
# cluster_request_params = "&limit=-1&timeout=-1"
# cluster_request_fields = "&field=documentID&field=title&field=clusterID"
# cluster_request_address = (cluster_request_start +
#                            cluster_request_query_start +
#                            cluster_request_query_id +
#                            cluster_request_query_end +
#                            cluster_request_params +
#                            cluster_request_fields)


# cluster_response = get(cluster_request_address)
# data = cluster_response.json()
# data_results = data.get('results')
# data_docs = data_results.get('docs')  # list

# nodes = get_nodes(data_docs, good_metadata)
# write_nodes_csv(nodes, cluster_request_query_id)

# clusters = get_clusters(data_docs)
# print("making edges")
# edges = get_edges(clusters)
# print("writing edges")
# write_edges_with_clusterids_csv(edges, cluster_request_query_id)

# -------------------------------------------------------
# cluster coverage of document:
# -------------------------------------------------------


def write_coverage_as_csv(coverage_data):
    output_csvfile = "coverage.csv"
    with open(output_csvfile, 'w') as coverage_file:
        csvwriter = csv.writer(coverage_file)
        csvwriter.writerow(['Coverage'])
        for row in coverage_data:
            csvwriter.writerow([row])


document_id = 1611003000  # madeville fable 1714
# document_id = 1313600106  # hume history

print("Getting document length...")
document_length = get_document_length_from_api(document_id)
print("got: " + str(document_length))
print("Getting cluster data...")
# document_data = get_cluster_data_for_document_id_from_api(document_id)
document_data = (
    get_cluster_data_for_document_id_from_api_filters(document_id,
                                                      good_metadata))
print("Calculating coverage...")
document_coverage = get_cluster_coverage_for_document(document_data,
                                                      document_length)

print("Drawing plot...")
plot_x = list(range(0, len(document_coverage)))
print("x length: " + str(len(plot_x)))
plot_y = ["Reuse"]
plot_z = [document_coverage]
print("z length: " + str(len(plot_z)))

# write_coverage_as_csv(hume_coverage)

plot_data = [
    go.Heatmap(
        z=plot_z,
        x=plot_x,
        y=plot_y,
        colorscale='Viridis',
    )
]

layout = go.Layout(
    title='Mandeville: Fable (1714)',
    xaxis=dict(ticks='', nticks=20),
    yaxis=dict(ticks=''),
    height=250
)

print("making fig")
fig = go.Figure(data=plot_data, layout=layout)
print("displaying fig")
po.offline.plot(fig)
