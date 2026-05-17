"""
load sample data
print original columns
run validation
print validation result
show errors/warnings

"""

from data_loader import load_sample_data
from validation import validate_data_columns, validate_data_types
from schema import normalize_column_names
TEST_MODE = True

# load sample data
df = load_sample_data()
print("Original columns:", df.columns)
#normalize column names
df.columns = normalize_column_names(df.columns)
#if unit price missing create it 
if 'unit_price' not in df.columns:
    if "sales" not in df.columns or "quantity" not in df.columns:
        raise ValueError("Cannot estimate unit_price without sales and quantity.")

    if (df["quantity"] == 0).any():
        raise ValueError("Cannot estimate unit_price because some quantity values are zero.")

    df["unit_price"] = df["sales"] / df["quantity"]

if TEST_MODE == True:
    print("Normalized columns:", df.columns)

    column_result = validate_data_columns(df)
    print("Column validation result:", column_result)

type_result = validate_data_types(df)
print("Type validation result:", type_result)



