# This file divides the csv data file into 2 parts: train and test

import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(df: pd.DataFrame, save_path, test_split_rate=0.2, postfix=""):
    # date should be start with _
    train, test = train_test_split(df, test_size=test_split_rate, random_state=42)
    
    train_path = os.path.join(save_path, f"train{postfix}.csv")
    train.to_csv(train_path, index=False)
    
    test_path = os.path.join(save_path, f"test{postfix}.csv")
    test.to_csv(test_path, index=False)

    print("Train data is saved at", train_path)
    print("Test data is saved at", test_path)
    return train_path, test_path
    
if __name__ == '__main__':
    data_path = 'data/training_dataset_261203.csv'
    save_path = 'data'
    split_dataset(data_path, save_path, postfix="_261203")