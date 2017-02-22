from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from reuse_database_sqlalchemy_declarative import (Cluster,
                                                   Book,
                                                   Base,
                                                   Extract)
# from text_reuse_common import (
#     load_good_metadata,
#     process_cluster
# )
from metadata_functions import (
    read_estc_dump,
    check_metadata_int,
    get_ecco_dump_dict)
import json
import glob


def filter_estc_books(estc_books, ecco_dump_dict):
    keys_accepted = ecco_dump_dict.values()
    return_dict = {key: estc_books[key] for key in
                   keys_accepted if key in estc_books}
    return return_dict


def commit_datadir_to_db(session, datadir, ecco_dump_dict, test=False):
    # filenames = glob.glob(datadir + "clusters_0")
    if test:
        filenames = glob.glob(datadir + "clusters_0")
    else:
        filenames = glob.glob(datadir + "clusters*")
    filenames_length = len(filenames)

    i = 1
    for filename in filenames:
        print('processing file ' + i + '/' + filenames_length)
        i = i + 1
        with open(filename) as cluster_data_file:

            cluster_data = json.load(cluster_data_file)
            cluster_data_len = len(cluster_data)
            i = 0
            for key, value in cluster_data.items():
                cluster_id = int(key[8:])
                cluster_count = int(value.get('Count'))
                cluster_avglength = int(value.get('Avglength'))

                new_cluster = Cluster(id=cluster_id,
                                      avglength=cluster_avglength,
                                      count=cluster_count)
                session.add(new_cluster)

                hits = value.get('Hits')
                for hit in hits:
                    extract_text = hit.get('text')
                    extract_cluster_id = cluster_id
                    extract_ecco_id = hit.get('book_id')
                    estc_id = ecco_dump_dict.get(extract_ecco_id)
                    if estc_id in estc_books.keys():
                        extract_book_id = estc_books.get(estc_id)
                    else:
                        print(estc_id + ' not found in estc metadata')
                        extract_book_id = None
                    new_extract = Extract(text=extract_text,
                                          cluster_id=extract_cluster_id,
                                          book_id=extract_book_id,
                                          ecco_id=extract_ecco_id)
                    session.add(new_extract)
                i = i + 1
                if i % 100 == 0:
                    session.commit()
                    print(str(filename) + ' --- db commit ok cluster_' +
                          str(cluster_id) +
                          ' --- ' + str(i) + '/' + str(cluster_data_len))


def commit_estc_metadata_to_db(session, estc_books):
    i = 0
    upto = len(estc_books)
    for key, value in estc_books.items():
        new_book = Book(id=value.get('id'),
                        title=value.get('title'),
                        author=value.get('author'),
                        author_birth=check_metadata_int(
                            value.get('author_birth')),
                        author_death=check_metadata_int(
                            value.get('author_death')),
                        language=value.get('language'),
                        publication_year=check_metadata_int(
                            value.get('publication_year')),
                        publication_place=value.get('publication_place'),
                        country=value.get('country'),
                        publisher=value.get('publisher'))
        session.add(new_book)
        i = i + 1
        if i % 100 == 0:
            session.commit()
            print('metadata db commit ok at: ' + str(i) + '/' + str(upto))


engine = create_engine('sqlite:///sqlalchemy_text_reuse.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Person in the person table
# new_cluster = Cluster(id=1001794, avglength=1876)
# session.add(new_cluster)
# session.commit()


# good_metadata_jsonfile = "data/metadata/good_metadata.json"
# good_metadata = load_good_metadata(good_metadata_jsonfile)

ecco_dump_file = 'data/metadata/dump_ecco12.json'
ecco_dump_dict = get_ecco_dump_dict(ecco_dump_file)
estc_books = read_estc_dump('data/metadata/estc_dump.csv')
estc_books = filter_estc_books(estc_books, ecco_dump_dict)


datadir = "data/test/"
commit_estc_metadata_to_db(session, estc_books)
commit_datadir_to_db(session, datadir, ecco_dump_dict)
