import json
from metadata_functions import (
    read_estc_dump,
    get_ecco_metadata,
    get_ecco_dump_idpairs,
    read_first_ed_years,
    get_eebo_dump_idpairs
    )


first_ed_years = read_first_ed_years("data/first_ed_years.csv")
estc_dump = read_estc_dump('data/metadata/estc_dump.csv')
ecco_id_pairs = get_ecco_dump_idpairs('data/metadata/dump_ecco12.json')


eebo1_json_file = "data/eebo1ids.json"
eebo1_id_pairs = get_eebo_dump_idpairs(eebo1_json_file)
eebo2_json_file = "data/eebo2ids.json"
eebo2_id_pairs = get_eebo_dump_idpairs(eebo2_json_file)

ecco_id_pairs.extend(eebo1_id_pairs)
ecco_id_pairs.extend(eebo2_id_pairs)


# write metadatafile
good_metadata = get_ecco_metadata(estc_dump, ecco_id_pairs, first_ed_years)
outputfile = "good_metadata.json"
with open(outputfile, "w") as outfile:
    json.dump(good_metadata, outfile)


# for pair in ecco_id_pairs:
#     if pair.get('eccoid') == '1706901800':
#         print(pair.get('estcid'))
