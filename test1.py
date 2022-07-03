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
response = requests.get("https://oxylabs.io/")
#print(response.text)
writeOutToFile((response.text),"output")