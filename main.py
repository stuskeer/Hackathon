from ingest import load_excel_data

if __name__ == "__main__":
    print("Starting data pipeline...")
    
    # Step 1: Ingest - Load data
    print("\n=== Step 1: Ingesting Data ===")
    from ingest import load_excel_data
    edinburgh_df, strathspey_df = load_excel_data()
    print("✓ Data loaded successfully")
    
    # Step 2: Clean - Process and clean the data
    print("\n=== Step 2: Cleaning Data ===")
    from clean import edinburgh_df as cleaned_edinburgh_df, strathspey_df as cleaned_strathspey_df
    print("✓ Data cleaned and processed")
    
    # Step 3: Resample - Combine and create minute-level data
    print("\n=== Step 3: Resampling Data ===")
    import resample
    print("✓ Data combined and resampled")
    
    print("\n=== Data Pipeline Completed Successfully! ===")
    print("\nOutputs:")
    print("  - dataOut/combined_data.csv")
    print("  - dataOut/temperature_minute_2012.csv")