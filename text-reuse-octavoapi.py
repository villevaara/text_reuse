from text_reuse_octavoapi_common import (
    # get_nodes,
    # write_nodes_csv,
    # get_clusters,
    # get_edges,
    # write_edges_csv,
    # write_edges_with_clusterids_csv,
    get_document_length_from_api,
    # get_cluster_data_for_document_id_from_api,
    # get_wide_cluster_data_for_document_id_from_api,
    # enrich_cluster_data,
    # get_cluster_ids_where_book_id_first,
    get_cluster_data_for_document_id_from_api_filters,
    get_cluster_coverage_for_document,
    get_text_for_document_id_from_api,
    get_headers_from_document_text,
    get_header_for_textindex,
    get_start_and_end_indices_for_cluster_and_document,
    # write_coverage_as_csv,
    )
from text_reuse_common import (
    load_good_metadata
    )
# import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as po
import csv


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

# document_id = "0825300109" # Bayle 1736
document_id = 1611003000  # madeville fable 1714
# document_id = 1313600106  # hume history
# document_id = "0429000102"  # hume history, tudor vol2 (elizabeth)

print("Getting document length...")
document_length = get_document_length_from_api(document_id)
print("got: " + str(document_length))
print("Getting cluster data...")
# document_data = get_cluster_data_for_document_id_from_api(document_id)

enriched_cluster_data = (
    get_cluster_data_for_document_id_from_api_filters(document_id,
                                                      good_metadata,
                                                      # years_min=0,
                                                      # years_max=20,
                                                      ))

document_text = get_text_for_document_id_from_api(document_id)
headers = get_headers_from_document_text(document_text)


def get_cluster_coverage_plotdata(enriched_cluster_data, document_length,
                                  document_id, headers):

    cluster_coverage = [0] * document_length
    cluster_text = [""] * document_length

    text_indices = (
        get_start_and_end_indices_for_cluster_and_document(
            enriched_cluster_data, document_id))
    # print(text_indices)

    max_end_i = 0
    for value in text_indices.values():
        cluster_end_i = value.get('end')
        if (max_end_i < cluster_end_i):
            max_end_i = cluster_end_i
    if (max_end_i != 0):
        cluster_coverage = [0] * max_end_i
        cluster_text = [""] * max_end_i
        print("new length: " + str(max_end_i))

    for entry in enriched_cluster_data:
        cluster_id = entry.get('cluster_id')
        index_data = text_indices.get(cluster_id)
        # print(index_data)
        start_index = index_data.get('start')
        end_index = index_data.get('end')
        for i in range(start_index, end_index):
            cluster_coverage[i] = cluster_coverage[i] + 1
            cluster_text[i] = get_header_for_textindex(i, headers)

    return {'cluster_coverage': cluster_coverage,
            'cluster_text': cluster_text}


def get_clusters_by_header(headers, enriched_cluster_data, document_id):

    text_indices = (
        get_start_and_end_indices_for_cluster_and_document(
            enriched_cluster_data, document_id))

    headerhits = {}

    for entry in enriched_cluster_data:
        cluster_id = entry.get('cluster_id')
        index_data = text_indices.get(cluster_id)
        start_index = index_data.get('start')
        header = get_header_for_textindex(start_index, headers)

        if header in headerhits.keys():
            headerhits[header] = headerhits[header] + 1
        else:
            headerhits[header] = 1

    returnlist = []

    for headerset in headers:
        hits = headerhits.get(headerset[1])
        h_dict = {
            'header': headerset[1],
            'index': headerset[0],
            'hits': hits
        }
        returnlist.append(h_dict)

    return returnlist


def write_headerhit_summary_csv(headerhits, outfile):
    output_csvfile = outfile
    with open(output_csvfile, 'w') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['Header', 'Index', 'Hits'])
        for item in headerhits:
            csvwriter.writerow([
                item.get('header'),
                item.get('index'),
                item.get('hits')])


print("Calculating coverage...")
# document_coverage = get_cluster_coverage_for_document(document_data,
#                                                       document_length)

plotdata = get_cluster_coverage_plotdata(enriched_cluster_data,
                                         document_length,
                                         document_id, headers)

cluster_coverage = plotdata.get('cluster_coverage')
cluster_text = plotdata.get('cluster_text')

headerhits = get_clusters_by_header(headers,
                                    enriched_cluster_data,
                                    document_id)
write_headerhit_summary_csv(headerhits, "headerhits_summary.csv")
# print(type(cluster_text))
# print(len(cluster_text))
# print(cluster_text[15000:16000])
# print(cluster_coverage)
print("Drawing plot...")
plot_x = list(range(0, len(plotdata.get('cluster_coverage'))))
print("x length: " + str(len(plot_x)))
plot_y = ["Reuse"]
plot_z = [cluster_coverage]
plot_text = [cluster_text]
print("z length: " + str(len(plot_z)))

# write_coverage_as_csv(hume_coverage)

plot_data = [
    go.Heatmap(
        z=plot_z,
        x=plot_x,
        y=plot_y,
        # text=plot_text,
        colorscale='Viridis',
    )
]

layout = go.Layout(
    title='Mandeville: Fable (1714)',
    xaxis=dict(ticks='', nticks=20),
    yaxis=dict(ticks=''),
    height=250
)

# plot_data = [
#     go.Scatter(
#         # z=plot_z,
#         x=plot_x,
#         y=cluster_coverage,
#         text=plot_text,
#         # colorscale='Viridis',
#         # mode="lines"
#         hoverinfo='text',
#     )
# ]

# layout = go.Layout(
#     showlegend=False
# )


print("making fig")
fig = go.Figure(data=plot_data, layout=layout)
print("displaying fig")
po.offline.plot(fig)
