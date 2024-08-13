import os 
import pandas as pd 

df = pd.DataFrame(columns=['problem_link', 'problem_statement', 'difficulty'])
ROOT_FILE_PATH = '../description2code/codechef'
ROOT_WEB_PATH = "https://www.codechef.com/problems/"

for dirpath, dirnames, filenames in os.walk(ROOT_FILE_PATH):
    for filename in filenames:
        if filename != "description.txt":
            continue

        file_path = os.path.join(dirpath, filename)   
        problem_statement = open(file_path).read()             
        problem_name = file_path.split("/")[-3]
        difficulty = file_path.split("/")[-4]

        problem_link = ROOT_WEB_PATH + problem_name

        new_row = {
            'problem_link': problem_link,
            'problem_statement': problem_statement,
            'difficulty': difficulty
        }

        df.loc[len(df)] = new_row        
    
df.to_csv('../datasets/codechef_problems.csv')