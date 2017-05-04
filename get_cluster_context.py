from requests import get

api_address = "https://vm0542.kaj.pouta.csc.fi/ecco_octavo_api/search?query="
query_content = "%3CDOCUMENT%7CdocumentID:0156400400%7CDOCUMENT%3E"
query_fields = (
    "&field=ESTCID&field=fullTitle" +
    "&field=documentID&field=content&field=documentLength")
request_address = api_address + query_content + query_fields
response = get(request_address)

data = response.json()
data_results = data.get('results').get('docs')[0]
data_content = data_results.get('content')
data_documentid = data_results.get('documentID')


data_cont = data_content.replace('\\\'', '\'')
data_cont = data_cont.replace("\\\"", "\"")
data_cont = data_cont.replace("\\\n", " ")

# find cluster text in whole text
with open('data/testdata/hume_test.txt', 'r') as myfile:
    testdata = myfile.read().replace('\n', '')

data_content.find(testdata)
