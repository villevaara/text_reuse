import csv

from lib.utils_common import (
    get_current_date_string,
    create_dir_if_not_exists
    )


def get_outpath_prefix_with_date(outpath_prefix):
    outpath_prefix = get_current_date_string() + "-" + outpath_prefix
    return outpath_prefix


def write_cluster_list_results_csv(cluster_list, outpath_prefix,
                                   include_date=False):

    print("> Writing cluster list as csv ...")
    group_ids = set()
    for cluster in cluster_list:
        group_ids.add(cluster.group_id)

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/by_header/"
    create_dir_if_not_exists(outdir)

    for group_id in group_ids:
        outfile = outdir + str(group_id) + ".csv"
        with open(outfile, 'w') as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow(['cluster_id',
                                'ecco_id',
                                'estc_id',
                                'author',
                                'title',
                                'preceding_header',
                                'year',
                                'location',
                                'text_before', 'text', 'text_after',
                                'preceding_header_index',
                                'start_index', 'end_index',
                                'find_start_index', 'find_end_index',
                                'document_length', 'fragment_indices',
                                'document_collection',
                                'group_name', 'group_id',
                                'group_start_index', 'group_end_index'])
        for cluster in cluster_list:
            if cluster.group_id == group_id:
                cluster.write_cluster_csv(outfile, include_header_row=False,
                                          method='a')
    print("  >> Done!")


def write_cluster_coverage_as_csv(coverage_data,
                                  outpath_prefix,
                                  include_date=False):

    print("> Writing cluster coverage as csv ...")

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"

    create_dir_if_not_exists(outdir)
    output_csvfile = outdir + "cluster_coverage.csv"
    with open(output_csvfile, 'w') as coverage_file:
        csvwriter = csv.writer(coverage_file)
        csvwriter.writerow(['Coverage'])
        for row in coverage_data:
            csvwriter.writerow([row])


def write_header_summarydata_csv(header_summarydata,
                                 outpath_prefix,
                                 outfile_suffix="",
                                 include_date=False):

    print("> Writing header summary data as csv ...")

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"

    create_dir_if_not_exists(outdir)
    output_csvfile = (outdir + "header_summary" +
                      outfile_suffix + ".csv")

    with open(output_csvfile, 'w') as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow(['header_index',
                                'header_text',
                                'total_fragments',
                                'unique_authors',
                                'authors',
                                'unique_titles',
                                'titles'])
            for row in header_summarydata:
                csvwriter.writerow([row.get('header_index'),
                                    row.get('header_text'),
                                    row.get('total_fragments'),
                                    row.get('unique_authors'),
                                    row.get('authors'),
                                    row.get('unique_titles'),
                                    row.get('titles')])


def write_document_text_with_coverage_highlight(document_text,
                                                outpath_prefix,
                                                include_date=False):

    print("> Writing document text with coverage highlights ...")

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"

    create_dir_if_not_exists(outdir)
    output_txtfile = (outdir + "coverage_highlight" +
                      ".txt")

    with open(output_txtfile, 'w') as output_file:
        output_file.write(document_text)
