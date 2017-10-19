import plotly.offline as py
import plotly.graph_objs as go
import csv
from collections import OrderedDict


def read_plotdata_csv(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        data = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def draw_sources_comparison():
    csv_filename = "output/data_used_for_plots/all_compared_from_others.csv"
    csvdata = read_plotdata_csv(csv_filename)
    xdata = []
    ydata = []
    for item in csvdata:
        xdata.append(item.get('Author'))
        ydata.append(item.get('Fragments per octavo page'))

    data = [go.Bar(
                x=xdata,
                y=ydata
        )]

    layout = go.Layout(
        title='Source Fragments per Octavo Page',
        xaxis=dict(title='Author'),
        yaxis=dict(title='Source fragments per page')
        )

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename="docs/sources_in_compared.html")


def draw_headerhits_per_author(inputfile, outputfile):
    author_headerdata = read_plotdata_csv(inputfile)

    xdata = list(author_headerdata[0].keys())
    xdata.remove('Author')
    ydata = OrderedDict()
    # ydata_keys = author_headerdata.get('Author')
    # for key in ydata_keys:
    #     ydata[key] = []

    for item in author_headerdata:
        author = item.get('Author')
        hits = []
        for header_key in xdata:
            hits.append(item.get(header_key))
        ydata[author] = hits

    data = []
    i = 0
    for author in ydata.keys():
        trace = go.Bar(
            x=xdata,
            y=ydata.get(author),
            name=author,
            )
        data.append(trace)
        i += 1

    layout = go.Layout(
        barmode='stack',
        title='Source Fragments per Author per Header',
        xaxis=dict(title='Header'),
        yaxis=dict(title='Source fragments')
        )

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename=outputfile)


draw_sources_comparison()
draw_headerhits_per_author(
    "output/data_used_for_plots/hume7_sources_fragments_per_author_top20.csv",
    "docs/hume7_header_authors.html")
