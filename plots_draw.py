
from plotting_functions import (
    draw_reuse_totals_by_volume,
    draw_sources_comparison,
    draw_headerhits_per_author,
    draw_source_fragments_per_author,
    draw_political_affiliation_by_subitem,
    )


pol_colours = {
    "parliamentarian": "DarkBlue",  # "Peru"
    "whig": "CornflowerBlue",  # "Tan"
    "tory": "firebrick",  # FIREBRICK
    "royalist": "IndianRed",  # "IndianRed"
    "jacobite": "darksalmon",  # "FireBrick" DarkRed maroon
    "no affiliation": "DarkGray",
    "others": "DarkGray"
}

# draw_headerhits_per_author(
#     "output/data_used_for_plots/hume7_sources_fragments_per_author_top20.csv",
#     "docs/hume7_header_authors",
#     "Source Fragments per Author per Header in Hume's History (vol. 7)")

# draw_headerhits_per_author(
#     "output/data_used_for_plots/hume7_sources_fragments_per_author_top10.csv",
#     "docs/hume7_header_authors_top10",
#     "Source Fragments per Author per Header in Hume's History (vol. 7)")

# draw_headerhits_per_author(
#     "output/plot_data/hume6_sources_fragments_per_author_top20.csv",
#     "docs/hume6_header_authors",
#     "Source fragments per author per header in Hume's History, vol. 6")


# 
# --- redraw-ready ---
# 


# 
# POL AFFILIATION PER SUBHEADER INSIDE VOLUME
# 

# draw_political_affiliation_by_subitem(
#     inputcsv="output/data_used_for_plots/carte_sources_political.csv",
#     outputfile="carte_volumes_sources_political",
#     plot_title="Carte's General History of England, source political affiliation by volume",
#     x_title="Volume",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1000)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/data_used_for_plots/guthrie_volumes_sources_political.csv",
#     outputfile="guthrie_volumes_sources_political",
#     plot_title="Guthrie's History of Great Britain, source political affiliation by volume",
#     x_title="Volume",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1000)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/data_used_for_plots/rapin_volumes_sources_political.csv",
#     outputfile="rapin_volumes_sources_political",
#     plot_title="Rapin's History of England, source political affiliation by volume",
#     x_title="Volume",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)


# 
# --- redrawn & saved
# 

#
# --- FIGS 1 ---
#

# draw_sources_comparison(
#     inputcsv="output/plot_data/f1_all_compared_from_others.csv",
#     outputfile="f1_sources_compared",
#     plot_title="Source fragments per octavo page",
#     save_img=True)


#
# --- FIGS 2-5 ---
#

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f2_volumes_all_sources_hume.csv",
#     outputfile="f2_from_others_hume",
#     plot_title="Hume's History of England, source fragments by volume",
#     save_img=True,
#     img_width=1200,
#     img_height=600)

draw_reuse_totals_by_volume(
    inputcsv="output/plot_data/f2b_volumes_all_sources_hume_first_eds.csv",
    outputfile="f2b_from_others_hume",
    plot_title="Hume's History of England, source fragments by volume, first edition",
    save_img=True,
    img_width=1200,
    img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f3_volumes_all_sources_rapin.csv",
#     outputfile="f3_from_others_rapin",
#     plot_title="Rapin's History of England, source fragments by volume",
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f4_volumes_all_sources_guthrie.csv",
#     outputfile="f4_from_others_guthrie",
#     plot_title="Guthrie's History of Great Britain, source fragments by volume",
#     save_img=True,
#     img_width=600,
#     img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f5_volumes_all_sources_carte.csv",
#     outputfile="f5_from_others_carte",
#     plot_title="Carte's General History of England, source fragments by volume",
#     save_img=True,
#     img_width=600,
#     img_height=600)


# 
# --- FIG 6 ---
# 

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f6_sources_political_hume_all.csv",
#     outputfile="f6_sources_political_hume_volumes",
#     plot_title="Hume's History of England, source political affiliation by volume",
#     x_title="Volume",
#     y_range=[0, 300],
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)


# --- FIG 7 ---
# --- FRAGMENTS PER AUTHOR, COLORED BY POLITICAL AFFILIATION ---
# 
# draw_source_fragments_per_author(
#     "output/plot_data/f7_hume_author_totals_pol_top20.csv",
#     "f7_hume_top21_authors",
#     "Source fragments per author (top 20) in Hume's History",
#     pol_colours=pol_colours,
#     save_img=True)


#
# --- FIGS 8-9  ---
#

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f8_volumes_all_sources_hume_minus_rushworth.csv",
#     outputfile="f8_sources_political_hume_volumes_no_rush",
#     plot_title=(
#         "Hume's History, source political affiliation by volume, excluding Rushworth"),
#     x_title="Volume",
#     y_range=[0, 300],
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f9_volumes_all_sources_hume_minus_rushworth_clarendon.csv",
#     outputfile="f9_sources_political_hume_volumes_no_rush_clar",
#     plot_title=(
#         "Hume's History, source political affiliation by volume, excluding Rushworth and Clarendon"),
#     x_title="Volume",
#     y_range=[0, 300],
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)


#
# --- FIGS 10-13  ---
#

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f10_hume6-8_sources_political.csv",
#     outputfile="f10_sources_political_headers_hume6-8",
#     plot_title=(
#         "Hume's History vols. 6-8," +
#         " source political affiliation by header"),
#     x_title="Header",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f11_rapin11-12_pol_headers.csv",
#     outputfile="f11_sources_political_headers_rapin11-12",
#     plot_title=(
#         "Rapin's History vols. 11-12," +
#         " source political affiliation by header"),
#     x_title="Header",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f12_guthrie4_sources_political.csv",
#     outputfile="f12_sources_political_headers_guthrie4",
#     plot_title="Guthrie's History vol. 4, source political affiliation by header",
#     x_title="Header",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1000)

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f13_carte4_sources_political.csv",
#     outputfile="f13_sources_political_headers_carte4",
#     plot_title="Carte's History vol. 4, source political affiliation by header",
#     x_title="Header",
#     pol_colours=pol_colours,
#     save_img=True,
#     img_width=1000)


# 
# --- FIG 14 ---
# 

# draw_political_affiliation_by_subitem(
#     inputcsv="output/plot_data/f14_sources_political_hume7.csv",
#     outputfile="sources_political_headers_hume7",
#     plot_title="Hume's History vol. 7, source political affiliation by header",
#     x_title="Header",
#     pol_colours=pol_colours,
#     save_img=True)

# 
# --- FIG 15 ---
# 

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f15_hume6-7_clarendon_only.csv",
#     outputfile="f15_hume6-7_clarendon_only",
#     plot_title="Clarendon as source in Hume's History, vols. 6-7",
#     x_title='Header',
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# 
# --- FIG 16-17 ---
# 

# draw_headerhits_per_author(
#     "output/plot_data/f16_hume6_fragments_per_author_top20.csv",
#     "f16_hume6_header_authors",
#     "Source fragments per author per header in Hume's History, vol. 6",
#     save_img=True)

# draw_headerhits_per_author(
#     "output/plot_data/f17_hume7_fragments_per_author_top20.csv",
#     "f17_hume7_header_authors",
#     "Source fragments per author per header in Hume's History, vol. 7",
#     save_img=True)


## FIG 18-21

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f18_volumes_all_after_hume.csv",
#     outputfile="f18_hume_reused_later",
#     plot_title="Hume's History reused by others",
#     save_img=True,
#     img_width=1200,
#     img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f19_volumes_all_after_guthrie.csv",
#     outputfile="f19_guthrie_reused_later",
#     plot_title="Guthrie's History reused by others",
#     save_img=True,
#     img_width=600,
#     img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f20_volumes_all_after_carte.csv",
#     outputfile="f20_carte_reused_later",
#     plot_title="Carte's History reused by others",
#     save_img=True,
#     img_width=600,
#     img_height=600)

# draw_reuse_totals_by_volume(
#     inputcsv="output/plot_data/f21_volumes_all_after_rapin.csv",
#     outputfile="f21_rapin_reused_later",
#     plot_title="Rapin's History reused by others",
#     save_img=True,
#     img_width=1200,
#     img_height=600)

