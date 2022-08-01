#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
from cgitb import html
from unittest import result
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

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

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

# --- Function to print get url ---
def getJobs(inputUrl, evenOrOdd):
    response = requests.get(inputUrl)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Printing Title of Webpage
    print(soup.title)


    # Finding even and odd numbered Jobs
    #for a in soup.findAll(attrs={'class': f'{evenOrOdd}'}):
    #for a in soup.findAll('tbody > tr'):
    for a in soup.findAll(attrs={'class': ('even', 'odd')}):

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find Job Title
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        name = a.find('a')
        # if name not in results:
        #     results.append(name.text)
        results.append(name.text)
            # Writing out text file to see what is in results
            #writeOutToFile(name.text + '\n',f"resultsOut_{evenOrOdd}")


    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job number
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        number = a.find('td')
        job_number.append(number.text)
        # Writing out text file to see what is in job number
        #writeOutToFile(number.text + '\n',f"jobNumbersOut_{evenOrOdd}")


    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job pay grade
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        grade = a.select("tr > td")[2]
        job_grade.append(grade.text)
        # Writing out text file to see what is in grade
        #writeOutToFile(grade.text + '\n',f"gradesOut_{evenOrOdd}")


    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job application due by
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        dueDate = a.select("tr > td")[4]
        job_due_date.append(dueDate.text)
        # Writing out text file to see what due date is
        #writeOutToFile(dueDate.text + '\n',f"dueDate_{evenOrOdd}")
        

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job agency
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        agency = a.select("tr > td")[5]
        job_agency.append(agency.text)
        # Writing out text file to see what is in agency
        #writeOutToFile(agency.text + '\n',f"agency_{evenOrOdd}")


    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job link
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        links = a.select("tr > td > a ")
        job_links.append(links)
        # Writing out text file to see what is in links -- This one is spotty
        #writeOutToFile(links + '\n',f"links_{evenOrOdd}")



    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Debugging -- Print lists to console
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print(results)
    print(job_number)
    print(job_grade)
    print(job_due_date)
    print(job_agency)
    print(job_links)


    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Output to CSV
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    df = pd.DataFrame({'Job Title': results, 'Job Number': job_number, 'Job Grade': job_grade, 'Job Agency': job_agency, 'Application Due By': job_due_date, 'Link To Job': job_links})
    df.to_csv(f'Current Jobs @ NYS {evenOrOdd}.csv', index=False, encoding='utf-8')



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

# Grab current date & time from function & store in variable
use_this_datetime = defang_datetime()

# NYS JOBS Target URL
url = "https://statejobs.ny.gov/public/vacancyTable.cfm"

# Get Even Designated Jobs CSV
getJobs(url,use_this_datetime)

# Get Odd Designated Jobs CSV
#getJobs(url,"odd")


# Signaling End of Program
print("Scrapping Completed!")
myLogo()