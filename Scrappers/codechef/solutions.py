import os 
import pandas as pd 

df = pd.DataFrame(columns=['problem_link', 'solution'])
ROOT_FILE_PATH = '../description2code/codechef'
ROOT_WEB_PATH = "https://www.codechef.com/problems/"

for dirpath, dirnames, filenames in os.walk(ROOT_FILE_PATH):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)   
        sol_dir = file_path.split("/")[-2]
        if sol_dir != "solutions_c++":
            continue
        
        try:
            problem_name = file_path.split("/")[-3]
            problem_link = ROOT_WEB_PATH + problem_name
            solution = open(file_path).read()

            new_row = {
                'problem_link': problem_link,
                'solution': solution
            }

            df.loc[len(df)] = new_row 
        except Exception as e:
            print(e)
    
df.to_csv('../datasets/codechef_solutions.csv')