import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
import os
import json
import datetime

NUM_SOLUTIONS = 1000
FILE_PATH = "../datasets/atcoder_solutions.csv"
PROGRESS_FILE = 'atcoder_solutions_progress.txt'


def convert_to_base0(x):
    if x < 10:
        return "00" + str(x)
    elif x < 100:
        return "0" + str(x)
    else:
        return str(x)


def convert_number_to_letter(x):
    # if it's already a letter, return it
    if isinstance(x, str) and 'a' <= x <= 'z':
        return x
    # if it's a number, convert it to a letter
    elif isinstance(x, int) and 0 <= x <= 25:
        return chr(x + ord('0'))
    else:
        return None


def append_to_csv(data, data_file):

    df = pd.DataFrame(data)

    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', header=True, index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)


def save_progress(last_problem_id, total_solutions, contest_page, progress_file=PROGRESS_FILE):
    progress = {
        "last_problem_id": last_problem_id,
        "total_solutions": total_solutions,
        "contest_page": contest_page
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f)


def load_progress(progress_file=PROGRESS_FILE):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
            return progress.get("last_problem_id", 0), progress.get("total_solutions", 0), progress.get("contest_page", 1)
    return 0, 0, 1


def translate_problem_link_to_page(problem_link):
    # problem link : https://atcoder.jp/contests/agc001/tasks/agc001_b?lang=en
    # page : https://atcoder.jp/contests/agc001/submissions?f.Task=agc001_b&f.LanguageName=C%2B%2B&f.Status=AC&f.User=
    # print(problem_link)
    # exit()
    page = "https://atcoder.jp/contests/" + problem_link.split("/")[4] + "/submissions?f.Task=" + problem_link.split("/")[
        6] + "&f.LanguageName=C%2B%2B&f.Status=AC&f.User="

    # erase substring ?lang=en
    page = page.replace("?lang=en", "")

    return page

def fuck_rate_limit(page):
    print("FUCK RATE LIMIT")
    print(page)
    print(datetime.datetime.now())
    time.sleep(5*60)

def problems_scraper():

    session = requests.Session()

    # put your revel session
    session.cookies.update({
        'REVEL_SESSION': ''
    })

    def code_extraction_from_link(submission_url):
        sub_soup = BeautifulSoup(session.get(submission_url).content, 'lxml')
        submission_code = sub_soup.find('pre', attrs={"id": "submission-code"})
        if submission_code is None:
            return None
        return submission_code.text

    df = pd.read_csv("../datasets/atcoder_problems.csv")

    # print columns in df
    # print(df.columns)

    # exit()

    problem_links = df['problem_link'].values
    problem_links = df['problem_link'].astype(str).values

    # print(problem_links[0:10])

    problem_id, total_solutions, contest_page = load_progress()

    while (problem_id < len(problem_links)):
        link = problem_links[problem_id]
        page_basic = translate_problem_link_to_page(link)
        cnt = 0

        while cnt < NUM_SOLUTIONS:

            page = page_basic + "&f.User=&page=" + str(contest_page)

            # print(page)

            response = session.get(page)

            if response.status_code == 403:
                fuck_rate_limit(page)
                continue
            if response.status_code != 200:
                print(response.status_code)
                print("All solutions fetched for problem " + str(problem_id))
                break

            print(f"Fetching data for {page}")

            soup = BeautifulSoup(response.content, 'html.parser')

            # get all rows
            rows = soup.find_all("tr")

            flag = 0

            # debug purposes
            # print("Length of rows: " + str(len(rows)))

            if len(rows) == 0:
                break
            for row in rows:
                if flag == 0:
                    flag += 1
                    continue
                
                hrefs = row.find_all("a")

                problem_link, solution_link = "", ""

                for href in hrefs:
                    if "tasks" in href["href"]:
                        problem_link = href["href"]
                    elif "submissions" in href["href"]:
                        solution_link = href["href"]

                problem_link = "https://atcoder.jp" + problem_link + "?lang=en"
                solution_link = "https://atcoder.jp" + solution_link

                # # debug purposes
                # print("__________________________")
                # print(solution_link)
                # print(problem_link)
                # print(response_code.status_code)

                code = code_extraction_from_link(solution_link)

                if code is None:
                    fuck_rate_limit(page)
                    continue

                append_to_csv({
                    "id": [total_solutions],
                    "problem_link": [problem_link],
                    "solution_link": [solution_link],
                    "solution_code": [code]
                }, FILE_PATH)
                    
                cnt += 1
                total_solutions += 1
                save_progress(problem_id, total_solutions, contest_page)
                
                # print("Total solutions: " + str(total_solutions))

                if cnt > NUM_SOLUTIONS:
                    break

            contest_page += 1

        problem_id += 1
        contest_page = 1
        save_progress(problem_id, total_solutions, contest_page)


problems_scraper()
