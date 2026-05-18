from schema import (
    OPTIONAL_COLUMNS,
    OPTIONAL_NUMERIC_COLUMNS,
    OPTIONAL_TEXT_COLUMNS,
    REQUIRED_COLUMNS,
    REQUIRED_DATE_COLUMNS,
    REQUIRED_NUMERIC_COLUMNS,
    REQUIRED_TEXT_COLUMNS,
    canonical_column_name,
    normalize_column_names 
)
import pandas as pd
TEST_MODE = True

"""Validate the data against the schema."""

required_columns_to_validate = REQUIRED_COLUMNS
optional_columns_to_validate = OPTIONAL_COLUMNS

def validate_data_columns(df):
    present_columns = normalize_column_names(df.columns) #get the present columns in the dataframe

   # list of missing and present columns
    missing_required = []
    present_required = []
    present_optional = []
    missing_optional = []

    # check for missing and present required columns
    for col in required_columns_to_validate:
        if col in present_columns:
            present_required.append(col)
        else:
            missing_required.append(col)

    # check for missing and present optional columns
    for col in optional_columns_to_validate:
        if col in present_columns:
            present_optional.append(col)
        else:
            missing_optional.append(col)

    # raise an error if any required columns are missing
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")

    return {
        "present_required": present_required,
        "missing_required": missing_required,
        "present_optional": present_optional,
        "missing_optional": missing_optional,
    }


#main
def validate_data_types(df):
    df = df.copy()

    # Rename columns to canonical names first
    df.columns = normalize_column_names(df.columns)

    # Make sure required columns exist before checking types
    validate_data_columns(df)

    errors = []
    warnings = []

    # Required numeric columns
    for col in REQUIRED_NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[col], errors="coerce")

        if converted.isna().all():
            errors.append(f"{col} could not be converted to numbers.")
        elif converted.isna().any():
            warnings.append(f"{col} has some values that could not be converted to numbers.")

    # Required date columns
    for col in REQUIRED_DATE_COLUMNS:
        converted = pd.to_datetime(df[col], errors="coerce")

        if converted.isna().all():
            errors.append(f"{col} could not be converted to dates.")
        elif converted.isna().any():
            warnings.append(f"{col} has some values that could not be converted to dates.")

    # Required text columns
    for col in REQUIRED_TEXT_COLUMNS:
        converted = df[col].astype(str).str.strip()

        if converted.eq("").all():
            errors.append(f"{col} is empty.")
        elif converted.eq("").any():
            warnings.append(f"{col} has some empty values.")

    # Optional numeric columns
    for col in OPTIONAL_NUMERIC_COLUMNS:
        if col in df.columns:
            converted = pd.to_numeric(df[col], errors="coerce")

            if converted.isna().all():
                warnings.append(f"Optional column {col} could not be converted to numbers.")
            elif converted.isna().any():
                warnings.append(f"Optional column {col} has some non-numeric values.")

    # Optional text columns
    for col in OPTIONAL_TEXT_COLUMNS:
        if col in df.columns:
            converted = df[col].astype(str).str.strip()

            if converted.eq("").all():
                warnings.append(f"Optional column {col} is empty.")
            elif converted.eq("").any():
                warnings.append(f"Optional column {col} has some empty values.")

    if errors:
        raise ValueError(errors)

    return {
        "is_valid": True,
        "warnings": warnings,
        "columns": list(df.columns),
    }

    

    



    
    


