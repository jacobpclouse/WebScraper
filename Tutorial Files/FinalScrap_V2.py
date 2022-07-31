#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
from cgitb import html
from unittest import result
import requests
from bs4 import BeautifulSoup
import pandas as pd

#=-=-=-=-=-=-
# Variables
#=-=-=-=-=-=-
results = []
other_results = []

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

url = "https://statejobs.ny.gov/public/vacancyTable.cfm"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)
for a in soup.findAll(attrs={'class': 'odd'}):
    name = a.find('a')
    if name not in results:
        results.append(name.text)
        writeOutToFile(name.text + '\n',"resultsOut")

print(results)

# Output to CSV
df = pd.DataFrame({'Jobs': results})
df.to_csv('Jobs.csv', index=False, encoding='utf-8')

"""# appending odd classes


for b in soup.findAll(attrs={'class': 'even'}):
    name2 = b.find('span')
    other_results.append(name.text)

series1 = pd.Series(results, name = 'Names')
series2 = pd.Series(other_results, name = 'Categories')
df = pd.DataFrame({'Names': series1, 'Categories': series2})
df.to_csv('names.csv', index=False, encoding='utf-8')
"""

'''
blog_titles = soup.findAll('tr', attrs={"class":"odd"})
for title in blog_titles:
    print(title.text)
    writeOutToFile(title.text,'scrapped_NYS_Jobs_Odd_Classes')
'''