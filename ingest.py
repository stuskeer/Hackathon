import pandas as pd
import os

def load_excel_data():

    # Define data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load Edinburgh daytime data
    edinburgh_path = os.path.join(data_dir, 'Edinburgh-daytime.xlsx')
    edinburgh_df = pd.read_excel(edinburgh_path)
    print(f"Loaded Edinburgh data: {edinburgh_df.shape[0]} rows, {edinburgh_df.shape[1]} columns")
    
    # Load Strathspey weather data
    strathspey_path = os.path.join(data_dir, 'Strathspey-weather.xlsx')
    strathspey_df = pd.read_excel(strathspey_path)
    print(f"Loaded Strathspey data: {strathspey_df.shape[0]} rows, {strathspey_df.shape[1]} columns")
    
    return edinburgh_df, strathspey_df


if __name__ == "__main__":
    # Load the data
    edinburgh_df, strathspey_df = load_excel_data()
    
    # Display basic information
    print("\n=== Edinburgh Daytime Data ===")
    print(edinburgh_df.head())
    print(f"\nColumns: {list(edinburgh_df.columns)}")
    
    print("\n=== Strathspey Weather Data ===")
    print(strathspey_df.head())
    print(f"\nColumns: {list(strathspey_df.columns)}")
