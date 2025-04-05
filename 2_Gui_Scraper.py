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

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print(" ... Alright gpt helped a little with this one, yah got me!")

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
            myLogo()
        except Exception as e:
            self.log(f"Error saving CSV: {e}")


# Run it!
if __name__ == "__main__":
    root = ttk.Window(themename=APP_THEME)
    app = WebScraperApp(root)
    root.mainloop()