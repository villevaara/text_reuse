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


def draw_reuse_totals_by_volume(inputcsv,
                                outputfile,
                                plot_title,
                                x_column="description",
                                x_title='Volume',
                                img_width=800,
                                img_height=600,
                                save_img=False):
    csvdata = read_plotdata_csv(inputcsv)
    xdata = []
    ydata = []
    for item in csvdata:
        xdata.append(item.get(x_column))
        ydata.append(item.get('fragments'))
    data = [go.Bar(
                x=xdata,
                y=ydata
        )]
    layout = go.Layout(
        title=plot_title,
        xaxis=dict(title=x_title),
        yaxis=dict(title='Fragments'),
        margin=dict(b=150,
                    r=120)
    )
    fig = go.Figure(data=data, layout=layout)
    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=img_width,
                image_height=img_height)
    else:
        py.plot(fig, filename=outputfile)


def draw_sources_comparison(inputcsv,
                            outputfile,
                            plot_title,
                            save_img=False,
                            image_width=1200,
                            image_height=600):
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
    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=image_width,
                image_height=image_height)
        # py.image.save_as(fig, filename='a-simple-plot.png')
    else:
        py.plot(fig, filename=outputfile)


def draw_headerhits_per_author(inputfile, outputfile, plot_title,
                               save_img=False):
    author_headerdata = read_plotdata_csv(inputfile)

    xdata = list(author_headerdata[0].keys())
    xdata.remove('Author')
    # xdata = []
    # for item in xdata_pre:
    #     xdata.append(item[:10] + "…")
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

    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=1200,
                image_height=800,
                )
    else:
        py.plot(fig, filename=outputfile + ".html")


def draw_source_fragments_per_author(inputcsv, outputfile, plot_title,
                                     pol_colours,
                                     save_img=False):
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
            name=pol_group,
            marker=dict(
                color=pol_colours.get(pol_group.lower()))
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

    if save_img:
        py.plot(fig,
                image='png',
                image_filename=outputfile,
                image_width=1200,
                image_height=800,
                )
    else:
        py.plot(fig,
                filename=outputfile + ".html",
                auto_open=False)


def draw_political_affiliation_by_subitem(inputcsv,
                                          outputfile,
                                          plot_title,
                                          x_title,
                                          pol_colours,
                                          y_range=None,
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
            xdata.append(item.get('Item'))
            ydata.append(item.get(pol_group))
        pol_group_data = go.Bar(
            x=xdata,
            y=ydata,
            name=pol_group,
            marker=dict(
                color=pol_colours.get(pol_group.lower()))
            )
        data.append(pol_group_data)

    if y_range is None:
        y_axis_params = dict(title='Fragments')
    else:
        y_axis_params = dict(title='Fragments',
                             range=y_range)

    layout = go.Layout(
        title=plot_title,
        xaxis=dict(title=x_title),
        yaxis=y_axis_params,
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
