import json
from metadata_functions import (
    read_estc_dump,
    get_ecco_metadata,
    get_ecco_dump_idpairs
    )


estc_dump = read_estc_dump('data/metadata/estc_dump.csv')
ecco_id_pairs = get_ecco_dump_idpairs('data/metadata/dump_ecco12.json')

# print(estc_dump[1:4])


good_metadata = get_ecco_metadata(estc_dump, ecco_id_pairs)
outputfile = "good_metadata.json"
with open(outputfile, "w") as outfile:
    json.dump(good_metadata, outfile)


# for pair in ecco_id_pairs:
#     if pair.get('eccoid') == '1706901800':
#         print(pair.get('estcid'))
