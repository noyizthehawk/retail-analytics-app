"overall cleaning"
import pandas as pd
from .schema import (
    OPTIONAL_NUMERIC_COLUMNS,
    OPTIONAL_TEXT_COLUMNS,
    REQUIRED_DATE_COLUMNS,
    REQUIRED_NUMERIC_COLUMNS,
    REQUIRED_TEXT_COLUMNS,
    normalize_column_names,
)



def _column_missing_or_empty(df, col: str) -> bool:
    """True if column is absent or has no usable values."""
    if col not in df.columns:
        return True
    return df[col].isna().all()


def convert_data_types(df):
    numeric_columns = REQUIRED_NUMERIC_COLUMNS + OPTIONAL_NUMERIC_COLUMNS
    date_columns = REQUIRED_DATE_COLUMNS
    text_columns = REQUIRED_TEXT_COLUMNS + OPTIONAL_TEXT_COLUMNS

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
def create_missing_deriv_columns(df):
    """sales = quantity * unit_price
order_month = month from order_date
order_year = year from order_date """ 
    if _column_missing_or_empty(df, "sales"):
        df["sales"] = df["quantity"] * df["unit_price"]
    if 'order_month' not in df.columns:
        df['order_month'] = df['order_date'].dt.month
    if 'order_year' not in df.columns:
        df['order_year'] = df['order_date'].dt.year

def handle_missing_values(df):
    "missing order id cell, remove row where order id is missing etc"


    columns_to_remove_rows = ['order_id', 'product_id', 'quantity', 'unit_price', 'order_date']
    for col in columns_to_remove_rows:
        if col not in df.columns:
            continue
        if df[col].isna().all():
            df = df.drop(col, axis=1)
        else:
            #check the column for missing values
            df = df[df[col].notna()]

    if 'customer_id' in df.columns:
        df['customer_id'] = df['customer_id'].fillna('unknown')

    if 'product_name' in df.columns:
        df['product_name'] = df['product_name'].fillna('unknown')

    if 'country' in df.columns:
        df['country'] = df['country'].fillna('unknown')

    if 'region' in df.columns:
        df['region'] = df['region'].fillna('unknown')

    return df


def remove_duplicate_rows(df):
    return df.drop_duplicates()


def handle_bad_num_vals(df):
    if 'quantity' in df.columns:
        df = df[df['quantity'] > 0]
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] > 0]
    if 'sales' in df.columns:
        df = df[df['sales'] > 0]
    return df
def analysis_friendly(df):
    "make the data more analysis friendly"
    if 'order_month' not in df.columns:
        df['order_month'] = df['order_date'].dt.month
    if 'order_day' not in df.columns:
        df['order_day'] = df['order_date'].dt.day
    if 'order_year' not in df.columns:
        df['order_year'] = df['order_date'].dt.year
    if _column_missing_or_empty(df, "sales"):
        df["sales"] = df["quantity"] * df["unit_price"]

    return df
def clean_data(df):
    df.columns = normalize_column_names(df.columns)
    convert_data_types(df)
    create_missing_deriv_columns(df)
    df = handle_missing_values(df)
    df = remove_duplicate_rows(df)

    if _column_missing_or_empty(df, "unit_price"):
        if _column_missing_or_empty(df, "sales") or _column_missing_or_empty(df, "quantity"):
            raise ValueError("Cannot estimate unit_price without sales and quantity.")
        if (df["quantity"] == 0).any():
            raise ValueError("Cannot estimate unit_price because some quantity values are zero.")
        df["unit_price"] = df["sales"] / df["quantity"]
    elif df["unit_price"].isna().any():
        mask = df["unit_price"].isna()
        df.loc[mask, "unit_price"] = df.loc[mask, "sales"] / df.loc[mask, "quantity"]

    df = handle_bad_num_vals(df)
    return analysis_friendly(df)


#test the function
if __name__ == "__main__":
    from .data_loader import load_sample_data

    df = load_sample_data()
     #rows before and after cleaning
    print(f"Rows before cleaning: {len(df)}")
     # print all the cols before and after cleaning
    print(f"Columns before cleaning: {df.columns}")
    
    clean_data(df)
   
    print(f"Rows after cleaning: {len(clean_data(df))}")
    #removed duplicate rows
    print(f"Duplicate rows removed: {len(df) - len(clean_data(df))}")
    #missing customer id filled
    print(f"Missing customer id filled: {clean_data(df)['customer_id'].isna().sum()}")
    #missing product name filled
    print(f"Missing product name filled: {clean_data(df)['product_name'].isna().sum()}")

   
    print(f"Columns after cleaning: {clean_data(df).columns}")
    

   
    #missing city filled

        