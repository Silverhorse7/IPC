# %%
from bs4 import BeautifulSoup
import logging
import requests
import re
import pandas as pd
from tqdm.auto import tqdm
import os
import json

# %%
ROOT = "https://codeforces.com"
PAGE = ROOT + "/problemset/page/"
DATA_FILE = "../datasets/codeforces_problems.csv"
PROGRESS_FILE = "cf_problems_progress.json"

# %%
# Setup logging
logging.basicConfig(filename='cf_problems_scraping.log',  # Log to this file
                    filemode='a',  # Append to the log file if it exists
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp
                    level=logging.INFO)  # Log info and above
# %%
# Function to save progress
def save_progress(progress, progress_file):
    with open(progress_file, 'w') as f:
        json.dump(progress, f)

# Function to load progress
def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {"last_page": 1, "last_saved_index": -1}

# Function to append data to CSV
def append_to_csv(data, data_file):
    df = pd.DataFrame(data)
    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)

# %%
progress = load_progress(PROGRESS_FILE)
last_saved_page = progress["last_page"]
last_saved_index = progress["last_saved_index"]
print(last_saved_page)
print(last_saved_index)

# %%
NUM_PAGES = 93
problems_counter = 0

# %%
for page_index in tqdm(range(last_saved_page, NUM_PAGES + 1)):
    webpage = BeautifulSoup(requests.get(PAGE + str(page_index)).text, "lxml")
    table = webpage.find("table", class_="problems")
    table_rows = table.find_all("tr")[1:]
    for i, row in enumerate(table_rows, start=1):  
        if page_index == last_saved_page and i <= last_saved_index:
            continue

        try: 
            problem_link_cell = row.find_all("td")[0]
            a_tag = problem_link_cell.find("a")
            problem_link = ROOT + a_tag["href"]

            # Get tags
            tag_cell = row.find_all("td")[1]
            tags = [tag.text.strip() for tag in tag_cell.find_all("a")]
            tags = tags[1:]

            # Skip April fools contests
            if "*special problem" in tags:
                continue

            # Get difficulty
            difficulty_cell = row.find("span", class_="ProblemRating")
            difficulty = (difficulty_cell.text if difficulty_cell else "N/A")

            content = BeautifulSoup(requests.get(problem_link).text, "lxml")
            cp = content.find("div", class_="problem-statement")
            div_10 = cp.find_all("div")[10]
            problem_text = div_10.text.replace('^{\\dagger}', '').replace('$', '').replace("\\ldots", '...').replace("\\le", "<=").replace("\\ge", ">=").replace("\\times", '*')\
                    .replace("\\dots", '...').replace("\xa0", ' ').replace(" \\ne ", '!=').replace("\\dagger", '')
            input_text = cp.find("div", class_="input").find("pre").text.strip()
            output_text = cp.find("div", class_="output").find("pre").text.strip()
        
            time_limit = re.search(r'(\d+)\s*seconds?', cp.find("div", class_="time-limit").text).group(1)
            memory_limit = re.search(r'(\d+)\s*me(ga|bi)bytes?', cp.find("div", class_="memory-limit").text).group(1)

            append_to_csv({
                    "id": [problems_counter],
                    "problem_link": [problem_link],
                    "time_limit": [time_limit],
                    "memory_limit": [memory_limit],
                    "problem_text": [problem_text],
                    "sample_input": [input_text],
                    "sample_output": [output_text],
                    "tags": [tags],
                    "difficulty": [difficulty]
                }, DATA_FILE)
            problems_counter += 1
            
        except Exception as e:
            logging.error(f"Error processing link {problem_link}: {e}")

        save_progress({"last_page": page_index, "last_saved_index": i}, PROGRESS_FILE)     
