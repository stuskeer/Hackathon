from ingest import load_excel_data

if __name__ == "__main__":
    print("Starting data pipeline...")
    
    # Run ingest.py functionality
    print("\n=== Step 1: Loading Data ===")
    edinburgh_df, strathspey_df = load_excel_data()
    
    print("\n=== Edinburgh Daytime Data ===")
    for sheet_name, df in edinburgh_df.items():
        print(f"\n--- Sheet: {sheet_name} ---")
        print(df.head())
        print(f"Columns: {list(df.columns)}")
    
    print("\n=== Strathspey Weather Data ===")
    for sheet_name, df in strathspey_df.items():
        print(f"\n--- Sheet: {sheet_name} ---")
        print(df.head())
        print(f"Columns: {list(df.columns)}")
    
    print("\n=== Data Loaded into Dataframes ===")

    print("\nData pipeline completed successfully!")