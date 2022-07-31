#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
from cgitb import html
import requests
from bs4 import BeautifulSoup
import json


#=-=-=-=-=-=-
# Functions
#=-=-=-=-=-=-
#  --- Function to write out to file --- 
# def writeOutToFile(outgoingData,fileName):
#     with open(f'./{fileName}.json', 'a') as z:
#         html.dump(outgoingData,z,indent=2)


#=-=-=-=-=-=-
# MAIN
#=-=-=-=-=-=-

# url='https://oxylabs.io/blog'
#url='https://www.albany.edu/'
url = 'https://shootthezombies.com'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)