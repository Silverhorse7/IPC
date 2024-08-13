import os 
import pandas as pd 

df = pd.DataFrame(columns=['problem_name', 'problem_statement'])
ROOT_FILE_PATH = '../description2code/hackerearth/problems_normal'

for dirpath, dirnames, filenames in os.walk(ROOT_FILE_PATH):
    for filename in filenames:
        if filename != "description.txt":
            continue

        file_path = os.path.join(dirpath, filename)   
        problem_statement = open(file_path).read()             
        problem_name = file_path.split("/")[-3]

        new_row = {
            'problem_name': problem_name,
            'problem_statement': problem_statement
        }

        df.loc[len(df)] = new_row        
    
df.to_csv('../datasets/hackerearth_problems.csv')