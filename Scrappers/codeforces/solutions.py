from bs4 import BeautifulSoup
import requests
from tqdm.auto import tqdm
import time
import pandas as pd
import os 
import logging
import json 

ROOT = "https://codeforces.com"
SUBMISSIONS_PAGE = "/contest/{contest_id}/status/{problem_id}/page/{page_number}"
DATA_FILE = "../datasets/codeforces_solutions.csv"
PROGRESS_FILE = "cf_solutions_progress.json"

# %%
# Setup logging
logging.basicConfig(filename='cf_solutions_scraping.log',  # Log to this file
                    filemode='a',  # Append to the log file if it exists
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp
                    level=logging.INFO)  # Log info and above
# %%
# Function to save progress
def save_progress(last_problem_link, last_page, total_solutions, progress_file):
    progress = {
        "last_problem_link": last_problem_link,
        "last_page": last_page,
        "total_solutions": total_solutions
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f)


# Function to load progress
def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
            return progress.get("last_problem_link", ""), progress.get("last_page", 1), progress.get("total_solutions", 0)
    return "", 1, 0


# Function to append data to CSV
def append_to_csv(data, data_file=DATA_FILE):
    df = pd.DataFrame(data)
    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)

# %%
last_problem_link, last_page, total_solutions = load_progress(PROGRESS_FILE)
# Step 1: Load problem links from CSV
df = pd.read_csv("../datasets/codeforces_problems.csv")
problem_links = df['problem_link'].tolist()

# Number of accepted submissions for each problem
NUM_SUBMISSIONS = 100

for link in tqdm(problem_links):
    # Extract contest_id and problem_id from the problem link
    _, _, _, _, _, contest_id, problem_id = link.rstrip('/').split('/')
    
    page_number = last_page if link == last_problem_link else 1
    submission_count = 0

    while submission_count < NUM_SUBMISSIONS:
        try:
            submission_link = ROOT + SUBMISSIONS_PAGE.format(contest_id=contest_id, problem_id=problem_id, page_number=page_number)
            response = requests.get(submission_link)

            if response.status_code != 200:
                raise Exception(f"Fuck rate limit, status code is {response.status_code}")

            page = BeautifulSoup(response.text, "lxml")
            submissions_table = page.find("table", class_="status-frame-datatable")
            submissions = submissions_table.find_all("tr")[1:]

            for sub in submissions:
                cells = sub.find_all('td')
                if not cells:
                    continue
                
                verdict = cells[5].text.strip()
                lang = cells[4].text.strip()
                
                if verdict == "Accepted" and lang.startswith("GNU"):
                    submission_id = sub['data-submission-id']
                    time_used = cells[6].text.strip()
                    memory_used = cells[7].text.strip()
                    
                    detailed_submission_link = f"{ROOT}/contest/{contest_id}/submission/{submission_id}"
                    detailed_page = BeautifulSoup(requests.get(detailed_submission_link).text, "lxml")
                    source_code_element = detailed_page.find("pre", id="program-source-text")
                    if source_code_element:
                        source_code = source_code_element.text.strip()
                        append_to_csv({
                            'id': [total_solutions],
                            'problem_link': [link],
                            'submission_link': [detailed_submission_link],
                            'source_code': [source_code],
                            'language': [lang],
                            'time': [time_used],
                            'memory': [memory_used]
                        })
                        submission_count += 1
                        total_solutions += 1
                        time.sleep(1) # to avoid rate limit


                save_progress(link, page_number, total_solutions, PROGRESS_FILE)
                page_number += 1
                
        except Exception as e:
            logging.error(e) 
            time.sleep(60) # to avoid rate limit
            pass