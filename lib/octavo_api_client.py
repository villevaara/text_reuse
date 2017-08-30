from requests import get


class OctavoAPIClient(object):

    def __init__(self,
                 api_base_address="https://vm0824.kaj.pouta.csc.fi/octavo",
                 limit=100,
                 timeout=300):
        self.api_base_address = api_base_address
        self.limit = limit
        self.timeout = timeout
        self.limit_timeout_part = (
            "&limit=" +
            str(limit) +
            "&timeout=" +
            str(timeout))

    def get_fields_request_part(self, fields):
        fields_string = ""
        if len(fields) > 0:
            for field in fields:
                fields_string = (fields_string + "&field=" + field)
        return fields_string

    def announce_query(self, api_request):
        print("Querying API with: " + api_request)


class OctavoEccoClusterClient(OctavoAPIClient):

    def __init__(self, limit=-1, timeout=300):
        super().__init__(limit=limit, timeout=timeout)
        self.api_request_start = (
            self.api_base_address +
            "/eccocluster" +
            "/search?query=")

    def get_cluster_data_for_document_id(self,
                                         document_id,
                                         fields=["documentID",
                                                 "title",
                                                 "clusterID",
                                                 "startIndex",
                                                 "endIndex",
                                                 "avgLength",
                                                 "text"]):

        fields_part = self.get_fields_request_part(fields)

        api_request = (
            self.api_request_start +
            "documentID:" +
            str(document_id) +
            fields_part +
            self.limit_timeout_part)

        self.announce_query(api_request)
        response = get(api_request)

        data = response.json().get('results').get('docs')
        return data

    def get_wide_cluster_data_for_document_id(self,
                                              document_id,
                                              fields=["documentID",
                                                      "title",
                                                      "clusterID",
                                                      "startIndex",
                                                      "endIndex",
                                                      "text"]):

        fields_part = self.get_fields_request_part(fields)

        api_request = (
            self.api_request_start +
            "<CLUSTER§<CLUSTER§documentID:" +
            str(document_id) +
            "§clusterID>§CLUSTER>" +
            fields_part +
            self.limit_timeout_part)

        self.announce_query(api_request)
        response = get(api_request)

        data = response.json().get('results').get('docs')
        return data


class OctavoEccoClient(OctavoAPIClient):

    def __init__(self, limit=-1, timeout=300):
        super().__init__(limit=limit, timeout=timeout)
        self.api_request_start = (
            self.api_base_address +
            "/ecco" +
            "/search?query=")

    def get_text_for_document_id(self, document_id):
        api_request = (self.api_request_start +
                       "<DOCUMENT§documentID:" +
                       str(document_id) +
                       "§DOCUMENT>&field=content&field=collectionID" +
                       self.limit_timeout_part)

        self.announce_query(api_request)
        response = get(api_request)

        text = response.json().get('results').get('docs')[0].get('content')
        collection = (
            response.json().get('results').get('docs')[0].get('collectionID'))

        retdict = {'text': text, 'collection': collection}
        return retdict
