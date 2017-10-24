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


def draw_sources_comparison(inputcsv, outputfile, plot_title,
                            save_img=False):
    # inputcsv = "output/data_used_for_plots/all_compared_from_others.csv"
    # outputfile = "docs/sources_in_compared.html"
    # plot_title = 'Source Fragments per Octavo Page'
    csvdata = read_plotdata_csv(inputcsv)
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
        title=plot_title,
        xaxis=dict(title='Author'),
        yaxis=dict(title='Source fragments per page')
        )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=outputfile)
    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=1200,
                image_height=600)


def draw_headerhits_per_author(inputfile, outputfile, plot_title,
                               save_image=False):
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
            text=author,
            hoverinfo="y+text",
            )
        data.append(trace)
        i += 1

    layout = go.Layout(
        barmode='stack',
        title=plot_title,
        xaxis=dict(title='Header'),
        yaxis=dict(title='Source fragments'),
        hovermode='closest',
        )

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename=outputfile + ".html")
    if save_image:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=1200,
                image_height=800,
                )


def draw_source_fragments_per_author(inputcsv, outputfile, plot_title,
                                     save_image=False):
    plotdata = read_plotdata_csv(
        inputcsv)

    pol_groups = set()
    for item in plotdata:
        pol_groups.add(item.get('Affiliation'))

    data = []
    for pol_group in pol_groups:
        xdata = []
        ydata = []
        for item in plotdata:
            xdata.append(item.get('Author'))
            if item.get('Affiliation') == pol_group:
                ydata.append(item.get('Fragments'))
            else:
                ydata.append(None)
        pol_group_data = go.Bar(
            x=xdata,
            y=ydata,
            name=pol_group
        )
        data.append(pol_group_data)

    layout = go.Layout(
        title=plot_title,
        xaxis=dict(title='Author'),
        yaxis=dict(title='Source fragments'),
        barmode='stack',
        margin=go.Margin(
            b=200),
        hovermode='closests'
        )

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig,
            filename=outputfile + ".html",
            auto_open=False)
    if save_image:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=1200,
                image_height=800,
                )


def draw_political_affiliation_volume(inputcsv,
                                      outputfile,
                                      plot_title,
                                      save_img=False,
                                      img_width=1400,
                                      img_height=800):
    plotdata = read_plotdata_csv(inputcsv)
    pol_groups = ["Whig", "Tory", "Others"]

    data = []
    for pol_group in pol_groups:
        xdata = []
        ydata = []
        for item in plotdata:
            xdata.append(item.get('Header'))
            ydata.append(item.get(pol_group))
        pol_group_data = go.Bar(
            x=xdata,
            y=ydata,
            name=pol_group)
        data.append(pol_group_data)

    layout = go.Layout(
        title=plot_title,
        xaxis=dict(title='Header'),
        yaxis=dict(title='Fragments'),
        barmode='group',
        margin=go.Margin(
            b=270),
        hovermode='closests'
        )

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig,
            filename="docs/" + outputfile + ".html",
            auto_open=False)
    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=img_width,
                image_height=img_height,
                )


# draw_sources_comparison(
#     inputcsv="output/data_used_for_plots/all_compared_from_others.csv",
#     outputfile="docs/sources_in_compared.html",
#     plot_title="Source Fragments per Octavo Page",
#     save_img=True)

# draw_headerhits_per_author(
#     "output/data_used_for_plots/hume7_sources_fragments_per_author_top20.csv",
#     "docs/hume7_header_authors",
#     "Source Fragments per Author per Header in Hume's History (vol. 7)")

# draw_headerhits_per_author(
#     "output/data_used_for_plots/hume6_sources_fragments_per_author_top20.csv",
#     "docs/hume6_header_authors",
#     "Source Fragments per Author per Header in Hume's History (vol. 6)")

# draw_source_fragments_per_author(
#     "output/data_used_for_plots/hume_author_totals_pol_top20.csv",
#     "docs/hume_top21_authors",
#     "Source Fragments per Author (top 21) in Hume's History")

# draw_political_affiliation_volume(
#     inputcsv="output/data_used_for_plots/hume7_sources_political.csv",
#     outputfile="hume7_sources_political",
#     plot_title="Hume's History vol. 7, Source political affiliation by headers",
#     save_img=True)

# draw_political_affiliation_volume(
#     inputcsv="output/data_used_for_plots/carte4_sources_political.csv",
#     outputfile="carte4_sources_political",
#     plot_title="Carte's History vol. 4, Source political affiliation by headers",
#     save_img=True,
#     img_width=1000)

draw_political_affiliation_volume(
    inputcsv="output/data_used_for_plots/rapin11-12_pol_headers.csv",
    outputfile="rapin11-12_sources_political",
    plot_title=(
        "Rapin's History (vols. 11-12)," +
        " Source political affiliation by headers"),
    save_img=True,
    img_width=1200,
    img_height=600)
