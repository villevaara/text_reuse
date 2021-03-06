import plotly
from plotly.graph_objs import Scatter, Layout

from lib.output_csv import get_outpath_prefix_with_date
from copy import deepcopy
from math import floor
# from collections import OrderedDict


def get_plotdata_fragments_per_year(cluster_list,
                                    start_year=-1,
                                    end_year=-1):
    # get all years in clusters
    all_years_list = []
    for cluster in cluster_list:
        all_years_list.extend(cluster.get_years())
    # filter not found years
    all_years_list = [x for x in all_years_list if x != 9999]
    # get first and last year of all clusters
    if len(all_years_list) < 1:
        return {'x': [-1], 'y': [-1]}
    if start_year == -1:
        start_year = min(all_years_list)
    if end_year == -1:
        end_year = max(all_years_list)
    # years can be set manual too to compare two datasets
    years_x = list(range(start_year, end_year + 1))
    frags_y = []
    for year in years_x:
        frags_y.append(all_years_list.count(year))
    return {'x': years_x, 'y': frags_y}


def get_plotdata_fragments_per_first_ed_year(cluster_list,
                                             start_year=-1,
                                             end_year=-1):
    # get all years in clusters
    all_years_list = []
    for cluster in cluster_list:
        all_years_list.extend(cluster.get_guessed_first_ed_years())
    # filter not found years
    all_years_list = [x for x in all_years_list if x is not None]
    # get first and last year of all clusters
    if start_year == -1:
        start_year = min(all_years_list)
    if end_year == -1:
        end_year = max(all_years_list)
    # years can be set manual too to compare two datasets
    years_x = list(range(start_year, end_year + 1))
    frags_y = []
    for year in years_x:
        frags_y.append(all_years_list.count(year))
    return {'x': years_x, 'y': frags_y}


def get_plotdata_first_ed_per_decade(cluster_list):
    fed_years = []
    for cluster in cluster_list:
        fed_years.extend(cluster.get_guessed_first_ed_years())
    # filter not found years
    fed_years = [x for x in fed_years if x is not None]
    fed_decades = []
    for fed_year in fed_years:
        year_decade = floor(int(fed_year)/10)*10
        fed_decades.append(year_decade)
    # min_year = min(fed_years['x'])
    min_decade = min(fed_decades)
    # max_year = max(fed_years['x'])
    max_decade = max(fed_decades)
    decades = list(range(min_decade, max_decade + 1, 10))
    hits_y = []
    for decade in decades:
        hits_y.append(fed_decades.count(decade))
    return {'x': decades, 'y': hits_y}


def get_plotdata_fragments_per_author_per_year(cluster_list,
                                               headerdata,
                                               start_year=-1,
                                               end_year=-1,
                                               test_amount=-1):
    results = list()
    #
    all_years_list = []
    for cluster in cluster_list:
        all_years_list.extend(cluster.get_years())
    # filter not found years
    all_years_list = [x for x in all_years_list if x != 9999]
    # get first and last year of all clusters
    if len(all_years_list) < 1:
        return [{'years': "NA",
                 'fragments': "NA",
                 'total': "NA",
                 'author': "NA",
                 'header_inds': "NA",
                 'header_texts': "NA",
                 'header_hits': "NA"}]
    if start_year == -1:
        start_year = min(all_years_list)
    if end_year == -1:
        end_year = max(all_years_list)
        #
    all_authors = set()
    for cluster in cluster_list:
        authors = cluster.get_authors()
        all_authors.update(authors)
        #
    number_of_authors = len(all_authors) + 1
    i = 0
    for author in all_authors:
        i += 1
        print(str(i) + "/" + str(number_of_authors) + " " + author)
        author_years = []
        author_headers = deepcopy(headerdata)
        for headerdatadict in author_headers:
            headerdatadict['hits'] = 0

        for cluster in cluster_list:
            fragments_with_author = cluster.get_fragments_with_author(author)

            for fragment in fragments_with_author:
                if fragment.year != 9999:
                    author_years.append(fragment.year)

                for headerdatadict in author_headers:
                    if (headerdatadict.get('index') ==
                            fragment.seed_header_id):
                        headerdatadict['hits'] += 1

        header_inds = []
        header_texts = []
        header_hits = []
        for headerdatadict in author_headers:
            header_inds.append(headerdatadict.get('index'))
            header_texts.append(headerdatadict.get('header_text'))
            header_hits.append(headerdatadict.get('hits'))

        author_hits_total = len(author_years)
        years_x = list(range(start_year, end_year + 1))
        author_frags_y = []
        for year in years_x:
            author_frags_y.append(author_years.count(year))
            #
        author_dict = {'years': years_x,
                       'fragments': author_frags_y,
                       'total': author_hits_total,
                       'author': author,
                       'header_inds': header_inds,
                       'header_texts': header_texts,
                       'header_hits': header_hits}
        results.append(author_dict)
        if test_amount != -1 and i == test_amount:
            break
    #
    results.sort(key=lambda x: x.get('total'), reverse=True)
    #
    return results


def plotdata_fragments_per_author_per_year_filters(plotdata,
                                                   filter_na=True,
                                                   keep_top=10):
    keep_top = min(keep_top, len(plotdata))
    if filter_na:
        na_index = None
        for i in range(0, keep_top):
            if plotdata[i].get('author') == "NA":
                na_index = i
                break
        if na_index is not None:
            na_dict = plotdata.pop(na_index)
            plotdata.append(na_dict)
    #
    # other
    years_x = plotdata[0].get('years')
    other_frags_y = [0] * len(years_x)
    #
    plotdata_size = len(plotdata)
    for i in range(keep_top, plotdata_size):
        frags_to_add = plotdata[i].get('fragments')
        for year_i in range(0, len(years_x)):
            other_frags_y[year_i] += frags_to_add[year_i]
    #
    other_total = sum(other_frags_y)
    other_dict = {'years': years_x, 'fragments': other_frags_y,
                  'total': other_total,
                  'author': "Others"}
    #
    retlist = plotdata[0:keep_top]
    retlist.append(other_dict)
    return retlist


def draw_plot_fragments_per_author_per_year(plotdata,
                                            outpath_prefix,
                                            include_date=True):
    pass


def draw_plot_fragments_per_year(plotdata, outpath_prefix,
                                 include_date=True):
    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)
    outdir = "output/" + outpath_prefix + "/"
    filename = outdir + 'plot_fragments_per_year.html'

    xdata = plotdata.get('x')
    ydata = plotdata.get('y')
    plotly.offline.plot({
        "data": [Scatter(x=xdata, y=ydata)],
        "layout": Layout(title="Fragments per year",
                         xaxis=dict(title='Year'),
                         yaxis=dict(title='Fragments'))},
        filename=filename,
        auto_open=False)
