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
def writeOutToFile(outgoingData,fileName):
    with open(f'./{fileName}.txt', 'a') as z:
        z.write(outgoingData)

# put in func to get date time
# put in func to get host scrapped


#=-=-=-=-=-=-
# MAIN
#=-=-=-=-=-=-

#url='https://oxylabs.io/blog'
#url = "https://shootthezombies.com"
url = "https://www.amazon.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)



blog_titles = soup.findAll('div', attrs={"class":"celwidget"})
for title in blog_titles:
    print(title.text)
# Output:
# Prints all blog tiles on the page

    writeOutToFile(title.text,'scrapped_Data')