import os
import pandas as pd

def clean(directory):    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path, low_memory=False)
                if 'id' in df.columns:
                    df.drop(columns=['id'], inplace=True)
                df = df.dropna(axis=1, how='any')
                df = df.dropna()
                # df['id'] = range(1, len(df) + 1)
                df.to_csv(file_path, index=True)

dataset_directory = 'datasets'
clean(dataset_directory)