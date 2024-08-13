from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import json
import os
import pandas as pd 
from tqdm.auto import tqdm

ROOT = "https://codeforces.com"
SUBMISSIONS_PAGE = "/contest/{contest_id}/status/{problem_id}/page/{page_number}"
DATA_FILE = "../datasets/codeforces_solutions.csv"
PROGRESS_FILE = "cf_solutions_progress.json"


logging.basicConfig(filename='cf_solutions_scraping.log',  # Log to this file
                    filemode='a',  # Append to the log file if it exists
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp
                    level=logging.INFO)  # Log info and above

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    driver = webdriver.Chrome(options=options)
    return driver

def save_progress(last_problem_link, last_page, total_solutions, progress_file):
    progress = {
        "last_problem_link": last_problem_link,
        "last_page": last_page,
        "total_solutions": total_solutions
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f)


def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
            return progress.get("last_problem_link", ""), progress.get("last_page", 1), progress.get("total_solutions", 0)
    return "", 1, 0

def append_to_csv(data, data_file=DATA_FILE):
    df = pd.DataFrame(data)
    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)


last_problem_link, last_page, total_solutions = load_progress(PROGRESS_FILE)
df = pd.read_csv("../datasets/codeforces_problems.csv")
problem_links = df['problem_link'].tolist()

# Number of accepted submissions for each problem
NUM_SUBMISSIONS = 100
NUM_SUBMISSIONS_PER_PAGE = 50
total_solutions = 0

def scrape_codeforces_solutions(problem_link):
    driver = init_driver()

    global total_solutions
    _, _, _, _, _, contest_id, problem_id = problem_link.rstrip('/').split('/')
    page_number = last_page if problem_link == last_problem_link else 1
    cur_submissions_count_all_pages = 0
    i = 0

    last_page = False
    while cur_submissions_count_all_pages < NUM_SUBMISSIONS:
        try:
            print(page_number)
            SUBMISSION_PAGE_LINK = ROOT + SUBMISSIONS_PAGE.format(contest_id=contest_id, problem_id=problem_id, page_number=page_number)
            driver.get(SUBMISSION_PAGE_LINK)
            # Ensure the page has loaded
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "status-frame-datatable")))

            total_submissions_count_this_page = len(driver.find_elements(By.XPATH, "//table[@class='status-frame-datatable']/tbody/tr")) - 1

            print(total_submissions_count_this_page)
            if total_submissions_count_this_page < NUM_SUBMISSIONS_PER_PAGE:
                last_page = True

            # Process each submission by index
            while i < total_submissions_count_this_page:
                time.sleep(5) # to avoid rate limit 
                # Navigate to the submissions page for each iteration to avoid stale references
                driver.get(SUBMISSION_PAGE_LINK)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "status-frame-datatable")))

                # Locate the submission row dynamically by index to ensure it's always fresh
                submission = driver.find_element(By.XPATH, f"//table[@class='status-frame-datatable']/tbody/tr[{i+1}]")
                i += 1
                cells = submission.find_elements(By.TAG_NAME, 'td')

                # Not a valid cell
                if not cells or len(cells) < 6:
                    continue

                verdict = cells[5].text.strip()
                language = cells[4].text.strip()

                if verdict == "Accepted" and language.startswith("GNU"):
                    submission_id = submission.get_attribute('data-submission-id')
                    time_used = cells[6].text.strip()
                    memory_used = cells[7].text.strip()
                    
                    # Navigate to the detailed submission page
                    detailed_submission_link = f"{ROOT}/contest/{contest_id}/submission/{submission_id}"
                    driver.get(detailed_submission_link)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "program-source-text")))

                    source_code = driver.find_element(By.ID, "program-source-text").text

                    append_to_csv({
                            'id': [total_solutions],
                            'problem_link': [problem_link],
                            'submission_link': [detailed_submission_link],
                            'source_code': [source_code],
                            'language': [language],
                            'time': [time_used],
                            'memory': [memory_used]
                        })
                    
                    cur_submissions_count_all_pages += 1
                    total_solutions += 1

            if last_page:
                break
            
            save_progress(problem_link, page_number, total_solutions, PROGRESS_FILE)
            page_number += 1
            i = 0
        
        except Exception as e:
            logging.log("Fuck rate limit")
            logging.error(e) 
            time.sleep(5*60) # Sleep 5 minutes

    driver.quit()

for problem_link in tqdm(problem_links):
    scrape_codeforces_solutions(problem_link)
