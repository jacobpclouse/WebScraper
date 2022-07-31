#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


#=-=-=-=-=-=-
# Variables
#=-=-=-=-=-=-
driver = webdriver.Chrome(executable_path='/usr/bin/google-chrome')
driver.get('https://www.ebay.com')

results = []
other_results = []
content = driver.page_source
soup = BeautifulSoup(content)

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

for a in soup.findAll(attrs={'class': 'widgets-placeholder'}):
    name = a.find('a')
    if name not in results:
        results.append(name.text)

for b in soup.findAll(attrs={'class': 'hl-card-header__title'}):
    name2 = b.find('span')
    other_results.append(name.text)


series1 = pd.Series(results, name = 'Names')
series2 = pd.Series(other_results, name = 'Categories')

df = pd.DataFrame({'Names': series1, 'Categories': series2})
df.to_csv('names.csv', index=False, encoding='utf-8')
