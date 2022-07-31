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
job_due_date = []
job_agency = []
job_links = []

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
        #writeOutToFile(name.text + '\n',"resultsOut")

#print(results)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Find job number
for b in soup.findAll(attrs={'class': 'odd'}):
    number = b.find('td')
    job_number.append(number.text)

    # Writing out text file to see what is in job number
    #writeOutToFile(number.text + '\n',"jobNumbersOut")

#print(job_number)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Find job pay grade
for c in soup.findAll(attrs={'class': 'odd'}):
    grade = c.select("tr > td")[2]
    job_grade.append(grade.text)

    # Writing out text file to see what is in grade
    #writeOutToFile(grade.text + '\n',"gradesOut")

#print(job_grade)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Find job application due by
for d in soup.findAll(attrs={'class': 'odd'}):
    dueDate = d.select("tr > td")[4]
    job_due_date.append(dueDate.text)

    # Writing out text file to see what is in grade
    #writeOutToFile(dueDate.text + '\n',"dueDate")

#print(job_due_date)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Find job agency
for e in soup.findAll(attrs={'class': 'odd'}):
    agency = e.select("tr > td")[5]
    job_agency.append(agency.text)

    # Writing out text file to see what is in grade
    #writeOutToFile(agency.text + '\n',"agency")

#print(job_agency)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Find job link
for f in soup.findAll(attrs={'class': 'odd'}):
    links = f.select("tr > td > a ")
    job_links.append(links)

    # Writing out text file to see what is in links
    #writeOutToFile(links + '\n',"links")

#print(job_links)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Output to CSV
df = pd.DataFrame({'Job Title': results, 'Job Number': job_number, 'Job Grade': job_grade, 'Job Agency': job_agency, 'Application Due By': job_due_date, 'Link To Job': job_links})
df.to_csv('Current Jobs @ NYS.csv', index=False, encoding='utf-8')


# Signaling End of Program
print("Scrapping Completed!")
myLogo()