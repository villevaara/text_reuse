import csv
import json


def read_first_ed_years(csv_file):
    with open(csv_file) as first_ed_year_file:
        reader = csv.DictReader(first_ed_year_file)
        first_ed_years = {}
        for row in reader:
            first_ed_years[row.get('estcid')] = row.get('first_ed_year')
        return first_ed_years


def read_estc_dump(csv_file):
    with open(csv_file) as estc_dump_file:
        reader = csv.DictReader(estc_dump_file)
        estc_dump_data = dict()
        for row in reader:
            key = row.get('id')
            estc_dump_data[key] = row
        return estc_dump_data


def fix_estc_id(estcid):
    estcid_start = estcid[0]
    estcid_rest = estcid[1:]
    estcid_rest = estcid_rest.lstrip("0")
    fixed_estcid = estcid_start + estcid_rest
    return fixed_estcid


def get_ecco_dump_idpairs(json_file):
    with open(json_file) as ecco_dump_file:
        ecco_data = json.load(ecco_dump_file)
        ecco_id_pairs = list()
        for row in ecco_data:
            eccoid = row.get('documentID')
            estcid = row.get('ESTCID')
            estcid = fix_estc_id(estcid)
            id_pair = {'eccoid': eccoid, 'estcid': estcid}
            ecco_id_pairs.append(id_pair)
        return ecco_id_pairs


def get_ecco_dump_dict(json_file):
    ecco_dict = {}
    with open(json_file) as ecco_dump_file:
        ecco_data = json.load(ecco_dump_file)
        for row in ecco_data:
            eccoid = row.get('documentID')
            estcid = row.get('ESTCID')
            estcid = fix_estc_id(estcid)
            ecco_dict[eccoid] = estcid
        return ecco_dict


def get_eebo_dump_idpairs(json_file):
    with open(json_file) as eebo_dump_file:
        json_data = json.load(eebo_dump_file)
        eebo_data = json_data.get('results').get('docs')
        eebo_id_pairs = list()
        for row in eebo_data:
            eccoid = row.get('documentID')
            estcid = row.get('ESTCID')
            estcid = fix_estc_id(estcid)
            id_pair = {'eccoid': eccoid, 'estcid': estcid}
            eebo_id_pairs.append(id_pair)
        return eebo_id_pairs


def get_ecco_metadata(estc_dump, ecco_id_pairs, first_ed_years):
    good_metadata = dict()
    for id_pair in ecco_id_pairs:
        eccoid = id_pair.get('eccoid')
        estcid = id_pair.get('estcid')
        first_ed_year = first_ed_years.get(estcid)
        estc_metadata = estc_dump.get(estcid)
        # print("id: " + str(estcid))

        if estc_metadata is None:
            print(str(eccoid) + "," + str(estcid))
            estc_author = 'ESTC DATA MISSING'
            estc_author_birth = 'ESTC DATA MISSING'
            estc_author_death = 'ESTC DATA MISSING'
            estc_publication_year = 'ESTC DATA MISSING'
            estc_publisher = 'ESTC DATA MISSING'
            estc_publication_place = 'ESTC DATA MISSING'
            estc_title = 'ESTC DATA MISSING'
            estc_language = 'ESTC DATA MISSING'
            estc_country = 'ESTC DATA MISSING'
        else:
            estc_author = estc_metadata.get('author')
            estc_author_birth = estc_metadata.get('author_birth')
            estc_author_death = estc_metadata.get('author_death')
            estc_publication_year = estc_metadata.get('publication_year')
            estc_publisher = estc_metadata.get('publisher')
            estc_publication_place = estc_metadata.get('publication_place')
            estc_title = estc_metadata.get('title')
            estc_language = estc_metadata.get('language')
            estc_country = estc_metadata.get('country')
        new_row = {'ecco_id': eccoid,
                   'estc_id': estcid,
                   'estc_author': estc_author,
                   'estc_author_birth': estc_author_birth,
                   'estc_author_death': estc_author_death,
                   'estc_publication_year': estc_publication_year,
                   'estc_publisher': estc_publisher,
                   'estc_publication_place': estc_publication_place,
                   'estc_title': estc_title,
                   'estc_language': estc_language,
                   'estc_country': estc_country,
                   'first_ed_year': first_ed_year}
        good_metadata[eccoid] = new_row
    return good_metadata


def check_metadata_int(metadata_value):
    if metadata_value == 'NA' or metadata_value == '' or 'ESTC DATA MISSING':
        metadata_value = None
    else:
        metadata_value = int(metadata_value)
    return metadata_value
