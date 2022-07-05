#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
import requests
import json

#=-=-=-=-=-=-
# Functions
#=-=-=-=-=-=-
#  --- Function to write out to file --- 
def writeOutToFile(outgoingData,fileName):
    with open(f'./{fileName}.json', 'a') as z:
        json.dump(outgoingData,z,indent=2)



#=-=-=-=-=-=-
# MAIN
#=-=-=-=-=-=-

form_data = {'key1': 'value1', 'key2': 'value2'}
response = requests.post("https://oxylabs.io/ ", data=form_data)
print(response.text)

#response = requests.get("https://oxylabs.io/")


#writeOutToFile((response.text),"output")