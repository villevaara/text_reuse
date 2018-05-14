from lib.utils_common import read_csv_to_dictlist
import csv


def get_total_reuses_all_volumes(csvfile):
    totals_list = read_csv_to_dictlist(csvfile)
    sum_fragments = 0
    sum_length = 0
    for item in totals_list:
        sum_fragments += int(item.get('fragments'))
        sum_length += int(item.get('length'))
    return {'fragments': sum_fragments, 'length': sum_length}


def write_plotdata_totals_compared(input_dict, output_csv):
    plotdata = []
    for key in input_dict.keys():
        fragdata = get_total_reuses_all_volumes(input_dict.get(key))
        per_oct_page = fragdata.get('fragments') / (fragdata.get('length') / 2000)
        # octavo page is approx. 2000 chars
        plotdata.append({'Author': key,
                         'Fragments': fragdata.get('fragments'),
                         'Total length': fragdata.get('length'),
                         'Fragments per octavo page': per_oct_page})
    with open(output_csv, 'w') as csvfile:
        fieldnames = ['Author', 'Fragments', 'Total length',
                      'Fragments per octavo page']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in plotdata:
            writer.writerow({
                'Author': item.get('Author'),
                'Fragments': item.get('Fragments'),
                'Total length': item.get('Total length'),
                'Fragments per octavo page': item.get(
                    'Fragments per octavo page')})

# f1
io_dict_plot1 = {
    "Hume, David": "output/plot_data/in/180511-hume_all_from_others/volume_totals.csv",
    "Carte, Thomas": "output/plot_data/in/180511-carte_all_from_others/volume_totals.csv",
    "Guthrie, William": "output/plot_data/in/180511-guthrie_all_from_others/volume_totals.csv",
    "Rapin, Paul de": "output/plot_data/in/180511-rapin_all_from_others/volume_totals.csv",
}
fig1_out_csv = "output/plot_data/f1_all_compared_from_others.csv"
write_plotdata_totals_compared(io_dict_plot1, fig1_out_csv)


# f 2-5
def write_reuse_totals_by_volume_csv(input_csv, output_csv):
    output_csv
    inputlist = read_csv_to_dictlist(input_csv)
    inputlist_sorted = sorted(inputlist, key=lambda k: int(k['sequence']))
    with open(output_csv, 'w') as csvfile:
        fieldnames = inputlist_sorted[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in inputlist_sorted:
            writer.writerow(item)


io_list_f2_5 = [
    {
        "input_csv": "output/plot_data/in/180513-hume_all_from_others_first_eds/volume_totals.csv",
        "output_csv": "output/plot_data/f2b_volumes_all_sources_hume_first_eds.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-hume_all_from_others/volume_totals.csv",
        "output_csv": "output/plot_data/f2_volumes_all_sources_hume.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-rapin_all_from_others/volume_totals.csv",
        "output_csv": "output/plot_data/f3_volumes_all_sources_rapin.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-guthrie_all_from_others/volume_totals.csv",
        "output_csv": "output/plot_data/f4_volumes_all_sources_guthrie.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-carte_all_from_others/volume_totals.csv",
        "output_csv": "output/plot_data/f5_volumes_all_sources_carte.csv"
    }
]

for item in io_list_f2_5:
    input_csv = item.get('input_csv')
    output_csv = item.get('output_csv')
    write_reuse_totals_by_volume_csv(input_csv, output_csv)


# f6
def write_plotdata_polparts(inputlist, output_csv, sort=True):
    if sort:
        inputlist = sorted(inputlist, key=lambda k: int(k['sequence']))
    with open(output_csv, 'w') as csvfile:
        fieldnames = ['Item', 'Whig', 'Tory', 'Others']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in inputlist:
            writer.writerow({
                'Item': item.get('content'),
                'Whig': item.get('whig_wide'),
                'Tory': item.get('tory_wide'),
                'Others': item.get('others_wide')})


io_list_f6 = [
    {
        "input_csv": "output/plot_data/in/180511-hume_all_from_others/politics_summary.csv",
        "output_csv": "output/plot_data/f6_sources_political_hume_all.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-rapin_all_from_others/politics_summary.csv",
        "output_csv": "output/plot_data/_sources_political_rapin_all.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-carte_all_from_others/politics_summary.csv",
        "output_csv": "output/plot_data/_sources_political_carte_all.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-guthrie_all_from_others/politics_summary.csv",
        "output_csv": "output/plot_data/_sources_political_guthrie_all.csv"
    }
]

for item in io_list_f6:
    inputlist = read_csv_to_dictlist(item.get('input_csv'))
    output_csv = item.get('output_csv')
    write_plotdata_polparts(inputlist, output_csv)


def write_plotdata_authortop(input_csv, output_csv, topn, discard_na=True):
    inputlist = read_csv_to_dictlist(f7_input_csv)
    inputlist_sorted = sorted(inputlist, key=lambda k: int(k['fragments']),
                              reverse=True)
    if discard_na:
        for i in range(0, len(inputlist_sorted)):
            if inputlist_sorted[i].get('author') == "NA":
                inputlist_sorted.pop(i)
                break
    inputlist_top = inputlist_sorted[0:topn]
    with open(output_csv, 'w') as csvfile:
        fieldnames = ['Author', 'Fragments', 'Affiliation', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in inputlist_top:
            writer.writerow({
                'Author': item.get('author'),
                'Fragments': item.get('fragments'),
                'Affiliation': item.get('political_views'),
                'link': item.get('link')})


f7_input_csv = "output/plot_data/in/180511-hume_all_from_others/author_totals.csv"
f7_output_csv = "output/plot_data/f7_hume_author_totals_pol_top20.csv"
write_plotdata_authortop(f7_input_csv, f7_output_csv, topn=20, discard_na=True)


# f8-9
io_list_f8_9 = [
    {
        "input_csv": "output/plot_data/in/180511-hume_all_from_others_minus_rushworth/politics_summary.csv",
        "output_csv": "output/plot_data/f8_volumes_all_sources_hume_minus_rushworth.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-hume_all_from_others_minus_rushworth_clarendon/politics_summary.csv",
        "output_csv": "output/plot_data/f9_volumes_all_sources_hume_minus_rushworth_clarendon.csv"
    }
]

for item in io_list_f8_9:
    input_csv = item.get('input_csv')
    inputlist = read_csv_to_dictlist(input_csv)
    output_csv = item.get('output_csv')
    write_plotdata_polparts(inputlist, output_csv)


# f14 -- broken here, do manyally
# f14_input_csv = "output/plot_data/in/180511-hume_all_from_others/0145100107/plotdata_political_views.csv"
# f14_output_csv = "output/plot_data/f14_sources_political_hume7.csv"
# write_plotdata_polparts(read_csv_to_dictlist(f14_input_csv), f14_output_csv, sort=False)

# f16-17
# manually

# f16_input_csv = "output/plot_data/in/180511-hume_all_from_others/author_totals.csv"
# f16_output_csv = "output/plot_data/f7_hume_author_totals_pol_top20.csv"
# write_plotdata_authortop(f7_input_csv, f7_output_csv, topn=20, discard_na=True)


# f18-21

io_list_f18_21 = [
    {
        "input_csv": "output/plot_data/in/180511-hume_all_after/volume_totals.csv",
        "output_csv": "output/plot_data/f18_volumes_all_after_hume.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-guthrie_all_after/volume_totals.csv",
        "output_csv": "output/plot_data/f19_volumes_all_after_guthrie.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-carte_all_after/volume_totals.csv",
        "output_csv": "output/plot_data/f20_volumes_all_after_carte.csv"
    },
    {
        "input_csv": "output/plot_data/in/180511-rapin_all_after/volume_totals.csv",
        "output_csv": "output/plot_data/f21_volumes_all_after_rapin.csv"
    },
]

for item in io_list_f18_21:
    input_csv = item.get('input_csv')
    output_csv = item.get('output_csv')
    write_reuse_totals_by_volume_csv(input_csv, output_csv)

