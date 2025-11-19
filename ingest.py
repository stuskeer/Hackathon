import pandas as pd
import os

def load_excel_data():

    # Define data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load Edinburgh daytime data - all sheets
    edinburgh_path = os.path.join(data_dir, 'Edinburgh-daytime.xlsx')
    edinburgh_df = pd.read_excel(edinburgh_path, sheet_name=None)  # Returns dict of DataFrames
    
    # Load Strathspey weather data - all sheets
    strathspey_path = os.path.join(data_dir, 'Strathspey-weather.xlsx')
    strathspey_df = pd.read_excel(strathspey_path, sheet_name=None)  # Returns dict of DataFrames
    
    return edinburgh_df, strathspey_df


if __name__ == "__main__":
    # Load the data
    edinburgh_df, strathspey_df = load_excel_data()
    
    print("Edinburgh Daytime Data:")
    for sheet_name, df in edinburgh_df.items():
        print(f"\n--- Sheet: {sheet_name} ---")
        print(df.head())
        print(f"Columns: {list(df.columns)}")

    print("\nStrathspey Weather Data:")
    for sheet_name, df in strathspey_df.items():
        print(f"\n--- Sheet: {sheet_name} ---")
        print(df.head())
        print(f"Columns: {list(df.columns)}")