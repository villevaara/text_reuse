from lib.octavo_api_client import (
    OctavoEccoClient,
    OctavoEccoClusterClient
    )

from lib.fragmentlists import (
    get_validated_fragmentlist)

from lib.headerdata_dump_common import read_docid_asciimap_csv
from lib.additional_cluster_data import read_datadir_add_clusterdata

from lib.tr_bookcontainer import (
    get_docid_fragments,
    BookContainer,
    get_local_ecco_fulltext_data
    )
import csv
# from collections import OrderedDict


def get_cluster_id_set(docid_fragments):
    cluster_id_set = set()
    for fragment in docid_fragments:
        cluster_id_set.add(fragment.cluster_id)
    return cluster_id_set


def get_volumes_fragment_dict(edition_ecco_ids,
                              field_eccocluster,
                              cluster_api_client,
                              ecco_api_client,
                              docids_asciimap,
                              local_eccodata_dir=None,
                              add_cludata=None):
    volumes_fragment_dict = {}
    for docid in edition_ecco_ids:
        docid_fragments = get_docid_fragments(docid,
                                              cluster_api_client,
                                              ecco_api_client,
                                              field_eccocluster,
                                              docids_asciimap,
                                              local_eccodata_dir,
                                              add_cludata)
        if local_eccodata_dir is not None:
            docid_fulltext = get_local_ecco_fulltext_data(
                docid, local_eccodata_dir)['text']
        else:
            docid_fulltext = ecco_api_client.get_text_for_document_id(
                docid)['text']
        docid_fragments_validated = get_validated_fragmentlist(
            docid_fragments,
            docid_fulltext,
            docid)
        volumes_fragment_dict[docid] = docid_fragments_validated
    return volumes_fragment_dict


def get_edition_cluster_ids(edition_fragments_dict):
    edition_cluster_ids = set()
    for key, value in edition_fragments_dict.items():
        # key = ecco_id, value = fragment list
        volume_cluster_ids = get_cluster_id_set(value)
        edition_cluster_ids.update(volume_cluster_ids)
    return edition_cluster_ids


def get_shared_fragments(fragment_dict_to_limit, fragment_dict_to_limit_with):
    return_cluster_ids = get_edition_cluster_ids(fragment_dict_to_limit)
    limiting_cluster_ids = get_edition_cluster_ids(
        fragment_dict_to_limit_with)
    shared_cluster_ids = return_cluster_ids.intersection(limiting_cluster_ids)
    ret_fragment_dict = {}
    for key, fragmentlist in fragment_dict_to_limit.items():
        filtered_fraglist = []
        for fragment in fragmentlist:
            if fragment.cluster_id in shared_cluster_ids:
                filtered_fraglist.append(fragment)
        ret_fragment_dict[key] = filtered_fraglist
    return ret_fragment_dict


def get_volume_shared_charmap(docid, volume_fraglist, ecco_api_client):
    docid_fulltext_data = ecco_api_client.get_text_for_document_id(docid)
    docid_fulltext_text = docid_fulltext_data.get('text')
    fulltext_charcount = len(docid_fulltext_text)
    char_inds = list(range(0, (len(docid_fulltext_text) - 1)))
    # initialize charmap as empty
    charmap = {}
    for char_ind in char_inds:
        charmap[char_ind] = False
    # create set of char inds included in fragment indices
    shared_char_inds = set()
    for fragment in volume_fraglist:
        if fragment.octavo_start_index == -1 | fragment.octavo_end_index == -1:
            print("woot, wtf! there shouldn't be this kind of octavo indices")
        fragment_char_inds = set(
            range(fragment.octavo_start_index, fragment.octavo_end_index))
        shared_char_inds.update(fragment_char_inds)
    # update charmap with inds in shared in above set
    for char_ind in shared_char_inds:
        charmap[char_ind] = True
    # count coverage
    shared_chars_count = 0
    for char_ind in charmap.keys():
        if charmap[char_ind]:
            shared_chars_count += 1
    # create a rough highlighted version of fulltext
    text_projection_list = []
    for char_ind in char_inds:
        if charmap[char_ind]:
            text_projection_list.append(docid_fulltext_text[char_ind])
        else:
            text_projection_list.append(docid_fulltext_text[char_ind].upper())
    text_projection = "".join(text_projection_list)
    return {
        'docid': docid,
        'doctext': docid_fulltext_text,
        'charmap': charmap,
        'fulltext_charcount': fulltext_charcount,
        'shared_charcount': shared_chars_count,
        'shared_ratio': (shared_chars_count / fulltext_charcount),
        'text_projection': text_projection
    }


def get_edition_char_dicts(edition_shared_frag_dict, ecco_api_client):
    docids = list(edition_shared_frag_dict.keys())
    edition_char_dicts = {}
    for docid in docids:
        vol_shared_chars = get_volume_shared_charmap(
            docid,
            edition_shared_frag_dict[docid],
            ecco_api_client)
        edition_char_dicts[docid] = vol_shared_chars
    return edition_char_dicts


def get_booklist(doc_id_list,
                 ecco_api_client,
                 xml_img_page_datadir,
                 fragment_dict,
                 outdir,
                 outfile_prefix,
                 write_pdf=False,
                 write_hl_stats=False):
    books = []
    i = 0
    for doc_id in doc_id_list:
        i += 1
        doc_book = BookContainer(doc_id, ecco_api_client,
                                 xml_img_page_datadir,
                                 fetch_images=True,
                                 use_local_eccodata=True)
        doc_frags = fragment_dict[doc_id]
        doc_book.set_fragment_list(fragment_list=doc_frags)
        doc_book.set_token_highlights(invert=True)
        doc_book.set_highlight_statistics()
        if write_pdf:
            doc_book.write_highlight_pdf(pdf_fname=(
                outdir + outfile_prefix +
                str(i) + "_id_" + doc_id + ".pdf"))
        if write_hl_stats:
            doc_hl = doc_book.document_highlight_stats
            page_hl = doc_book.pages_highlight_stats
            section_hl = doc_book.section_highlight_stats
            page_stats_csv_file = (
                outdir + outfile_prefix +
                str(i) + "_id_" + doc_id + "_page_stats.csv")
            header_stats_csv_file = (
                outdir + outfile_prefix +
                str(i) + "_id_" + doc_id + "_header_stats.csv")
            doc_stats_csv_file = (
                outdir + outfile_prefix +
                str(i) + "_id_" + doc_id + "_doc_stats.csv")
            # page csv
            with open(page_stats_csv_file, 'w') as csv_outfile:
                csvwriter = csv.writer(csv_outfile)
                csvwriter.writerow(['octavo_id',
                                    'header',
                                    'page_number',
                                    'tokens_total',
                                    'tokens_highlighted',
                                    'tokens_ratio',
                                    'chars_total',
                                    'chars_highlighted',
                                    'chars_ratio'
                                    ])
                for page_number in page_hl.keys():
                    csvwriter.writerow([
                        doc_book.octavo_id,
                        page_hl[page_number]['header'],
                        page_hl[page_number]['page_number'],
                        page_hl[page_number]['tokens_total'],
                        page_hl[page_number]['tokens_highlighted'],
                        page_hl[page_number]['tokens_ratio'],
                        page_hl[page_number]['chars_total'],
                        page_hl[page_number]['chars_highlighted'],
                        page_hl[page_number]['chars_ratio']
                        ])
            # header csv
            with open(header_stats_csv_file, 'w') as csv_outfile:
                csvwriter = csv.writer(csv_outfile)
                csvwriter.writerow(['octavo_id',
                                    'header',
                                    'header_page',
                                    'tokens_total',
                                    'tokens_highlighted',
                                    'tokens_ratio',
                                    'chars_total',
                                    'chars_highlighted',
                                    'chars_ratio'
                                    ])
                for header in section_hl.keys():
                    csvwriter.writerow([
                        doc_book.octavo_id,
                        section_hl[header]['header'],
                        section_hl[header]['page_number'],
                        section_hl[header]['tokens_total'],
                        section_hl[header]['tokens_highlighted'],
                        section_hl[header]['tokens_ratio'],
                        section_hl[header]['chars_total'],
                        section_hl[header]['chars_highlighted'],
                        section_hl[header]['chars_ratio']
                        ])
            # doc csv
            with open(doc_stats_csv_file, 'w') as csv_outfile:
                csvwriter = csv.writer(csv_outfile)
                csvwriter.writerow(['octavo_id',
                                    'tokens_total',
                                    'tokens_highlighted',
                                    'tokens_ratio',
                                    'chars_total',
                                    'chars_highlighted',
                                    'chars_ratio'
                                    ])
                csvwriter.writerow([
                    doc_book.octavo_id,
                    doc_hl['tokens_total'],
                    doc_hl['tokens_highlighted'],
                    doc_hl['tokens_ratio'],
                    doc_hl['chars_total'],
                    doc_hl['chars_highlighted'],
                    doc_hl['chars_ratio']
                    ])
            # end csvs
        books.append(doc_book)
    return books


# ---------------------------
# main script
# ---------------------------


ecco_api_client = OctavoEccoClient()
ecco_api_client = "local"
# cluster_api_client = OctavoEccoClusterClient(timeout=600)
cluster_api_client = None

docids_asciimap = read_docid_asciimap_csv('data/eccoids/asciilines.csv')
xml_img_page_datadir = (
    "/home/vvaara/projects/comhis/data-own-common/ecco-xml-img/")
fields_ecco = ["documentID", "content"]
field_eccocluster = ["documentID", "fragmentID", "text",
                     "startIndex", "endIndex"]
add_cludatadir = "data/tr_data_additional/clusters_newest/"
add_cludata = read_datadir_add_clusterdata(add_cludatadir)

# Robertson, History of the reign of the Emperor Charles V
# T71143 - Strahan 1769, 3 vols
# T78989 - 1792, 4 vols

# docids_first = ["0261000101",
#                 "0261000102",
#                 "0261000103"]

# docids_later = ["0694400101",
#                 "0694400102",
#                 "0694400103",
#                 "0694400104"]


# Hume, History of England
docids_first = [
    "0162900301",
    "0162900302",
    "0429000101",
    "0429000102",
    "0156400400",
    "0162200200"
    ]

docids_later = [
    "0145000201",
    "0145000202",
    "0145100103",
    "0145100104",
    "0145100105",
    "0145100106",
    "0145100107",
    "0145200108"
    ]


first_ed_volumes_frag_dict = get_volumes_fragment_dict(
    docids_first,
    field_eccocluster,
    cluster_api_client,
    ecco_api_client,
    docids_asciimap,
    xml_img_page_datadir,
    add_cludata)
# first_ed_cluster_ids = get_edition_cluster_ids(first_ed_volumes_frag_dict)

later_ed_volumes_frag_dict = get_volumes_fragment_dict(
    docids_later,
    field_eccocluster,
    cluster_api_client,
    ecco_api_client,
    docids_asciimap,
    xml_img_page_datadir,
    add_cludata)
# later_ed_cluster_ids = get_edition_cluster_ids(later_ed_volumes_frag_dict)

first_ed_shared_frag_dict = get_shared_fragments(
    first_ed_volumes_frag_dict, later_ed_volumes_frag_dict)
later_ed_shared_frag_dict = get_shared_fragments(
    later_ed_volumes_frag_dict, first_ed_volumes_frag_dict)


# get booklists and write highlight pdfs
first_ed_books = get_booklist(
    docids_first,
    ecco_api_client,
    xml_img_page_datadir,
    first_ed_shared_frag_dict,
    "output/ed_comparison/clusters_newest/first/",
    "first_ed_vol",
    write_pdf=True,
    write_hl_stats=True)

later_ed_books = get_booklist(
    docids_later,
    ecco_api_client,
    xml_img_page_datadir,
    later_ed_shared_frag_dict,
    "output/ed_comparison/clusters_newest/later/",
    "later_ed_vol",
    write_pdf=True,
    write_hl_stats=True)

# # ----------------------
# # get char by char data
# # ----------------------

# first_ed_shared_char_dicts = get_edition_char_dicts(first_ed_shared_frag_dict,
#                                                     ecco_api_client)
# later_ed_shared_char_dicts = get_edition_char_dicts(later_ed_shared_frag_dict,
#                                                     ecco_api_client)


# # ----------------------
# # output txt
# # ----------------------

# for value in first_ed_shared_char_dicts.values():
#     print(str(value['docid']) + " : " + str(value['shared_ratio']))
#     outfname_hl = ('output/ed_comparison/first_ed/' + str(value['docid']) +
#                    '_highlight.txt')
#     outfname_ft = ('output/ed_comparison/first_ed/' + str(value['docid']) +
#                    '_fulltext.txt')
#     with open(outfname_hl, 'w') as outfile:
#         outfile.write(value['text_projection'])
#     with open(outfname_ft, 'w') as outfile:
#         outfile.write(value['doctext'])


# for value in later_ed_shared_char_dicts.values():
#     print(str(value['docid']) + " : " + str(value['shared_ratio']))
#     outfname_hl = ('output/ed_comparison/later_ed/' + str(value['docid']) +
#                    '_highlight.txt')
#     outfname_ft = ('output/ed_comparison/later_ed/' + str(value['docid']) +
#                    '_fulltext.txt')
#     with open(outfname_hl, 'w') as outfile:
#         outfile.write(value['text_projection'])
#     with open(outfname_ft, 'w') as outfile:
#         outfile.write(value['doctext'])
