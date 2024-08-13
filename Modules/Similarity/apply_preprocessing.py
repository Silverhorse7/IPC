from preprocessing import *
import pandas as pd

def apply_preprocessing():
    # Switch to the directory where the script is loca
    # 
    # ted
    os.chdir(os.path.dirname(__file__))

    df = pd.read_csv('IPC_Datasets/combined_solutions_v1.csv')

    # df = df.head(10)
    
    # Apply batch processing to the dataset
    preprocessed_data, tokenized_data = preprocess_dataset(df)

    # Create a new DataFrame with preprocessed solutions
    preprocessed_df = pd.DataFrame({
        'preprocessed_solution': preprocessed_data,
        'tokenized_solution': tokenized_data,
    })

    # Merge preprocessed solutions DataFrame with the original DataFrame
    df = pd.concat([df, preprocessed_df], axis=1)

    # Save the preprocessed dataset
    df.to_csv('IPC_Datasets/preprocessed_solutions_v1.csv', index=False)
    print('Preprocessed dataset saved successfully!')

apply_preprocessing()