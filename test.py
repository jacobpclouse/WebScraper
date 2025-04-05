import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import csv

import tkinter as tk
from tkinter import filedialog, StringVar, IntVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

DEFAULT_FOLDER = "OUTPUTS"
URL = "https://statejobs.ny.gov/public/vacancyTable.cfm"
JOB_SPECIFIC_URL = "https://statejobs.ny.gov/public/vacancyDetailsView.cfm?id="

TEXT_SIZE = 12
APP_TITLE = "NYS Web Scraper"
APP_SIZE = "900x750"
APP_THEME = "vapor"

PREDEFINED_FILTERS = {
    "All Jobs": [],
    "IT Jobs": ["ITS2", "Information Technology Specialist", "Computer Programmer"],
    "Office Jobs": ["Office Assistant", "HR Specialist", "Human Resources Technician", "Business Analyst"],
    "Internships": ["Intern", "Internship"]
}


class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)

        self.filter_category = StringVar(value="All Jobs")
        self.custom_filters = StringVar(value="")
        self.save_path = StringVar(value=os.path.expanduser("~/Downloads"))

        self.job_results = []
        self.build_ui()


    def build_ui(self):
        ttk.Label(self.root, text=APP_TITLE, font=("Helvetica", 18, "bold")).pack(pady=10)

        # Filter Dropdown
        dropdown_frame = ttk.Frame(self.root)
        dropdown_frame.pack(pady=10)
        ttk.Label(dropdown_frame, text="Select Job Filter:", font=("Helvetica", TEXT_SIZE)).pack(side=LEFT, padx=5)
        filter_menu = ttk.Combobox(dropdown_frame, values=list(PREDEFINED_FILTERS.keys()),
                                   textvariable=self.filter_category, state="readonly", width=30)
        filter_menu.pack(side=LEFT, padx=5)
        ttk.Button(dropdown_frame, text="Apply Filter", command=self.populate_filter_box).pack(side=LEFT)

        # Filter Textbox
        ttk.Label(self.root, text="Edit Filters (comma-separated):", font=("Helvetica", TEXT_SIZE)).pack()
        self.filter_entry = ttk.Entry(self.root, textvariable=self.custom_filters, width=80)
        self.filter_entry.pack(pady=5)

        # Save location
        location_frame = ttk.Frame(self.root)
        location_frame.pack(pady=5)
        ttk.Label(location_frame, text="Save Location:", font=("Helvetica", TEXT_SIZE)).pack(side=LEFT, padx=5)
        ttk.Entry(location_frame, textvariable=self.save_path, width=50).pack(side=LEFT)
        ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(side=LEFT, padx=5)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Start Scraping", bootstyle=SUCCESS, command=self.start_scraping).pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text="Download CSV", bootstyle=PRIMARY, command=self.save_to_csv).pack(side=LEFT, padx=10)

        # Log Output
        ttk.Label(self.root, text="Log Output:", font=("Helvetica", TEXT_SIZE)).pack()
        self.log_output = tk.Text(self.root, height=20, width=100)
        self.log_output.pack(pady=5)

    def populate_filter_box(self):
        category = self.filter_category.get()
        filters = PREDEFINED_FILTERS.get(category, [])
        self.custom_filters.set(", ".join(filters))

    def browse_location(self):
        folder_selected = filedialog.askdirectory(initialdir=self.save_path.get())
        if folder_selected:
            self.save_path.set(folder_selected)

    def log(self, message):
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)

    def start_scraping(self):
        self.job_results = []
        self.log("Starting job scrape...\n")

        filters = [f.strip().lower() for f in self.custom_filters.get().split(",") if f.strip()]
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        jobs = self.scrape_jobs(URL)
        self.job_results = self.filter_jobs(jobs, filters)

        self.log(f"\nTotal matching jobs: {len(self.job_results)}")

    def scrape_jobs(self, url):
        self.log("Fetching job list from NYS Jobs site...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        jobs = []
        for row in soup.find_all("tr", class_=["even", "odd"]):
            cols = row.find_all("td")
            if len(cols) < 6:
                continue
            job_id = cols[0].text.strip()
            title = cols[1].text.strip()
            agency = cols[5].text.strip()
            link = f"{JOB_SPECIFIC_URL}{job_id}"

            job_data = {
                "Job ID": job_id,
                "Title": title,
                "Agency": agency,
                "Link": link
            }

            self.log(f"Found job: {title}")
            jobs.append(job_data)

        return jobs

    def filter_jobs(self, jobs, filters):
        if not filters:
            return jobs
        filtered = []
        for job in jobs:
            title_lower = job["Title"].lower()
            if any(f in title_lower for f in filters):
                filtered.append(job)
        return filtered

    def save_to_csv(self):
        if not self.job_results:
            self.log("No job data to save!")
            return

        filename = f"NYS_Jobs_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        filepath = os.path.join(self.save_path.get(), filename)
        try:
            with open(filepath, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.job_results[0].keys())
                writer.writeheader()
                writer.writerows(self.job_results)
            self.log(f"Saved CSV to: {filepath}")
        except Exception as e:
            self.log(f"Error saving CSV: {e}")


# Run it!
if __name__ == "__main__":
    root = ttk.Window(themename=APP_THEME)
    app = WebScraperApp(root)
    root.mainloop()
'''
#=-=-=-=-=-=-
# Imports
#=-=-=-=-=-=-
import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import csv

from tkinter import filedialog, messagebox, StringVar, IntVar 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


#=-=-=-=-=-=-
# Variables
#=-=-=-=-=-=-


DEFAULT_FOLDER = "OUTPUTS"
# NYS JOBS Target URL
URL = "https://statejobs.ny.gov/public/vacancyTable.cfm" # this is the one for the general jobs page
JOB_SPECIFIC_URL = "https://statejobs.ny.gov/public/vacancyDetailsView.cfm?id=" # this is the one we us in conjuction with the job # to get job specifics

job_all_attributes = []


# Global text size
TEXT_SIZE = 12
APP_TITLE = "NYS Web Scraper"
APP_SIZE = "800x700"
APP_THEME="vapor"


class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)
        
        # Variables
        self.url_var = StringVar()
        self.format_var = StringVar(value="all")
        self.location_var = StringVar(value=os.path.expanduser("~/Downloads"))
        self.filename_var = StringVar()
        self.progress_var = IntVar(value=0)
        self.theme_var = StringVar(value=APP_THEME)

        # Build UI
        self.build_ui()

    def build_ui(self):
        # Theme Selector
        ttk.Label(self.root, text="Select Theme:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
        theme_frame = ttk.Frame(self.root)
        theme_frame.pack(pady=5)
        ttk.Combobox(theme_frame, values=ttk.Style().theme_names(), textvariable=self.theme_var, state="readonly", width=20).pack(side=LEFT, padx=5)
        ttk.Button(theme_frame, text="Apply Theme", command=self.apply_theme).pack(side=LEFT, padx=5)


        # theme_frame for same line, self.root for different line
        ttk.Labelframe(self.root, text='My widgets')
        ttk.Labelframe(self.root, text='My widgets', style='info.TLabelframe')

        # frm = ttk.Frame(self.root, style='danger.TFrame').pack(pady=5)
        # lbl = ttk.Label(self.root, text='Hello world!', style='danger.Inverse.TLabel').pack(pady=5)


        # URL Input
        ttk.Label(self.root, text="CHANGE** YouTube URL:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
        ttk.Entry(self.root, textvariable=self.url_var, width=50, font=("Helvetica", TEXT_SIZE)).pack(pady=5)

        # Choose filter - All or IT jobs
        ttk.Label(self.root, text="Format:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=5)
        ttk.Radiobutton(format_frame, text="All Jobs", variable=self.format_var, value="all").pack(side=LEFT, padx=10)
        ttk.Radiobutton(format_frame, text="IT / Software Jobs", variable=self.format_var, value="InfTech").pack(side=LEFT, padx=10)

        # Save Location
        ttk.Label(self.root, text="Save Location:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
        location_frame = ttk.Frame(self.root)
        location_frame.pack(pady=5)
        ttk.Entry(location_frame, textvariable=self.location_var, width=40, font=("Helvetica", TEXT_SIZE)).pack(side=LEFT, padx=5)
        ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(side=LEFT, padx=5)

        # # File Name (Optional)
        # ttk.Label(self.root, text="File Name (Optional):", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
        # ttk.Entry(self.root, textvariable=self.filename_var, width=50, font=("Helvetica", TEXT_SIZE)).pack(pady=5)

        # # Download Button
        # ttk.Button(self.root, text="Download", command=self.download, bootstyle=SUCCESS).pack(pady=20)

        # # Progress Bar
        # self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, length=450)
        # self.progress_bar.pack(side=BOTTOM, pady=10)


    def apply_theme(self):
        selected_theme = self.theme_var.get()
        self.root.style.theme_use(selected_theme)


    def browse_location(self):
        folder_selected = filedialog.askdirectory(initialdir=self.location_var.get())
        if folder_selected:
            self.location_var.set(folder_selected)



#=-=-=-=-=-=-
# Functions
#=-=-=-=-=-=-
# --- Function to create a folder if it does not exist ---
def createFolderIfNotExists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

def GetIDUrl(jobNum):
    return f'{JOB_SPECIFIC_URL}{jobNum}'

# Helper function to get text safely - if it exists it will return otherwise it wont
def get_text_safe(lst, index):
    return lst[index].text if index < len(lst) else ""

# --- Function to write out to file as JSON---
def JsonAndCSVOutToFile(outgoingData, currentDatetime, filenamePrefix):
    with open(
        os.path.join(DEFAULT_FOLDER, f"{filenamePrefix}{currentDatetime}.json"), "a"
    ) as z:
        json.dump(outgoingData, z, indent=1)

    # Load JSON file
    with open(os.path.join(DEFAULT_FOLDER, f"{filenamePrefix}{currentDatetime}.json"), "r") as json_file:
        data = json.load(json_file)

    # Extract keys for CSV headers
    keys = data[0].keys()

    # Write CSV file
    with open(os.path.join(DEFAULT_FOLDER, f"{filenamePrefix}{currentDatetime}.csv"), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Wrote Out JSON and CSV data to: {DEFAULT_FOLDER}")


# --- Function to get category url ---
def sortUrlMaker(category):
	catUrlOut = f'https://statejobs.ny.gov/public/vacancyTable.cfm?searchResults=Yes&Keywords=&title=&JurisClassID=&AgID=&minDate=&maxDate=&cat{category}={category}&employmentType=&grade=&SalMin='
	return catUrlOut

# --- Function to display category url options ---
def catOptionsFunc():
	print("Here are your options: ")
	print("Clerical, Secretarial, Office Aide  =  1")
	print("Financial, Accounting, Auditing  =  2")
	print("Education, Teaching  =  3")
	print("Other Professional Careers =	 4")
	print("Skilled Craft, Apprenticeship, Maintenance =  5")
	print("Health Care, Human/Social Services  =  6")
	print("I.T. Engineering, Sciences =  7")
	print("Administrative or General Management  =  8")
	print("Enforcement or Protective Services  =  9")
	print("Legal  =  10")


# --- Function to print get all job url ---
def getJobs(inputUrl, outputFileName,jsonName):
    response = requests.get(inputUrl)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Printing Title of Webpage
    print(soup.title)

    index_val = 0

    # Finding even and odd numbered Jobs
    for a in soup.findAll(attrs={'class': ('even', 'odd')}):
        # index_val+=1 # uncomment this if you want to limite how many jobs returned, mainly for testing
    
        # if index_val > 9:
        #     break
        # else:
        

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find Job Title
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        name = a.find('a')
        # Writing out text file to see what is in results

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job number (used as key)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        number = a.find('td')
        # Writing out text file to see what is in job number

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job pay grade
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        grade = a.select("tr > td")[2]
        # Writing job pay grade object

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # When Posted
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        postedDate = a.select("tr > td")[3]
        # Writing posted day object

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job application due by
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        dueDate = a.select("tr > td")[4]
        # Writing out text file to see what due date is

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job agency
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        agency = a.select("tr > td")[5]
        # Writing out text file to see what is in agency

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Find job link
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Job_page = GetIDUrl(number.text)
        # using job id to get link

        print(f"JOB NUM: {number.text} - TITLE: {name.text}")
        print(f"    > LINK: {Job_page}")


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # NOW WE LOOK AT JOB PAGE:
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        response_LVL2 = requests.get(Job_page)
        soup_LVL2 = BeautifulSoup(response_LVL2.text, "html.parser")

        # Find all span tags
        all_rightCol = soup_LVL2.find_all(attrs={"class": ("rightCol")})

        job_data = {
            "job title": name.text,
            "job number": number.text,
            "job grade": grade.text,
            "job posted date": postedDate.text,
            "job due date": dueDate.text,
            "job agency": agency.text,
            "job link": Job_page,
            "job_Category": get_text_safe(all_rightCol, 6),
            "job_Bargaining_Unit": get_text_safe(all_rightCol, 8),
            "job_Pay_Range": get_text_safe(all_rightCol, 9),
            "job_Employment_Type": get_text_safe(all_rightCol, 10),
            "job_Appointment_Type": get_text_safe(all_rightCol, 11),
            "job_Travel": get_text_safe(all_rightCol, 13),
            "job_Workweek": get_text_safe(all_rightCol, 14),
            "job_Hours_Per_Week": get_text_safe(all_rightCol, 15),
            "job_Start_Time": get_text_safe(all_rightCol, 16),
            "job_End_Time": get_text_safe(all_rightCol, 17),
            "job_Flextime_Allowed": get_text_safe(all_rightCol, 18),
            "job_Mandatory_Overtime": get_text_safe(all_rightCol, 19),
            "job_Compressed_Workweek_Allowed": get_text_safe(all_rightCol, 20),
            "job_Telecommuting_Allowed": get_text_safe(all_rightCol, 21),
            "job_County": get_text_safe(all_rightCol, 22),
            "job_Street_Address": get_text_safe(all_rightCol, 23) + "\n" + get_text_safe(all_rightCol, 24),
            "job_City": get_text_safe(all_rightCol, 25),
            "job_State": get_text_safe(all_rightCol, 26),
            "job_Zip_Code": get_text_safe(all_rightCol, 27),
            "job_Duties_Description": get_text_safe(all_rightCol, 28),
            "job_Minimum_Qualifications": get_text_safe(all_rightCol, 29),
            "job_Additional_Comments": get_text_safe(all_rightCol, 30),
            "job_Apply_Name": get_text_safe(all_rightCol, 31),
            "job_Apply_Telephone": get_text_safe(all_rightCol, 32),
            "job_Apply_Fax": get_text_safe(all_rightCol, 33),
            "job_Apply_Email": get_text_safe(all_rightCol, 34),
            "job_Apply_Street_Addr": get_text_safe(all_rightCol, 35) + "\n" + get_text_safe(all_rightCol, 36),
            "job_Apply_City": get_text_safe(all_rightCol, 37),
            "job_Apply_State": get_text_safe(all_rightCol, 38),
            "job_Apply_Zip_Code": get_text_safe(all_rightCol, 39),
            "job_Note_On_Applying": get_text_safe(all_rightCol, 40)
        }

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Updating Dictionary
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        job_all_attributes.append(job_data)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Output to JSON and CSV
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-   
    # after done with loop, output all json data
    JsonAndCSVOutToFile(job_all_attributes,use_this_datetime,jsonName)



# --- Function to get specific job categories ---
def specificJobs(date):
    # If they want it sorted, give them the options and let them pic
    catOptionsFunc()

	# have them choose
    chooseCategory = input("\nWhich do you want?\n")
    categoryNums = ["1","2","3","4","5","6","7","8","9","10"]
    print(f"Your response: {chooseCategory}")

    #while(chooseCategory != 1 || != 2 || != 3 || != 4 || != 5 || != 6 || != 7 || != 8 || != 9 || != 10 )
    while chooseCategory not in categoryNums:
        catOptionsFunc()
        chooseCategory = input("\nThat was invalid, choose one of the above: ")
        print(f"Your response: {chooseCategory}")
    
    # create url and then submit
    searchCatUrl = sortUrlMaker(chooseCategory)

    print(searchCatUrl)

    # Determining output names NOT WORKING RIGHT
    outputNameCat = ''
    if (chooseCategory == "1"):
        outputNameCat = ' Clerical_Secretarial_Office Aide '
    if (chooseCategory == "2"):
        outputNameCat = ' Financial_Accounting_Auditing '
    if (chooseCategory == "3"):
        outputNameCat = ' Education_Teaching '
    if (chooseCategory == "4"):
        outputNameCat = ' Other Professional Careers '
    if (chooseCategory == "5"):
        outputNameCat = ' Skilled Craft_Apprenticeship_Maintenance '
    if (chooseCategory == "6"):
        outputNameCat = ' Health Care_Human Services_Social Services '
    if (chooseCategory == "7"):
        outputNameCat = ' IT_Engineering_Sciences '
    if (chooseCategory == "8"):
        outputNameCat = ' Administrative_General Management '
    if (chooseCategory == "9"):
        outputNameCat = ' Enforcement_Protective Services '
    if (chooseCategory == "10"):
        outputNameCat = ' Legal '

    print(f"Your Category name: {outputNameCat}")
    catNameAndDate = f"For {outputNameCat} on {date}"

    # getting data back
    getJobs(searchCatUrl,catNameAndDate,outputNameCat)

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

# --- Get All jobs:

# Grab current date & time from function & store in variable
use_this_datetime = defang_datetime()
createFolderIfNotExists(DEFAULT_FOLDER)

# # NYS JOBS Target URL
# URL = "https://statejobs.ny.gov/public/vacancyTable.cfm"
# JOB_SPECIFIC_URL = "https://statejobs.ny.gov/public/vacancyDetailsView.cfm?id="


# Get Even Designated Jobs CSV


if __name__ == "__main__":
    root = ttk.Window(themename=APP_THEME)
    app = WebScraperApp(root)
    root.mainloop()





getJobs(URL,use_this_datetime,"All Jobs")


# --- Specific categories:

# Do they want to sort?
wantSort = (input("Do you want to sort by type? (YES or NO)\n")).upper()
print(f"You answered: {wantSort}")

# Make sure it is valid
while ((wantSort != 'YES') and (wantSort != 'NO')):
    
    wantSort = (input("I'm sorry, answer either YES or NO...\n")).upper()   
    print(f"You answered: {wantSort}")

# if they answered 'YES', perform search
if (wantSort == 'YES'):
    specificJobs(use_this_datetime)
else:
    print("Skipping specific search...")

# --- Signaling End of Program:
print('#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
print("Scrapping Completed!")
print('#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
myLogo()
print('#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')



'''

# import os
# from tkinter import filedialog, StringVar, Text, END
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *

# # Settings
# APP_TITLE = "NYS Web Scraper"
# APP_SIZE = "900x750"
# APP_THEME = "vapor"
# TEXT_SIZE = 12

# # Filter presets
# FILTER_PRESETS = {
#     "All Jobs": [],
#     "IT Jobs": ["ITS2", "Information Technology Specialist", "Computer Programmer"],
#     "Office Jobs": ["Office Assistant", "HR Specialist", "Human Resources Technician", "Business Analyst"],
#     "Internships": ["Intern", "Internship"]
# }


# class WebScraperApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title(APP_TITLE)
#         self.root.geometry(APP_SIZE)
#         self.style = ttk.Style(theme=APP_THEME)

#         # Variables
#         self.selected_filter_type = StringVar(value="All Jobs")
#         self.filter_text = StringVar()
#         self.location_var = StringVar(value=os.path.expanduser("~/Downloads"))

#         self.build_ui()

#     def build_ui(self):
#         # Title Label
#         ttk.Label(self.root, text=APP_TITLE, font=("Helvetica", 20, "bold")).pack(pady=10)

#         # Filter Selection Dropdown
#         filter_frame = ttk.Frame(self.root)
#         filter_frame.pack(pady=10)
#         ttk.Label(filter_frame, text="Select Job Filter Type:", font=("Helvetica", TEXT_SIZE)).pack(side=LEFT, padx=5)
#         filter_dropdown = ttk.Combobox(filter_frame, values=list(FILTER_PRESETS.keys()),
#                                        textvariable=self.selected_filter_type, state="readonly", width=25)
#         filter_dropdown.pack(side=LEFT, padx=5)
#         filter_dropdown.bind("<<ComboboxSelected>>", self.update_filter_box)

#         # Editable Filter Textbox
#         ttk.Label(self.root, text="Editable Filters:", font=("Helvetica", TEXT_SIZE)).pack()
#         self.filter_box = Text(self.root, height=4, width=70, font=("Courier", 10))
#         self.filter_box.pack(pady=5)
#         self.update_filter_box()

#         # Save Location
#         location_frame = ttk.Frame(self.root)
#         location_frame.pack(pady=5)
#         ttk.Label(location_frame, text="Save to:", font=("Helvetica", TEXT_SIZE)).pack(side=LEFT)
#         ttk.Entry(location_frame, textvariable=self.location_var, width=50).pack(side=LEFT, padx=5)
#         ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(side=LEFT)

#         # Scrape Button
#         ttk.Button(self.root, text="Start Scraping", bootstyle=SUCCESS, command=self.start_scraping).pack(pady=10)

#         # Output / Log Window
#         ttk.Label(self.root, text="Output Logs:", font=("Helvetica", TEXT_SIZE)).pack()
#         self.output_box = Text(self.root, height=15, width=100, font=("Courier", 10), wrap="word")
#         self.output_box.pack(padx=10, pady=5)

#         # Save CSV Button
#         ttk.Button(self.root, text="Download CSV", bootstyle=PRIMARY, command=self.download_csv).pack(pady=10)

#     def update_filter_box(self, event=None):
#         """Update the filter textbox based on dropdown selection."""
#         selected = self.selected_filter_type.get()
#         filters = FILTER_PRESETS.get(selected, [])
#         self.filter_box.delete("1.0", END)
#         self.filter_box.insert(END, "\n".join(filters))

#     def browse_location(self):
#         folder = filedialog.askdirectory(initialdir=self.location_var.get())
#         if folder:
#             self.location_var.set(folder)

#     def log(self, message):
#         """Log to the output box."""
#         self.output_box.insert(END, message + "\n")
#         self.output_box.see(END)

#     def start_scraping(self):
#         self.log("Starting scrape...")
#         selected_filter = self.filter_box.get("1.0", END).strip().splitlines()
#         self.log(f"Filter terms: {selected_filter}")

#         # Call your job scrape logic here:
#         # get_all_jobs() -> filters -> scrape_details()
#         # For now, just mocking output
#         self.log("Scraping all jobs...")
#         self.log("Filtering jobs...")
#         self.log("Scraping filtered job details...")
#         self.log("Done!")

#     def download_csv(self):
#         """Let user save a dummy CSV file."""
#         path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             initialdir=self.location_var.get(),
#             filetypes=[("CSV Files", "*.csv")],
#             title="Save CSV file"
#         )
#         if path:
#             with open(path, "w") as f:
#                 f.write("Job Title,Agency,Location,Posted Date\n")
#                 f.write("Sample Job,Dept. of Labor,Albany,2025-04-05\n")
#             self.log(f"CSV saved to: {path}")


# # Run the app
# if __name__ == "__main__":
#     root = ttk.Window(themename=APP_THEME)
#     app = WebScraperApp(root)
#     root.mainloop()



# # # NOTE: You need to have ffmpeg downloaded and added to the path variable for this to work, get it here: https://ffmpeg.org/download.html#build-windows
# #     # You also need to 'pip install yt-dlp'
    
# #     #  If throwing errors update using this command: pip install --upgrade yt-dlp

# # # To convert this to exe, use the following:
# #     # https://stackoverflow.com/questions/5458048/how-can-i-make-a-python-script-standalone-executable-to-run-without-any-dependen
# #     # or
# #     # pyinstaller -F yourprogram.py


# # import os
# # from tkinter import filedialog, messagebox, StringVar, IntVar 
# # import ttkbootstrap as ttk
# # from ttkbootstrap.constants import *
# # # from yt_dlp import YoutubeDL

# # # Global text size
# # TEXT_SIZE = 12
# # APP_TITLE = "YOUTUBE DOWNLOADER"
# # APP_SIZE = "800x700"
# # APP_THEME="solar"

# # class WebScraperApp:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title(APP_TITLE)
# #         self.root.geometry(APP_SIZE)
        
# #         # Variables
# #         self.url_var = StringVar()
# #         self.format_var = StringVar(value="mp4")
# #         self.location_var = StringVar(value=os.path.expanduser("~/Downloads"))
# #         self.filename_var = StringVar()
# #         self.progress_var = IntVar(value=0)
# #         self.theme_var = StringVar(value=APP_THEME)

# #         # Build UI
# #         self.build_ui()

# #     def build_ui(self):
# #         # Theme Selector
# #         ttk.Label(self.root, text="Select Theme:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
# #         theme_frame = ttk.Frame(self.root)
# #         theme_frame.pack(pady=5)
# #         ttk.Combobox(theme_frame, values=ttk.Style().theme_names(), textvariable=self.theme_var, state="readonly", width=20).pack(side=LEFT, padx=5)
# #         ttk.Button(theme_frame, text="Apply Theme", command=self.apply_theme).pack(side=LEFT, padx=5)

# #         # URL Input
# #         ttk.Label(self.root, text="YouTube URL:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
# #         ttk.Entry(self.root, textvariable=self.url_var, width=50, font=("Helvetica", TEXT_SIZE)).pack(pady=5)

# #         # Format Selection (Video or Audio)
# #         ttk.Label(self.root, text="Format:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
# #         format_frame = ttk.Frame(self.root)
# #         format_frame.pack(pady=5)
# #         ttk.Radiobutton(format_frame, text="MP4 (Video)", variable=self.format_var, value="mp4").pack(side=LEFT, padx=10)
# #         ttk.Radiobutton(format_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3").pack(side=LEFT, padx=10)

# #         # Save Location
# #         ttk.Label(self.root, text="Save Location:", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
# #         location_frame = ttk.Frame(self.root)
# #         location_frame.pack(pady=5)
# #         ttk.Entry(location_frame, textvariable=self.location_var, width=40, font=("Helvetica", TEXT_SIZE)).pack(side=LEFT, padx=5)
# #         ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(side=LEFT, padx=5)

# #         # File Name (Optional)
# #         ttk.Label(self.root, text="File Name (Optional):", font=("Helvetica", TEXT_SIZE)).pack(pady=5)
# #         ttk.Entry(self.root, textvariable=self.filename_var, width=50, font=("Helvetica", TEXT_SIZE)).pack(pady=5)

# #         # Download Button
# #         ttk.Button(self.root, text="Download", command=self.download, bootstyle=SUCCESS).pack(pady=20)

# #         # Progress Bar
# #         self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, length=450)
# #         self.progress_bar.pack(side=BOTTOM, pady=10)

# #     def apply_theme(self):
# #         selected_theme = self.theme_var.get()
# #         self.root.style.theme_use(selected_theme)

# #     def browse_location(self):
# #         folder_selected = filedialog.askdirectory(initialdir=self.location_var.get())
# #         if folder_selected:
# #             self.location_var.set(folder_selected)

# #     def download(self):
# #         url = self.url_var.get().strip()
# #         file_format = self.format_var.get()
# #         location = self.location_var.get()
# #         filename = self.filename_var.get().strip()

# #         if not url:
# #             messagebox.showerror("Error", "Please enter a valid YouTube URL!")
# #             return

# #         self.progress_var.set(0)
# #         #self.download_with_yt_dlp(url, file_format, location, filename)

# #     # def download_with_yt_dlp(self, url, file_format, location, filename):
# #     #     try:
# #     #         ydl_opts = {
# #     #             'format': 'mp4' if file_format == 'mp4' else 'bestaudio/best',
# #     #             'outtmpl': os.path.join(location, f"{filename or '%(title)s'}.%(ext)s"),
# #     #             'progress_hooks': [self.ytdlp_progress_hook]
# #     #         }
# #     #         if file_format == "mp3":
# #     #             ydl_opts['postprocessors'] = [{
# #     #                 'key': 'FFmpegExtractAudio',
# #     #                 'preferredcodec': 'mp3'
# #     #             }]
            
# #     #         with YoutubeDL(ydl_opts) as ydl:
# #     #             ydl.download([url])
# #     #         messagebox.showinfo("Success", "Download completed successfully!")

# #     #         self.url_var.set("")
# #     #         self.filename_var.set("")
# #     #         self.progress_var.set(0)
# #     #     except Exception as e:
# #     #         messagebox.showerror("Error", f"An error occurred: {e}")

# #     # def ytdlp_progress_hook(self, d):
# #     #     if d['status'] == 'downloading':
# #     #         downloaded_bytes = d.get('downloaded_bytes', 0)
# #     #         total_bytes = d.get('total_bytes', 1)
# #     #         if total_bytes:
# #     #             progress = (downloaded_bytes / total_bytes) * 100
# #     #             self.progress_var.set(int(progress))
# #     #             self.root.update_idletasks()

# # if __name__ == "__main__":
# #     root = ttk.Window(themename=APP_THEME)
# #     app = WebScraperApp(root)
# #     root.mainloop()