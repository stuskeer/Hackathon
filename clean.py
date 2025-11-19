import pandas as pd
from ingest import load_excel_data

# start with data loading
edinburgh_df, strathspey_df = load_excel_data()

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