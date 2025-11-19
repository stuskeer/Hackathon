# Hackathon Project - Weather Data Pipeline

A data processing pipeline that ingests, cleans, and combines weather and daylight data from Edinburgh and Strathspey, Scotland. The pipeline processes multi-sheet Excel files and generates both combined daily data and minute-level temperature interpolations.

## Project Structure

- `ingest.py` - Loads Excel data from Edinburgh daytime and Strathspey weather files (multi-sheet workbooks)
- `config.py` - Contains column definitions and data type specifications for both datasets
- `clean.py` - Cleans and processes data from both sources:
  - Removes header rows and empty rows
  - Applies column names from config
  - Converts data types and handles datetime parsing from sheet names (YYMM format)
  - Cleans string columns and extracts sunrise/sunset times
  - Concatenates all sheets into single dataframes
- `resample.py` - Combines and resamples the data:
  - Merges Edinburgh and Strathspey dataframes on the 'date' column
  - Filters data for 2012
  - Creates minute-level time series for the entire year
  - Interpolates temperature values (mean, min, max) for every minute
  - Exports both combined daily data and minute-level temperature data
- `main.py` - Entry point that orchestrates the entire pipeline (ingest → clean → resample)
- `data/` - Directory containing source Excel files:
  - `Edinburgh-daytime.xlsx` - Daylight and solar data
  - `Strathspey-weather.xlsx` - Weather measurements
- `dataOut/` - Output directory containing processed CSV files

## Setup

Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- openpyxl (for Excel file reading)

## Usage

### Run Complete Pipeline
Execute the entire data processing pipeline with a single command:
```bash
python main.py
```

This will sequentially run:
1. **Ingest** - Load raw Excel data
2. **Clean** - Process and standardize data
3. **Resample** - Combine and create minute-level interpolations

### Run Individual Scripts
For debugging or partial processing:
```bash
python ingest.py        # Load and inspect Excel data
python clean.py         # Clean and process data only
python resample.py      # Combine and resample (requires cleaned data)
```

## Output Files

### `dataOut/combined_data.csv`
Combined daily weather and daylight data from both sources, merged on date with suffixes:
- `_edinburgh` - Daylight-related columns (sunrise, sunset, twilight times, etc.)
- `_strathspey` - Weather-related columns (temperature, rain, pressure, wind, etc.)

### `dataOut/temperature_minute_2012.csv`
Minute-level temperature estimates for the entire year 2012:
- **527,040 records** (one per minute in 2012)
- Columns: `datetime`, `temp_mean`, `temp_min`, `temp_max`
- Values are linearly interpolated between daily readings
- Useful for high-resolution time-series analysis

## Data Sources

- **Edinburgh Daytime Data**: Solar and daylight information including sunrise/sunset times, twilight periods, and solar noon
- **Strathspey Weather Data**: Daily weather measurements including temperature, rainfall, pressure, wind speed/direction, and sunshine hours

## Notes

- Date parsing extracts year/month from Excel sheet names (YYMM format, e.g., '1112' = November 2011)
- Temperature interpolation uses linear method with bidirectional filling for edge cases
- All timestamps in minute-level data use the noon value for each day as interpolation anchor points