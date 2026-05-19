"overall cleaning"
import pandas as pd
from validation import validate_data_columns, validate_data_types
from schema import(
    REQUIRED_NUMERIC_COLUMNS,OPTIONAL_NUMERIC_COLUMNS,
    REQUIRED_DATE_COLUMNS,
    REQUIRED_TEXT_COLUMNS,OPTIONAL_TEXT_COLUMNS,
    normalize_column_names
)
from data_loader import load_sample_data



#function:
def convert_data_types(df):
    numeric_columns = REQUIRED_NUMERIC_COLUMNS + OPTIONAL_NUMERIC_COLUMNS
    date_columns = REQUIRED_DATE_COLUMNS
    text_columns = REQUIRED_TEXT_COLUMNS + OPTIONAL_TEXT_COLUMNS
    #clean numeric columns
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = None #if column is not in the dataframe, set it to None
    #clean date columns
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        else:
            df[col] = None #if column is not in the dataframe, set it to None
    #clean text columns
    for col in text_columns:
        if col in df.columns:
           df[col] = pd.to_datetime(df['order_date'])
        else:
            df[col] = None #if column is not in the dataframe, set it to None
def create_missing_deriv_columns(df):
    """sales = quantity * unit_price
order_month = month from order_date
order_year = year from order_date """ 
    if 'sales' not in df.columns:
        df['sales'] = df['quantity'] * df['unit_price']
    if 'order_month' not in df.columns:
        df['order_month'] = df['order_date'].dt.month
    if 'order_year' not in df.columns:
        df['order_year'] = df['order_date'].dt.year

def handle_missing_values(df):
    "missing order id cell, remove row where order id is missing etc"


    columns_to_remove_rows = ['order_id', 'product_id', 'quantity', 'unit_price','order_date']
    for col in columns_to_remove_rows:
        #check the full column for missing values
        if df[col].isna().all():
            df = df.drop(col, axis=1)
        else:
            #check the column for missing values
            df = df[df[col].notna()]
    #keep customer id if present but mark as "uknown"
    if 'customer_id' in df.columns:
        df['customer_id'] = df['customer_id'].fillna('unknown')

    if 'product_name' in df.columns:
        df['product_name'] = df['product_name'].fillna('unknown')
    
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('unknown')
    
    if 'region' in df.columns:
        df['region'] = df['region'].fillna('unknown')

def remove_duplicate_rows(df):
    "remove duplicate rows"
    df = df.drop_duplicates()

def handle_bad_num_vals(df):
    "handle bad numeric values"
    if 'quantity' in df.columns:
        df = df[df['quantity'] > 0]
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] > 0]
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] == 0]
    if 'sales' in df.columns:
        df = df[df['sales'] > 0]
def analysis_friendly(df):
    "make the data more analysis friendly"
    if 'order_month' not in df.columns:
        df['order_month'] = df['order_date'].dt.month
    if 'order_day' not in df.columns:
        df['order_day'] = df['order_date'].dt.day
    if 'order_year' not in df.columns:
        df['order_year'] = df['order_date'].dt.year
    if 'sales' not in df.columns:
        df['sales'] = df['quantity'] * df['unit_price']

    return df
def clean_data(df):
    #normalize column names
    df.columns = normalize_column_names(df.columns)
    convert_data_types(df)
    create_missing_deriv_columns(df)
    handle_missing_values(df)
    remove_duplicate_rows(df)
    # check if rows of unit_price is nan
    if 'unit_price' in df.columns and df['unit_price'].isna().any():
        if "sales" not in df.columns or "quantity" not in df.columns:
            raise ValueError("Cannot estimate unit_price without sales and quantity.")

        if (df["quantity"] == 0).any():
            raise ValueError("Cannot estimate unit_price because some quantity values are zero.")

        df["estimated_unit_price"] = df["sales"] / df["quantity"]
    handle_bad_num_vals(df)
    analysis_friendly(df)

    return df


#test the function
if __name__ == "__main__":
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

        