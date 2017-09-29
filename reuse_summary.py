from lib.utils_common import (read_csv_to_dictlist,
                              write_csv_from_dictlist)
from lib.text_reuse_common import (load_good_metadata,
                                   get_author_from_estc,
                                   get_estcid_from_estc,
                                   get_location_from_estc,
                                   get_year_from_estc,
                                   get_title_from_estc)


def enrich_reuse_summary(reuse_summary, metadata):
    for row in reuse_summary:
        row['title'] = get_title_from_estc(row['document_id'], metadata)
        row['year'] = get_year_from_estc(row['document_id'], metadata)
        row['author'] = get_author_from_estc(row['document_id'], metadata)
        row['location'] = get_location_from_estc(row['document_id'], metadata)
        row['estcid'] = get_estcid_from_estc(row['document_id'], metadata)


reuse_summary = read_csv_to_dictlist('data/reuse_summary.csv')
metadata = load_good_metadata('data/metadata/good_metadata.json')
enrich_reuse_summary(reuse_summary, metadata)
write_csv_from_dictlist(reuse_summary, 'output/enriched_reuse_summary.csv')

# * sum by ESTCID
# * get top20 titles by decade
# * get top20 authors by decade
