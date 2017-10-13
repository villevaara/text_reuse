import sys
from copy import deepcopy
import csv

from lib.tr_cluster import TextReuseCluster

from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.text_reuse_common import (
    load_good_metadata
    )

from lib.utils_common import (
    create_dir_if_not_exists
    )

from lib.headerdata import (
    get_headers_for_document_id,
    get_header_summary_data,
    )

from lib.output_csv import (
    write_cluster_list_results_csv,
    write_cluster_coverage_as_csv,
    write_header_summarydata_csv,
    write_document_html_with_coverage_highlight,
    save_plotdata_csv,
    get_outpath_prefix_with_date,
    write_plotdata_politics_csv,
    )

from lib.fragmentlists import (FragmentList,
                               get_doctext_indexmap,
                               get_document_text_splitjoined)

from lib.cfg_reader import (get_config_file_params,
                            get_start_params,
                            )

from lib.plots import (
    get_plotdata_fragments_per_year,
    get_plotdata_fragments_per_author_per_year,
    plotdata_fragments_per_author_per_year_filters)

from lib.sum_csvs import create_csv_summaries
from lib.author_metadata import read_author_metadata_csv


def get_cluster_list(fragment_list, add_cluster_groups=True):
    print("> Getting cluster list ...")
    cluster_ids = fragment_list.get_unique_cluster_ids()
    cluster_list = []
    for cluster_id in cluster_ids:
        fragments = fragment_list.get_fragments_of_cluster_id(cluster_id)
        cluster = TextReuseCluster(document_id, cluster_id, fragments)
        if add_cluster_groups:
            cluster.add_cluster_groups()
        cluster_list.append(cluster)
    print("  >> Done!")
    return cluster_list


def get_cluster_list_with_filters(cluster_list,
                                  require_first_author=None,
                                  filter_out_author="",
                                  author_ignore_id="",
                                  filter_out_year_below=-1,
                                  filter_out_year_above=-1,
                                  only_keep_first_author=False,
                                  filter_out_estcids=None):
    print("> Filtering cluster list ...")
    cluster_list_results = []
    for cluster in cluster_list:
        results_cluster = deepcopy(cluster)
        if require_first_author is not None:
            if require_first_author == "orig":
                if not results_cluster.orig_author_first():
                    continue
            elif require_first_author == "not-orig":
                if results_cluster.orig_author_first():
                    continue
        if filter_out_estcids is not None:
            results_cluster.filter_out_estcids(filter_out_estcids)
        if filter_out_author != "":
            results_cluster.filter_out_author(filter_out_author,
                                              author_ignore_id)
        if filter_out_year_above != -1:
            results_cluster.filter_out_year_above(filter_out_year_above)
        if filter_out_year_below != -1:
            results_cluster.filter_out_year_below(filter_out_year_below)
        if only_keep_first_author:
            first_ed_year = results_cluster.get_lowest_first_ed_year_guess()
            results_cluster.filter_out_firts_ed_year_not(first_ed_year)
            results_cluster.filter_only_one_book_per_author()
        if len(results_cluster.fragment_list) > 0:
            cluster_list_results.append(results_cluster)
    print("  >> Done!")
    return cluster_list_results


def get_cluster_coverage_data(document_id_to_cover,
                              cluster_list,
                              ecco_api_client):
    document_text = ecco_api_client.get_text_for_document_id(
        document_id_to_cover).get('text')
    document_length = len(document_text)
    cluster_coverage = [0] * document_length
    # cluster_text = [""] * document_length
    for cluster in cluster_list:
        start = cluster.group_start_index
        end = cluster.group_end_index
        length = cluster.get_length()
        # print("s: " + str(start) + " e: " +
        #       str(end) + " l: " + str(length))
        for i in range(start, end + 1):
            cluster_coverage[i] = cluster_coverage[i] + length
    return cluster_coverage


def get_document_text_with_coverage_highlight(document_id,
                                              coverage_data,
                                              ecco_api_client):
    document_text = ecco_api_client.get_text_for_document_id(
        document_id).get('text')
    document_text_list = list(document_text)
    document_length = len(document_text_list)
    for char_index in range(0, document_length):
        if coverage_data[char_index] == 0:
            document_text_list[char_index] = (
                document_text_list[char_index].upper())
    document_text_results = ''.join(document_text_list)
    return document_text_results


def author_plotdata_add_decades(plotdata):
    for author_data in plotdata:
        author_years = author_data.get('years')
        yearly_fragments = author_data.get('fragments')
        decades = list(range(1700, 1799, 10))
        decade_fragments = []
        for decade in decades:
            fragment_total = 0
            for i in range(0, len(author_years)):
                if (author_years[i] >= decade) & (
                        author_years[i] < decade + 10):
                    fragment_total += yearly_fragments[i]
            decade_fragments.append(fragment_total)
        author_data['decades'] = decades
        author_data['decade_fragments'] = decade_fragments


def write_csv_total_fragments_per_author_per_year(plotdata,
                                                  outpath_prefix,
                                                  include_date=True):
    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"
    create_dir_if_not_exists(outdir)
    topx = len(plotdata)
    outputfile = (
        outdir + "fragments_per_author_per_decade_top" +
        str(topx) +
        ".csv")

    with open(outputfile, 'w') as output_csv:
        headerrow = ["decade"]
        authors = []
        for entry in plotdata:
            authors.append(entry.get('author'))
        headerrow.extend(authors)
        csvwriter = csv.writer(output_csv)
        csvwriter.writerow(headerrow)
        decades = plotdata[0].get('decades')
        for i in range(0, len(decades)):
            datarow = [plotdata[0].get('decades')[i]]
            for entry in plotdata:
                datarow.append(entry.get('decade_fragments')[i])
            csvwriter.writerow(datarow)


def write_csv_total_fragments_per_author(plotdata,
                                         author_metadata,
                                         outpath_prefix,
                                         include_date=True):
    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)
    outdir = "output/" + outpath_prefix + "/"
    create_dir_if_not_exists(outdir)
    outputfile = outdir + "fragments_per_author.csv"

    with open(outputfile, 'w') as output_csv:
        headerrow = ["author", "total_fragments", "political_views", "link"]
        csvwriter = csv.writer(output_csv)
        csvwriter.writerow(headerrow)
        for entry in plotdata:
            author = entry.get('author')
            total = entry.get('total')
            views = "no_record"
            link = "no_record"
            if author in author_metadata.keys():
                a_meta = author_metadata[author]
                views = a_meta.get("political_views")
                link = a_meta.get("odnb_link")
            csvwriter.writerow([author,
                                total,
                                views,
                                link])


def get_totals_for_headers(headerdata, cluster_list):
    outdata_indices = []
    outdata_headers = []
    outdata_hits = []
    for item in headerdata:
        outdata_indices.append(item.get('index'))
        outdata_headers.append(item.get('header_text'))
    for index in outdata_indices:
        total_fragments = 0
        for cluster in cluster_list:
            if cluster.group_id == index:
                total_fragments += cluster.get_length()
        outdata_hits.append(total_fragments)
    retdict = {'indices': outdata_indices,
               'headers': outdata_headers,
               'hits': outdata_hits}
    return retdict


def get_header_plotdata(cluster_list, start_year, headerdata):
    headerdata_limits = [2, 5, 10, 20, -1]
    plotdata = []
    for limit in headerdata_limits:
        if limit != -1:
            toplimit = start_year - 1 + limit
        else:
            toplimit = -1
        filtered_clusters = (get_cluster_list_with_filters(
            cluster_list,
            filter_out_year_below=start_year,
            filter_out_year_above=toplimit))
        limit_hits = get_totals_for_headers(headerdata, filtered_clusters)
        limit_hits['within'] = limit
        plotdata.append(limit_hits)
    return plotdata


def get_plotdata_politicalview_by_header(cluster_list, headerdata,
                                         author_metadata):
    plotdata = []

    for item in headerdata:
        plotdata_index = item.get('index')
        plotdata_header = item.get('header_text')
        whig = 0
        royalist = 0
        jacobite = 0
        parliamentarian = 0
        tory = 0
        unionist = 0
        no_record = 0

        for cluster in cluster_list:
            if cluster.group_id == plotdata_index:
                cluster_affiliations = cluster.get_political_affiliations(
                    author_metadata)
                whig += cluster_affiliations.get('whig')
                royalist += cluster_affiliations.get('royalist')
                jacobite += cluster_affiliations.get('jacobite')
                parliamentarian += cluster_affiliations.get('parliamentarian')
                tory += cluster_affiliations.get('tory')
                unionist += cluster_affiliations.get('unionist')
                no_record += cluster_affiliations.get('no_record')

        plotdata.append({
            'index': plotdata_index,
            'header': plotdata_header,
            'whig': whig,
            'royalist': royalist,
            'jacobite': jacobite,
            'parliamentarian': parliamentarian,
            'tory': tory,
            'unionist': unionist,
            'no_record': no_record,
            'whig_wide': (whig + parliamentarian),
            'tory_wide': (tory + royalist + jacobite),
            'others_wide': (no_record + unionist),
            })

    return plotdata


def write_header_plotdata_csv(header_plotdata,
                              outpath_prefix,
                              include_date=True):
    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"
    create_dir_if_not_exists(outdir)
    outputfile = outdir + "header_plotdata.csv"

    with open(outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        indices = header_plotdata[0].get('indices')
        header_texts = header_plotdata[0].get('headers')
        limiters = []
        for item in header_plotdata:
            limiters.append("within_" + str(item.get('within')))
        headerrow = ['header_index', 'header_text']
        headerrow.extend(limiters)
        csvwriter.writerow(headerrow)
        for i in range(0, len(indices)):
            header_index_hits = []
            for item in header_plotdata:
                header_index_hits.append(item.get('hits')[i])
            resultrow = [indices[i], header_texts[i]]
            resultrow.extend(header_index_hits)
            csvwriter.writerow(resultrow)


def cluster_list_remove_duplicates(cluster_list, filter_author_ref=False):
    start_fragments = 0
    for cluster in cluster_list:
        start_fragments += cluster.get_length()
    print(" > Removing dulicates. Total " + str(start_fragments) +
          " fragments to start with.")
    used_seed_uids = set()
    new_cluster_list = []
    for cluster in cluster_list:
        used_seed_uids = (
            cluster.filter_non_unique_seed_uids(used_seed_uids))
        if len(cluster.fragment_list) > 0:
            new_cluster_list.append(cluster)

    retlist = new_cluster_list

    if filter_author_ref:
        used_seed_author_uids = set()
        author_cluster_list = []
        for cluster in retlist:
            used_seed_uids = (
                cluster.filter_non_unique_author_ref_uids(
                    used_seed_author_uids))
            if len(cluster.fragment_list) > 0:
                author_cluster_list.append(cluster)
        retlist = author_cluster_list

    end_fragments = 0
    for cluster in retlist:
        end_fragments += cluster.get_length()
    print(" > Duplicates removed. Total " + str(end_fragments) +
          " fragments remaining.")
    return retlist


# start_params = {'config_file': "hume2.yml",
#                 'api_limit': -1,
#                 'output_path_prefix': 'humetesti'}

start_params = get_start_params(sys.argv[1:])
# document_id = start_params.get('document_id')
config_file = start_params.get('config_file')
api_limit = start_params.get('api_limit')
outpath_prefix_base = start_params.get('output_path_prefix')
outpath_with_date = (
    "output/" + get_outpath_prefix_with_date(outpath_prefix_base) + "/")

config_file_params = get_config_file_params(config_file)
document_ids = config_file_params.get('document_ids')
filter_out_author = config_file_params.get('filter_out_author')
author_ignore_id = config_file_params.get('author_ignore_id')
require_first_author = config_file_params.get('require_first_author')
filter_out_year_below = config_file_params.get('filter_out_year_below')
filter_out_year_above = config_file_params.get('filter_out_year_above')
only_keep_first_author = config_file_params.get('only_keep_first_author')
filter_out_estcids = config_file_params.get('filter_out_estcids')

# get metadata
print("> Loading good metadata...")
good_metadata_jsonfile = "data/metadata/good_metadata.json"
good_metadata = load_good_metadata(good_metadata_jsonfile)
author_metadata = read_author_metadata_csv(
    "../data-public/authors-metadata/misc/author_metadata.csv")

print("  >> Done!")
all_outpaths = []

for document_id_dict in document_ids:
    document_id = document_id_dict.get('id')

    if (document_id_dict.get('filter_out_year_above') != -1):
        filter_out_year_above = document_id_dict.get('filter_out_year_above')
    if (document_id_dict.get('filter_out_year_below') != -1):
        filter_out_year_below = document_id_dict.get('filter_out_year_below')

    outpath_prefix = outpath_prefix_base + "/" + document_id
    all_outpaths.append(get_outpath_prefix_with_date(outpath_prefix))
    # get doc from api
    ecco_api_client = OctavoEccoClient()
    cluster_api_client = OctavoEccoClusterClient(limit=api_limit,
                                                 timeout=600)
    document_data = ecco_api_client.get_text_for_document_id(document_id)
    document_text = document_data.get('text')
    headerdata = get_headers_for_document_id(document_id, document_text)
    cluster_ids = cluster_api_client.get_cluster_ids_list_for_document_id(
        document_id)
    cluster_data = cluster_api_client.get_cluster_data_for_cluster_id_list(
        cluster_ids)
    # cluster_data = cluster_api_client.get_wide_cluster_data_for_document_id(
    #     document_id)

    # remove after update!
    docid_indexmap_ascii = get_doctext_indexmap(
            orig_text=document_text, method_ascii=True)
    docid_indexmap_unicode = get_doctext_indexmap(
        orig_text=document_text, method_ascii=False)
    doctext_splitjoined_unicode = (
        get_document_text_splitjoined(
            document_data.get('text'),
            ascii_search=False))
    doctext_splitjoined_ascii = (
        get_document_text_splitjoined(
            document_data.get('text'),
            ascii_search=True))
    document_data['splitjoined_unicode'] = (doctext_splitjoined_unicode)
    document_data['splitjoined_ascii'] = (doctext_splitjoined_ascii)

    fragment_list = FragmentList(cluster_data, seed_docid=document_id)
    fragment_list.add_metadata(author_metadata)
    fragment_list.add_headerdata(headerdata, document_id)

    # remove after update!
    # hume 5/8 is supposedly ascii. remove this after octavo indices set.
    for fragment in fragment_list.fragment_list:
        if fragment.ecco_id == document_id:
            is_ascii = fragment.set_fragment_encoding(document_data)
            if is_ascii:
                fragment.set_octavo_indices(docid_indexmap_ascii, False)
            else:
                fragment.set_octavo_indices(docid_indexmap_unicode, False)

    cluster_list = get_cluster_list(fragment_list, add_cluster_groups=True)
    cluster_list = cluster_list_remove_duplicates(
        cluster_list,
        filter_author_ref=only_keep_first_author)

    cluster_list_filtered = get_cluster_list_with_filters(
        cluster_list=cluster_list,
        filter_out_author=filter_out_author,
        require_first_author=require_first_author,
        author_ignore_id=author_ignore_id,
        filter_out_year_below=filter_out_year_below,
        filter_out_year_above=filter_out_year_above,
        only_keep_first_author=only_keep_first_author,
        filter_out_estcids=filter_out_estcids)

    # --- total fragments per year
    plotdata_fragments_per_year = (
        get_plotdata_fragments_per_year(cluster_list_filtered))
    save_plotdata_csv(plotdata_fragments_per_year,
                      "year", "fragments", outpath_prefix,
                      include_date=True)

    # --- cluster data grouped by header
    write_cluster_list_results_csv(cluster_list_filtered,
                                   outpath_prefix,
                                   include_date=True)

    # --- authors
    print("> Plotdata fragments / author / year")
    plotdata_fragments_per_author_per_year = (
        get_plotdata_fragments_per_author_per_year(cluster_list_filtered))
    # author totals all
    write_csv_total_fragments_per_author(
        plotdata_fragments_per_author_per_year,
        author_metadata,
        outpath_prefix)
    # top N
    plotdata_fragments_per_author_per_year_filtered = (
        plotdata_fragments_per_author_per_year_filters(
            plotdata_fragments_per_author_per_year,
            filter_na=True, keep_top=10))
    author_plotdata_add_decades(
        plotdata_fragments_per_author_per_year_filtered)
    write_csv_total_fragments_per_author_per_year(
        plotdata_fragments_per_author_per_year_filtered,
        outpath_prefix)
    # author political affiliation summary
    plotdata_politics = get_plotdata_politicalview_by_header(
        cluster_list_filtered, headerdata, author_metadata)
    write_plotdata_politics_csv(plotdata_politics, outpath_prefix,
                                include_date=True)

    # --- coverage html
    coverage_data = get_cluster_coverage_data(
        document_id, cluster_list_filtered, ecco_api_client)
    doctext_with_coverage_highlight = (
        get_document_text_with_coverage_highlight(document_id, coverage_data,
                                                  ecco_api_client))
    write_cluster_coverage_as_csv(coverage_data,
                                  outpath_prefix,
                                  include_date=True)
    write_document_html_with_coverage_highlight(coverage_data,
                                                document_text,
                                                outpath_prefix,
                                                include_date=True)

    # --- summaries by header
    header_summarydata = get_header_summary_data(cluster_list_filtered,
                                                 document_id)
    header_plotdata = get_header_plotdata(cluster_list_filtered,
                                          filter_out_year_below,
                                          headerdata)
    write_header_summarydata_csv(header_summarydata,
                                 outpath_prefix,
                                 outfile_suffix="",
                                 include_date=True)
    write_header_plotdata_csv(header_plotdata,
                              outpath_prefix)

create_csv_summaries(outpath_with_date)

# TODO
# * clusterset -class
#   * name, list of tr_clusters (with lists of fragments)
#   * filters used (filter history)
#   * method with which cluster group name was created
#   * method for saving clusterset as csv

# RESULT DATA:
# total coverage of document by character
# by others
# by all editions of hume -> what parts have been revised?
