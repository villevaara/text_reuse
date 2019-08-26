# find_ecco_id.py


from lib.octavo_api_client import (
    OctavoEccoClient,
    )


def print_response(responsedata):
    if len(responsedata) == 0:
        print("\nNo match\n")
    else:
        for item in responsedata:
            print()
            for key, value in item.items():
                print(key + ": " + str(value))
            print()


ecco_api_client = OctavoEccoClient()

print_response(ecco_api_client.get_estc_id_metadata("R223440"))

# estc_id = "T136947"
# estc_id = "R223440"
# responsedata = ecco_api_client.get_estc_id_metadata(estc_id)
# print_response(responsedata)
