import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# topic,problem_link,statistics,problem_name,problem_statement,input,output,constraints,example


def append_to_csv(data, data_file):

    df = pd.DataFrame(data)

    if not os.path.isfile(data_file):
        df.to_csv(data_file, mode='w', index=False)
    else:
        df.to_csv(data_file, mode='a', header=False, index=False)


def problem__info(problem_link):
    r = requests.get(problem_link)

    # get the content of the page
    html = r.content

    """ 
        structure: 
        <div class="md">
        problem statement
        <h1 id="input">Input</h1>
        input 
        <h1 id="output">Output</h1>
        output
        <h1 id="constraints">Constraints</h1>
        constraints
        <h1 id="example">Example</h1>
        example
    """

    soup = BeautifulSoup(html, 'html.parser')
    md = soup.find('div', class_='md')

    # get all the paragraphs that's before <h1 id="input">
    problem_statement = ''
    for p in md.find_all('p'):
        if p.find('h1', id='input'):
            break
        problem_statement += p.text

    # get the input
    input = md.find('h1', id='input').find_next('p').text

    # get the output
    output = ''
    if (md.find('h1', id='output') != None):
        if (md.find('h1', id='output').find_next('p') != None):
            output = md.find('h1', id='output').find_next('p').text

    # get the constraints
    constraints = ''

    if (md.find('h1', id='constraints') != None):
        if (md.find('h1', id='constraints').find_next('ul') != None):
            constraints = md.find('h1', id='constraints').find_next('ul').text
        else:
            constraints = md.find('h1', id='constraints').find_next('p').text

    # get the example

    options = ['example', 'example1', 'example2', 'example3', 'example4',
               'example5', 'example6', 'example7', 'example8', 'example9']

    example = ''

    for option in options:
        if md.find('h1', id=option):
            example += md.find('h1', id=option).find_next('p').text
            example += md.find('h1', id=option).find_next('pre').text
            example += md.find('h1',
                               id=option).find_next('pre').find_next('p').text
            example += md.find('h1', id=option).find_next(
                'pre').find_next('p').find_next('pre').text
            example += "\n\n"

    # print(example)

    # print("Problem Statement: ", problem_statement)
    # print("Input: ", input)
    # print("Output: ", output)
    # print("Constraints: ", constraints)
    # print("Example: ", example)

    return [problem_statement, input, output, constraints, example]


# problem__info('https://cses.fi/problemset/task/1070')
# exit()


# File to store the data
file_path = 'cses_problems.csv'


# URL of the page
url = 'https://cses.fi/problemset/'

# Send a GET request to the server and store the response
response = requests.get(url)

if response.status_code != 200:
    print('Failed to get the page:', response.status_code)
    exit()

# get the content of the page
html = response.content

# get all the classes with ul class="task-list"
soup = BeautifulSoup(html, 'html.parser')
task_list = soup.find_all('ul', class_='task-list')

# get all the problems
link, problem_name, statistics, topic = [], [], [], []

for task in task_list:
    for li in task.find_all('li'):
        a = li.find('a')
        # if link contains 'task'
        if a['href'].find('task') != -1:
            link.append(a['href'])
            problem_name.append(a.text)
            statistics.append(li.find('span').text)

            print(link)


# get the topics
# topics is within <h2> tag
h2 = soup.find_all('h2')
for h in h2:
    topic.append(h.text)

# remove the first element
topic.pop(0)

conditions = ['Distinct Numbers', 'Dice Combinations', 'Counting Rooms', 'Static Range Sum Queries', 'Subordinates',
              'Josephus Queries', 'Word Combinations', 'Point Location Test', 'Meet in the Middle', 'Shortest Subsequence', 'a']


for condition in conditions:
    while len(problem_name) > 0 and problem_name[0] != condition:

        problem_link = 'https://cses.fi' + link[0]

        print(problem_link)

        problem_info = problem__info(problem_link)

        print("Successfully scraped: ", problem_name[0])

        with open(file_path, 'a') as file:
            append_to_csv({
                "topic": [topic[0]],
                "problem_link": [link[0]],
                "problem_name": [problem_name[0]],
                "statistics": [statistics[0]],
                "problem_statement": [problem_info[0]],
                "input": [problem_info[1]],
                "output": [problem_info[2]],
                "constraints": [problem_info[3]],
                "example": [problem_info[4]]
            }, file_path)

        link.pop(0)
        problem_name.pop(0)
        statistics.pop(0)

    if len(topic) > 0:
        topic.pop(0)
