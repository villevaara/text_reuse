import csv
# import markdown
# import codecs
import cgi

from lib.utils_common import (
    get_current_date_string,
    create_dir_if_not_exists
    )


def get_outpath_prefix_with_date(outpath_prefix):
    outpath_prefix = get_current_date_string() + "-" + outpath_prefix
    return outpath_prefix


def save_plotdata_csv(plotdata, xlabel, ylabel,
                      outpath_prefix,
                      include_date=False):
    xdata = plotdata.get('x')
    ydata = plotdata.get('y')
    data_size = len(xdata)

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)

    outdir = "output/" + outpath_prefix + "/"

    create_dir_if_not_exists(outdir)
    output_csvfile = (outdir + "plotdata_" + xlabel + "-" + ylabel + ".csv")
    with open(output_csvfile, 'w') as coverage_file:
        csvwriter = csv.writer(coverage_file)
        csvwriter.writerow([xlabel, ylabel])
        for i in range(0, data_size):
            csvwriter.writerow([xdata[i], ydata[i]])


def write_plotdata_politics_csv(plotdata_politics,
                                outpath_prefix,
                                include_date=True):
    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)
    outdir = "output/" + outpath_prefix + "/"
    create_dir_if_not_exists(outdir)

    fieldnames = ['index', 'header',
                  'whig', 'royalist', 'jacobite', 'parliamentarian',
                  'tory', 'unionist', 'no_record',
                  'whig_wide', 'tory_wide', 'others_wide']

    output_csvfile = (outdir + "plotdata_political_views.csv")
    with open(output_csvfile, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in plotdata_politics:
            csvwriter.writerow(row)

    output_csvsummary = (outdir + "plotdata_politics_sum.csv")
    with open(output_csvsummary, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fieldnames[2:])
        whig = 0
        royalist = 0
        jacobite = 0
        parliamentarian = 0
        tory = 0
        unionist = 0
        no_record = 0
        whig_wide = 0
        tory_wide = 0
        others_wide = 0
        for row in plotdata_politics:
            whig += row.get('whig')
            royalist += row.get('royalist')
            jacobite += row.get('jacobite')
            parliamentarian += row.get('parliamentarian')
            tory += row.get('tory')
            unionist += row.get('unionist')
            no_record += row.get('no_record')
            whig_wide += row.get('whig_wide')
            tory_wide += row.get('tory_wide')
            others_wide += row.get('others_wide')
        csvwriter.writerow([whig, royalist, jacobite, parliamentarian,
                           tory, unionist, no_record,
                           whig_wide, tory_wide, others_wide])


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
                                'political_view',
                                'title',
                                'preceding_header',
                                'year',
                                'location',
                                'text_before',
                                'text',
                                'text_after',
                                'preceding_header_index',
                                'start_index',
                                'end_index',
                                'find_start_index',
                                'find_end_index',
                                'octavo_start_index',
                                'octavo_end_index',
                                'document_length',
                                'document_collection',
                                'group_name',
                                'group_id',
                                'group_start_index',
                                'group_end_index'])
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


def get_html_start(add_header=False, add_stylesheet=False):
    start_string = "<html>\n"
    if add_stylesheet:
        start_string = (
            start_string + '<head>\n'
            '<link rel="stylesheet" ' +
            'href="/public/bootstrap/css/bootstrap.min.css">\n' +
            '</head>\n'
            )
    if add_header:
        start_string = (
            start_string + "\n<body>\n<p>" +
            "<b>NOTE: <mark>Highlighted text is from other source</mark>" +
            " and not highlighted is original by author.</b></p>\n")
    start_string = start_string + "<body>\n"
    return start_string


def get_html_end():
    return "</body>\n</html>"


def write_document_html_with_coverage_highlight(coverage_data,
                                                document_text,
                                                outpath_prefix,
                                                include_date=False):

    print("> Writing document html with coverage highlights ...")
    document_text_list = list(document_text)
    document_length = len(document_text_list)
    html_text_list = []

    html_text_list.append(get_html_start(add_header=True))
    html_text_list.append("<p>")

    char_index = 0
    prev_char_in_cluster = False
    mark_tag_open = False
    header_tag_open = False
    mark_tag_reopen = False

    while char_index < document_length:
        if coverage_data[char_index] == 0:
            this_char_in_cluster = False
        else:
            this_char_in_cluster = True

        if (this_char_in_cluster) and (not prev_char_in_cluster):
            html_text_list.append("<mark>")
            mark_tag_open = True
        elif (not this_char_in_cluster) and (prev_char_in_cluster):
            html_text_list.append("</mark>")
            mark_tag_open = False

        if (document_text_list[char_index] == "\n" and
                document_text_list[char_index + 1] == "\n" and
                document_text_list[char_index + 2] == "#"):
            header_tag_open = True
            if mark_tag_open:
                html_text_list.append("</mark></p>\n<p><h1>")
                mark_tag_reopen = True
            else:
                html_text_list.append("</p>\n<p><h1>")
            char_to_append = ""
            char_index_step = 3
        elif (document_text_list[char_index] == "\n" and
                document_text_list[char_index + 1] == "\n"):
            if mark_tag_open:
                html_text_list.append("</mark>")
                mark_tag_reopen = True
            if header_tag_open:
                html_text_list.append("</h1>")
                header_tag_open = False
            html_text_list.append("</p>")
            char_to_append = "\n<p>"
            char_index_step = 2
        elif document_text_list[char_index] == "\n":
            char_to_append = " "
            char_index_step = 1
        else:
            char_to_append = cgi.escape(document_text_list[char_index])
            char_index_step = 1

        html_text_list.append(char_to_append)

        if mark_tag_reopen:
            html_text_list.append("<mark>")
            mark_tag_reopen = False
        prev_char_in_cluster = this_char_in_cluster
        char_index += char_index_step

    if mark_tag_open:
        html_text_list.append("</mark>")
    html_text_list.append("</p>")
    html_text_list.append(get_html_end())
    html_text_results = ''.join(html_text_list)

    if include_date:
        outpath_prefix = get_outpath_prefix_with_date(outpath_prefix)
    outdir = "output/" + outpath_prefix + "/"
    create_dir_if_not_exists(outdir)

    output_htmlfile = (outdir + "coverage_highlight.html")
    with open(output_htmlfile, 'w') as output_file:
        output_file.write(html_text_results)
