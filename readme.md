# Hackathon Project - Weather Data Pipeline

A data processing pipeline that ingests, cleans, and combines weather and daylight data from Edinburgh and Strathspey, Scotland.

## Project Structure

- `ingest.py` - Loads Excel data from Edinburgh daytime and Strathspey weather files
- `config.py` - Contains column definitions and data type specifications for both datasets
- `clean.py` - Cleans and processes data from both sources, including:
  - Removing header rows and empty rows
  - Applying column names from config
  - Converting data types and handling datetime parsing
  - Cleaning string columns and extracting sunrise/sunset times
  - Concatenating all sheets into single dataframes
- `resample.py` - Combines the cleaned Edinburgh and Strathspey dataframes on the 'date' column and exports to CSV
- `main.py` - Entry point to run the data pipeline
- `data/` - Directory containing source Excel files and output CSV files

## Setup

Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

Run the entire data pipeline:
```bash
python main.py
```

Run individual scripts:
```bash
python clean.py         # Clean and process data
python resample.py      # Combine datasets and export to CSV
```

## Output

The combined dataset is exported to `data/combined_data.csv` with columns from both Edinburgh daytime data and Strathspey weather data, merged on the date column with suffixes `_edinburgh` and `_strathspey`.