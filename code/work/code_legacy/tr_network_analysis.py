import csv
from text_reuse_common import (
    # load_good_metadata,
    get_author_from_estc,
    get_year_from_estc,
    # get_estcid_from_estc,
    )


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
