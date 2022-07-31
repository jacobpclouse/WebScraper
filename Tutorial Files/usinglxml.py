#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
from cgitb import html
import requests
from bs4 import BeautifulSoup
#from lxml import html


#=-=-=-=-=-=-
# Functions
#=-=-=-=-=-=-
#  --- Function to write out to file --- 
def writeOutToFile(outgoingData,fileName):
    with open(f'./{fileName}.txt', 'a') as z:
#        html.dump(outgoingData,z,indent=2)
        z.write(outgoingData)


#=-=-=-=-=-=-
# MAIN
#=-=-=-=-=-=-

#url='https://oxylabs.io/blog'
url = "https://shootthezombies.com"
response = requests.get(url)

# After response = requests.get() 
from lxml import html
tree = html.fromstring(response.text)

blog_titles = tree.xpath('//h2[@class="featurette-heading highlight pb-md-4"]/text()')
for title in blog_titles:
    print(title)


'''
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)



blog_titles = soup.findAll('h2', attrs={"class":"featurette-heading highlight pb-md-4"})
for title in blog_titles:
    print(title.text)
# Output:
# Prints all blog tiles on the page

    writeOutToFile(title.text,'shootthezombiesh3')
'''