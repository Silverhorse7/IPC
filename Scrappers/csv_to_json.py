import os
import json
import pandas as pd
import time
import os

def convert_csv_to_json(data_file, json_file):
    # create a dataframe from the csv file
    df = pd.read_csv(data_file)
    # convert the dataframe to a dictionary
    data = df.to_dict(orient='records')
    # create and save the json file
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
# convert the csv file to a json file

files = ['atcoder_problems.csv', 'codeforces_problems.csv', 'leetcode_problems.csv', 'cses_problems.csv', 'uva_problems.csv', 'yosupo_problems.csv']

for file in files:
    data_file = f'./datasets/{file}'
    json_file = f'./datasets/{file.split(".")[0]}.json'
    convert_csv_to_json(data_file, json_file)
    print(f'Converted {data_file} to {json_file}')
    time.sleep(1)
    
