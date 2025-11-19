import pandas as pd
from ingest import load_excel_data

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