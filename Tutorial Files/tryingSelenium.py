#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
from cgitb import html
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


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

driver = Chrome(executable_path='/usr/bin/google-chrome')


#url = "https://shootthezombies.com"
#response = requests.get(url)

driver.get('https://oxylabs.io/blog')

blog_titles = driver.get_elements_by_css_selector(' h2.blog-card__content-title')
for title in blog_titles:
    print(title.text)
driver.quit() # closing the browser