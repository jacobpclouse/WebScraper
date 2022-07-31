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
job_number = []
job_grade = []

#=-=-=-=-=-=-
# Functions
#=-=-=-=-=-=-
#  --- Function to write out to file --- 
def writeOutToFile(outgoingData,fileName):
    with open(f'./{fileName}.txt', 'a') as z:
        z.write(outgoingData)

# put in func to get date time
# put in func to get host scrapped

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")


#=-=-=-=-=-=-
# MAIN
#=-=-=-=-=-=-

url = "https://statejobs.ny.gov/public/vacancyTable.cfm"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Printing Title of Webpage
print(soup.title)


# Finding Odd numbered Jobs -- Job Titles
for a in soup.findAll(attrs={'class': 'odd'}):
    name = a.find('a')
    if name not in results:
        results.append(name.text)

        # Writing out text file to see what is in results
        writeOutToFile(name.text + '\n',"resultsOut")

#print(results)

# Find job number
for b in soup.findAll(attrs={'class': 'odd'}):
    number = b.find('td')
    job_number.append(number.text)

    # Writing out text file to see what is in results
    writeOutToFile(number.text + '\n',"jobNumbersOut")

print(job_number)


for c in soup.findAll(attrs={'class': 'odd'}):
    grade = c.select("tr > td")[2]
    job_grade.append(grade.text)

    # Writing out text file to see what is in results
    writeOutToFile(grade.text + '\n',"gradesOut")

print(job_grade)

# Output to CSV
df = pd.DataFrame({'Job Title': results, 'Job Number': job_number, 'Job Grade': job_grade})
df.to_csv('Current Jobs.csv', index=False, encoding='utf-8')

print("Scrap Completed!")
myLogo()