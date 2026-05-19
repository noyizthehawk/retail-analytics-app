import pandas as pd
'''
This file contains the data loading functions for the retail analytics app.
It provides functions to load data from a csv file, a sample data file, and get the data shape.
'''

#load data from csv file
def load_data(file_path):
    if file_path is None:
        raise ValueError("No uploaded file provided.")
    df = pd.read_csv(file_path, encoding="latin-1")
    return df

def load_sample_data():
    df = pd.read_csv("data/online_retail_II.csv", encoding="latin-1")
    return df

# get data shape to get columns and row counts of a data frame as a dictionary
def get_data_shape(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }
