# This file divides the csv data file into 2 parts: train and test

import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(data_path, save_path, test_size=0.2, date=""):
    # date should be start with _
    df = pd.read_csv(data_path)
    train, test = train_test_split(df, test_size=test_size, random_state=42)
    
    train.to_csv(os.path.join(save_path, f"train{date}.csv"), index=False)
    test.to_csv(os.path.join(save_path, f"test{date}.csv"), index=False)
    
if __name__ == '__main__':
    data_path = 'data/training_dataset_261203.csv'
    save_path = 'data'
    split_dataset(data_path, save_path, date="_261203")