import pandas as pd
from ingest import load_excel_data

### Concat all sheets into single dataframes ###
def concat_edinburgh_data(edinburgh_excel):
    """Concatenate all Edinburgh sheets into a single dataframe."""
    dfs = []
    
    for sheet_name, df in edinburgh_excel.items():
        # Add a column to track the source sheet (optional, for debugging)
        df['source_sheet'] = sheet_name
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

def concat_strathspey_data(strathspey_excel):
    """Concatenate all Strathspey sheets into a single dataframe."""
    dfs = []
    
    for sheet_name, df in strathspey_excel.items():
        # Add a column to track the source sheet (optional, for debugging)
        df['source_sheet'] = sheet_name
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

if __name__ == "__main__":
    # Load the data from ingest
    edinburgh_excel, strathspey_excel = load_excel_data()
    
    # Concatenate into two dataframes
    edinburgh_df = concat_edinburgh_data(edinburgh_excel)
    strathspey_df = concat_strathspey_data(strathspey_excel)
 ### concat end ###


    print("Edinburgh DataFrame:")
    print(edinburgh_df.head())
    
    print("\nStrathspey DataFrame:")
    print(strathspey_df.head())

