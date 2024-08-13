import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

PROGRESS_FILE = 'atcoder_problems_progress.txt'

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


def is_japanese(text):
    for ch in str(text):
        if u'\u3040' <= ch <= u'\u309F' or u'\u30A0' <= ch <= u'\u30FF' or u'\u4E00' <= ch <= u'\u9FBF':
            return True
    return False

# Function to append data to CSV


def append_to_csv(data, data_file):
    df = pd.DataFrame(data)
    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)


def AtcoderScraper():

    url = "https://atcoder.jp/contests/"

    problems_counter = 0
    contest_time = 1

    # read the contest_time from Progress_Saver.txt
    # if it doesn't exist, create it and set it to 0
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "w") as file:
            file.write("0")
    else:
        with open(PROGRESS_FILE, "r") as file:
            contest_time = int(file.read())

    # Check if the file exists, if not, create it
    file_path = "../datasets/atcoder_problems.csv"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")

    contest_type = ["abc", "arc", "agc"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # append letters to numbers
    for i in range(0, 9):
        numbers.append(chr(i + ord('a')))

    while contest_time < 500:
        for task in range(0, len(numbers)):
            for contest in contest_type:
                tasks = numbers[task]
                letter = convert_number_to_letter(tasks)
                problem_link = f"{url}{contest}{convert_to_base0(contest_time)}/tasks/{contest}{convert_to_base0(contest_time)}_{letter}?lang=en"

                response = requests.get(problem_link)
                if response.status_code != 200:
                    print(
                        f"Failed to fetch data for {problem_link}. Status Code: {response.status_code}")
                    continue

                print(f"Fetching data for {problem_link}")

                # Parse the page content
                soup = BeautifulSoup(response.content, 'html.parser')

                test_path = 'test.txt'
                if not os.path.exists(test_path):
                    with open(test_path, 'w') as file:
                        file.write("")

                time_limit = 0
                memory_limit = 0

                for p in range(0, len(soup.find_all('p'))):
                    if "sec" in soup.find_all('p')[p].text.strip():
                        time_limit = soup.find_all('p')[p].text.strip()
                        time_limit = time_limit[time_limit.find(
                            "sec") - 3:time_limit.find("sec")].strip()
                        break

                for p in range(0, len(soup.find_all('p'))):
                    if "MB" in soup.find_all('p')[p].text.strip():
                        memory_limit = soup.find_all('p')[p].text.strip()
                        memory_limit = memory_limit[memory_limit.find(
                            "MB") - 4:memory_limit.find("MB")].strip()
                        break

                try:
                    id = 0

                    """
                    The below loop is made because the structure of atcoder is as follows:
                    1- Japanese Full Tags  
                    2- English Full Tags
                    We detect the japanese by checking if any of the characters in the problem statement is japanese
                    and then after that we parse the english version of the problem statement
                    """

                    while True:
                        flag = 0
                        for j in soup.find_all('div', attrs={'class': 'part'})[id].text.strip():
                            if is_japanese(j):
                                flag = 1
                                break

                        if flag == 1:
                            id += 1
                        else:
                            break

                    problem_statement = soup.find_all(
                        'div', attrs={'class': 'part'})[id].text.strip()

                    id += 1
                    problem_constraints = soup.find_all(
                        'div', attrs={'class': 'part'})[id].text.strip()

                    id += 1
                    input_style = soup.find_all(
                        'div', attrs={'class': 'part'})[id].text.strip()

                    id += 1
                    output_style = soup.find_all(
                        'div', attrs={'class': 'part'})[id].text.strip()
                    inputs = []
                    outputs = []

                    id += 1
                    for i in range(id, len(soup.find_all('div', attrs={'class': 'part'}))):
                        if i % 2 == 0:
                            inputs.append(soup.find_all(
                                'div', attrs={'class': 'part'})[i].text.strip())
                        else:
                            outputs.append(soup.find_all(
                                'div', attrs={'class': 'part'})[i].text.strip())

                    print(f"Time Limit: {time_limit}")

                    print(f"Memory Limit: {memory_limit}")

                    with open(file_path, 'a') as file:
                        append_to_csv({
                            "id": [problems_counter],
                            "problem_link": [problem_link],
                            "time_limit": [time_limit],
                            "memory_limit": [memory_limit],
                            "problem_statement": [problem_statement],
                            "problem_constraints": [problem_constraints],
                            "input_style": [input_style],
                            "output_style": [output_style],
                            "inputs": [inputs],
                            "outputs": [outputs]
                        }, file_path)

                    problems_counter += 1

                except Exception as e:
                    print(f"An error occurred: {e}")
        # Progress Saving
        with open(PROGRESS_FILE, "w") as file:
            file.write(str(contest_time))

        contest_time += 1


AtcoderScraper()
