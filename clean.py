import pandas as pd
from ingest import load_excel_data
from config import EDINBURGH_COLUMNS, STRATHSPEY_COLUMNS
import re

# start with data loading
edinburgh_df, strathspey_df = load_excel_data()

# drop first 2 header rows
for sheet_name in edinburgh_df:
    edinburgh_df[sheet_name] = edinburgh_df[sheet_name].iloc[2:].reset_index(drop=True)

for sheet_name in strathspey_df:
    strathspey_df[sheet_name] = strathspey_df[sheet_name].iloc[5:].reset_index(drop=True)

# remove empty rows
for sheet_name in edinburgh_df:
    edinburgh_df[sheet_name] = edinburgh_df[sheet_name].dropna(how='all').reset_index(drop=True)

for sheet_name in strathspey_df:
    strathspey_df[sheet_name] = strathspey_df[sheet_name].dropna(how='all').reset_index(drop=True)

# remove rows without a date in the first column
for sheet_name in edinburgh_df:
    first_col = edinburgh_df[sheet_name].columns[0]
    edinburgh_df[sheet_name] = edinburgh_df[sheet_name][pd.to_numeric(edinburgh_df[sheet_name][first_col], errors='coerce').notnull()].reset_index(drop=True)
for sheet_name in strathspey_df:
    first_col = strathspey_df[sheet_name].columns[0]
    strathspey_df[sheet_name] = strathspey_df[sheet_name][pd.to_numeric(strathspey_df[sheet_name][first_col], errors='coerce').notnull()].reset_index(drop=True)

# apply column names from config.py
for sheet_name in edinburgh_df:
    edinburgh_df[sheet_name].columns = list(EDINBURGH_COLUMNS.keys())
    # Convert dtypes, handling datetime columns separately
    first_col = list(EDINBURGH_COLUMNS.keys())[0]
    for col, dtype in EDINBURGH_COLUMNS.items():
        if col == first_col and (dtype == pd.Timestamp or dtype == 'datetime64[ns]'):
            # Parse sheet name format YYMM (e.g., '1112' = Nov 2011)
            year = '20' + sheet_name[:2]
            month = sheet_name[2:4]
            day = pd.to_numeric(edinburgh_df[sheet_name][col], errors='coerce')
            # Create date strings by combining year-month-day
            date_strings = year + '-' + month + '-' + day.fillna(0).astype(int).astype(str)
            edinburgh_df[sheet_name][col] = pd.to_datetime(date_strings, format='%Y-%m-%d', errors='coerce')
        elif dtype == pd.Timestamp or dtype == 'datetime64[ns]':
            edinburgh_df[sheet_name][col] = pd.to_datetime(edinburgh_df[sheet_name][col], errors='coerce')
        elif dtype in [float, 'float64', 'float32']:
            # Replace comma with period for European decimal format
            edinburgh_df[sheet_name][col] = edinburgh_df[sheet_name][col].astype(str).str.replace(',', '.', regex=False)
            edinburgh_df[sheet_name][col] = pd.to_numeric(edinburgh_df[sheet_name][col], errors='coerce')
        elif dtype in [int, 'int64', 'int32']:
            # Use nullable integer type to handle NaN values
            edinburgh_df[sheet_name][col] = edinburgh_df[sheet_name][col].astype(str).str.replace(',', '.', regex=False)
            edinburgh_df[sheet_name][col] = pd.to_numeric(edinburgh_df[sheet_name][col], errors='coerce').astype('Int64')
        else:
            edinburgh_df[sheet_name][col] = edinburgh_df[sheet_name][col].astype(dtype)

for sheet_name in strathspey_df:
    strathspey_df[sheet_name].columns = list(STRATHSPEY_COLUMNS.keys())
    # Convert dtypes, handling datetime columns separately
    first_col = list(STRATHSPEY_COLUMNS.keys())[0]
    for col, dtype in STRATHSPEY_COLUMNS.items():
        if col == first_col and (dtype == pd.Timestamp or dtype == 'datetime64[ns]'):
            # Parse sheet name format YYMM
            year = '20' + sheet_name[:2]
            month = sheet_name[2:4]
            day = pd.to_numeric(strathspey_df[sheet_name][col], errors='coerce')
            # Create date strings by combining year-month-day
            date_strings = year + '-' + month + '-' + day.fillna(0).astype(int).astype(str)
            strathspey_df[sheet_name][col] = pd.to_datetime(date_strings, format='%Y-%m-%d', errors='coerce')
        elif dtype == pd.Timestamp or dtype == 'datetime64[ns]':
            strathspey_df[sheet_name][col] = pd.to_datetime(strathspey_df[sheet_name][col], errors='coerce')
        elif dtype in [float, 'float64', 'float32']:
            # Replace comma with period for European decimal format
            strathspey_df[sheet_name][col] = strathspey_df[sheet_name][col].astype(str).str.replace(',', '.', regex=False)
            strathspey_df[sheet_name][col] = pd.to_numeric(strathspey_df[sheet_name][col], errors='coerce')
        elif dtype in [int, 'int64', 'int32']:
            # Use nullable integer type to handle NaN values
            strathspey_df[sheet_name][col] = strathspey_df[sheet_name][col].astype(str).str.replace(',', '.', regex=False)
            strathspey_df[sheet_name][col] = pd.to_numeric(strathspey_df[sheet_name][col], errors='coerce').astype('Int64')
        else:
            strathspey_df[sheet_name][col] = strathspey_df[sheet_name][col].astype(dtype)

# Cleans string columns - applies string cleaning to text fields
def clean_string_column(series):
    series = series.astype(str).str.strip()  # Remove leading/trailing whitespace
    series = series.str.replace(r'[-°↑()]', '', regex=True)  # Remove -, °, ↑, (, and ) characters
    series = series.replace({'': None, 'nan': None, 'NaN': None})  # Replace empty strings with None
    return series

# trim sunrise/sunset columns to remove anything but time in edinburgh data
for sheet_name in edinburgh_df: 
    if 'sunrise' in edinburgh_df[sheet_name].columns:
        edinburgh_df[sheet_name]['sunrise'] = edinburgh_df[sheet_name]['sunrise'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0]
    if 'sunset' in edinburgh_df[sheet_name].columns:
        edinburgh_df[sheet_name]['sunset'] = edinburgh_df[sheet_name]['sunset'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0]
# Apply string cleaning to all string columns in both dataframes
for sheet_name in edinburgh_df:
    for col in edinburgh_df[sheet_name].columns:
        if edinburgh_df[sheet_name][col].dtype == 'object':
            edinburgh_df[sheet_name][col] = clean_string_column(edinburgh_df[sheet_name][col])

for sheet_name in strathspey_df:
    for col in strathspey_df[sheet_name].columns:
        if strathspey_df[sheet_name][col].dtype == 'object':
            strathspey_df[sheet_name][col] = clean_string_column(strathspey_df[sheet_name][col])

# print data heads after dropping headers and emopty rows
print("Edinburgh Daytime Data after dropping headers and empty rows:")
for sheet_name in edinburgh_df:
    print(edinburgh_df[sheet_name].head())

print("\nStrathspey Daytime Data after dropping headers and empty rows:")
for sheet_name in strathspey_df:
    print(strathspey_df[sheet_name].head())





'''
# remove nan values
for sheet_name in edinburgh_df:
    edinburgh_df[sheet_name] = edinburgh_df[sheet_name].dropna()

for sheet_name in strathspey_df:
    strathspey_df[sheet_name] = strathspey_df[sheet_name].dropna()


# 

# print cleaned data info
print("Cleaned Edinburgh Daytime Data:")
for sheet_name in edinburgh_df:
    print(f"Sheet: {sheet_name}, Shape: {edinburgh_df[sheet_name].shape}")

print("\nCleaned Strathspey Daytime Data:")
for sheet_name in strathspey_df:
    print(f"Sheet: {sheet_name}, Shape: {strathspey_df[sheet_name].shape}")

    '''