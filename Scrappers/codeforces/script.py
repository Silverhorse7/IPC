import pandas as pd

file_path = '../datasets/codeforces_problems.csv'

df = pd.read_csv(file_path)

rows_with_nan_in_difficulty = df[df['difficulty'].isna()]
print(rows_with_nan_in_difficulty)

nan_count = df['difficulty'].isna().sum()
print(f"Number of rows with NaN in 'difficulty' column: {nan_count}")

df = df.dropna(subset=['difficulty'])
df['difficulty'] = df['difficulty'].astype(int)

df['id'] = range(0, len(df))

df.to_csv(file_path, index=False)

print(f"Updated CSV file '{file_path}' with correct 'id' enumeration starting from 0.")
