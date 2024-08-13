from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO
import fitz  # PyMuPDF
import json
import os

def append_to_csv(data, data_file):
    df = pd.DataFrame(data)
    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)

def convert_pdf_to_text(pdf_path, timeout=10):
    try:
        response = requests.get(pdf_path, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to load: {pdf_path}")
        return None

    # Open the PDF from the downloaded content
    with fitz.open("pdf", BytesIO(response.content)) as pdf_document:
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

    return text

def extract_problem_text_sample_input_output(problem_content):
    def read_section(start_index, end_keyword):
        section = ""
        index = start_index
        lines = problem_content.splitlines()

        while index < len(lines):
            line = lines[index]

            if "Universidad de Valladolid OJ" in line:
                index += 2
                continue

            if end_keyword is not None and end_keyword in line:
                index += 1
                break

            section += line + "\n"
            index += 1

        return section.strip(), index

    problem_text, index = read_section(2, "Sample Input")
    sample_input, index = read_section(index, "Sample Output")
    sample_output, _ = read_section(index, None)

    return problem_text, sample_input, sample_output

def get_problems_id(a_tags):
    problems_id = []
    for a_tag in a_tags:
        if "pdf" in a_tag["href"] and not a_tag["href"].startswith("p"):
            problem_id = a_tag["href"].split(".")[0]
            problems_id.append(problem_id)
    return problems_id

def get_problem_rtl(problem_id):
    api = f"https://uhunt.onlinejudge.org/api/p/id/{problem_id}"
    response = requests.get(api)
    response.raise_for_status()
    data = response.json()
    # Convert runtime limit from ms to s
    time_limit = data["rtl"] / 1000
    return time_limit

def save_progress(volume, last_problem_id, progress_file):
    progress = {"last_volume": volume, "last_problem_id": last_problem_id}
    with open(progress_file, 'w') as f:
        json.dump(progress, f)

def main():
    DATA_FILE = "../datasets/uva_problems.csv"
    PROGRESS_FILE = "uva_problems_progress.json"
    ROOT = "https://onlinejudge.org/external/"
    NUM_VOLUMES = 17

    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    os.chdir(current_directory)


    for volume in range(1, NUM_VOLUMES + 1):
        page = requests.get(ROOT + str(volume)).text        
        soup = BeautifulSoup(page, "lxml")
        a_tags = soup.find_all("a")
        problems_id = get_problems_id(a_tags)

        for problem_id in problems_id:
            problem_link = ROOT + str(volume) + "/" + problem_id + ".pdf"
            problem_rtl = get_problem_rtl(problem_id)
            problem_content = convert_pdf_to_text(problem_link)
            problem_text, sample_input, sample_output = extract_problem_text_sample_input_output(problem_content)

            append_to_csv({
                        "problem_link": [problem_link],
                        "time_limit": [problem_rtl], 
                        "memory_limit": "N/A",
                        "problem_text": [problem_text],
                        "sample_input": [sample_input],
                        "sample_output": [sample_output],
                        "tags": "N/A",
                        "difficulty": "N/A"
                }, DATA_FILE)

            save_progress(volume, problem_id, PROGRESS_FILE)

if __name__ == "__main__":
    main()