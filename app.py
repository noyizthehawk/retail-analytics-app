import streamlit as st
import pandas as pd
from src.data_loader import load_sample_data
from src.schema import normalize_column_names
from src.validation import validate_data_types
from src.cleaning import clean_data
from src.metrics import calculate_summary_metrics
st.set_page_config(page_title="Retail Analytics App", 
                    page_icon=":bar_chart:",
                     layout="wide"
                )

#load data
df = load_sample_data()
df.columns = normalize_column_names(df.columns)
validate_data_types(df)
df = clean_data(df)


#show summary metrics
st.write(calculate_summary_metrics(df))
st.title("Retail Analytics App")
st.write("This is a retail analytics app that allows you to analyze retail data.")

