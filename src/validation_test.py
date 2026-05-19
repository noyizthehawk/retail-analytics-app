"""
load sample data
print original columns
run validation
print validation result
show errors/warnings

"""

from .data_loader import load_sample_data
from .validation import validate_data_columns, validate_data_types
from .schema import normalize_column_names
from .cleaning import clean_data
import pandas as pd
TEST_MODE = True

df = load_sample_data()
print("Original columns:", df.columns)

df.columns = normalize_column_names(df.columns)

if TEST_MODE == True:
    cleaned_df = clean_data(df)

    print("First 5 rows cleaned data:")
    print(cleaned_df.head())

    print("Columns after cleaning:")
    for i, col in enumerate(cleaned_df.columns, start=1):
        print(f"{i}. {col}")
else:
    #validate cols
    column_result = validate_data_types(df)
    cleaned_df = clean_data(column_result)
    print("First 5 rows cleaned data:")
    print(cleaned_df.head())
    print("Columns after cleaning:")
    for i, col in enumerate(cleaned_df.columns, start=1):
        print(f"{i}. {col}")









