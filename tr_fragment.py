import re

from text_reuse_octavoapi_common import (
    get_text_for_document_id_from_api,
    )
from text_reuse_common import (
    get_location_from_estc,
    get_author_from_estc,
    get_year_from_estc,
    get_estcid_from_estc,
    get_title_from_estc,
    )


class TextReuseFragment(object):

    def __init__(self, ecco_id, cluster_id,
                 text, start_index, end_index):
        self.estc_id = None
        self.ecco_id = ecco_id
        self.cluster_id = cluster_id
        self.title = None
        self.author = None
        self.year = None
        self.text = text
        self.location = None
        self.start_index = start_index
        self.end_index = end_index
        self.text_before = None
        self.text_after = None
        self.find_start_index = -1
        self.find_end_index = -1
        self.document_length = None

    def add_metadata(self, good_metadata):
        self.location = get_location_from_estc(
            self.ecco_id, good_metadata)
        self.author = get_author_from_estc(
            self.ecco_id, good_metadata)
        self.estc_id = get_estcid_from_estc(
            self.ecco_id, good_metadata)
        self.year = get_year_from_estc(
            self.ecco_id, good_metadata)
        self.title = get_title_from_estc(
            self.ecco_id, good_metadata)

    def add_context(self, window_size=2000):
        document_text_data = get_text_for_document_id_from_api(self.ecco_id)
        document_text = document_text_data.get('text')
        document_collection = document_text_data.get('collection')
        document_text_stripped = ' '.join(document_text.split())

        # if collection is ecco1, convert to ascii. else unicode
        if document_collection == "ecco1":
            document_text_stripped = re.sub(r'[^\x00-\x7f]',
                                            r'', document_text_stripped)

        document_text_stripped_length = len(document_text_stripped)
        self.document_length = document_text_stripped_length

        fragment_start_index = document_text_stripped.find(self.text)

        if fragment_start_index == -1:
            print("Fragment text not found in fulltext!")
            return

        self.find_start_index = fragment_start_index
        self.find_end_index = (fragment_start_index +
                               len(self.text))

        context_before_start_index = self.find_start_index - window_size
        if context_before_start_index < 0:
            print("Fragment context start index before document start!")
            context_before_start_index = 0
        context_before_end_index = fragment_start_index

        self.text_before = (document_text_stripped[
            context_before_start_index:context_before_end_index])

        context_after_start_index = self.find_end_index
        context_after_end_index = context_after_start_index + window_size
        if context_after_end_index > document_text_stripped_length:
            print("Fragment context end index larger than document length!")
            context_after_end_index = document_text_stripped_length

        self.text_after = (document_text_stripped[
            context_after_start_index:context_after_end_index])
