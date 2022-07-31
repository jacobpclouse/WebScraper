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


# Finding Odd numbered Jobs
for a in soup.findAll(attrs={'class': 'odd'}):

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find Job Title
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    name = a.find('a')
    if name not in results:
        results.append(name.text)
        # Writing out text file to see what is in results
        #writeOutToFile(name.text + '\n',"resultsOut")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find job number
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    number = a.find('td')
    job_number.append(number.text)
    # Writing out text file to see what is in job number
    #writeOutToFile(number.text + '\n',"jobNumbersOut")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find job pay grade
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    grade = a.select("tr > td")[2]
    job_grade.append(grade.text)
    # Writing out text file to see what is in grade
    #writeOutToFile(grade.text + '\n',"gradesOut")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find job application due by
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    dueDate = a.select("tr > td")[4]
    job_due_date.append(dueDate.text)
    # Writing out text file to see what due date is
    #writeOutToFile(dueDate.text + '\n',"dueDate")
    

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find job agency
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    agency = a.select("tr > td")[5]
    job_agency.append(agency.text)
    # Writing out text file to see what is in agency
    #writeOutToFile(agency.text + '\n',"agency")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Find job link
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    links = a.select("tr > td > a ")
    job_links.append(links)
    # Writing out text file to see what is in links -- This one is spotty
    #writeOutToFile(links + '\n',"links")



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Debugging -- Print lists to console
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#print(results)
#print(job_number)
#print(job_grade)
#print(job_due_date)
#print(job_agency)
#print(job_links)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Output to CSV
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
df = pd.DataFrame({'Job Title': results, 'Job Number': job_number, 'Job Grade': job_grade, 'Job Agency': job_agency, 'Application Due By': job_due_date, 'Link To Job': job_links})
df.to_csv('Current Jobs @ NYS.csv', index=False, encoding='utf-8')


# Signaling End of Program
print("Scrapping Completed!")
myLogo()