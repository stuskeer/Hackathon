# Hackathon Project - Weather Data Pipeline

A data processing pipeline that ingests, cleans, and combines weather and daylight data from Edinburgh and Strathspey, Scotland. The pipeline processes multi-sheet Excel files and generates both combined daily data and minute-level temperature interpolations using sinusoidal modeling.

## File Structure

```
Hackathon/
├── main.py                 # Main pipeline orchestrator
├── ingest.py              # Data loading module
├── clean.py               # Data cleaning and processing module
├── resample.py            # Data combination and resampling module
├── config.py              # Column definitions and data types
├── requirements.txt       # Python package dependencies
├── readme.md             # Project documentation
├── data/                 # Source data directory
│   ├── Edinburgh-daytime.xlsx
│   └── Strathspey-weather.xlsx
├── dataOut/              # Output directory
│   ├── combined_data.csv
│   └── temperature_minute_2012.csv
└── __pycache__/          # Python cache files
```

## Project Modules

### `ingest.py`
Loads Excel data from Edinburgh daytime and Strathspey weather files (multi-sheet workbooks)

### `config.py`
Contains column definitions and data type specifications for both datasets

### `clean.py`
Cleans and processes data from both sources:
  - Removes header rows and empty rows
  - Applies column names from config
  - Converts data types and handles datetime parsing from sheet names (YYMM format)
  - Cleans string columns and extracts sunrise/sunset times
  - Concatenates all sheets into single dataframes

### `resample.py`
Combines and resamples the data:
  - Merges Edinburgh and Strathspey dataframes on the 'date' column
  - Filters data for 2012
  - Creates minute-level time series for the entire year
  - Applies **sinusoidal temperature interpolation** for realistic daily temperature curves
  - Temperature patterns: minimum at 6 AM, maximum at 3 PM
  - Rounds all temperature values to 4 decimal places
  - Exports both combined daily data and minute-level temperature data

### `main.py`
Entry point that orchestrates the entire pipeline (ingest → clean → resample)

## Setup

Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- numpy
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
- Columns: `datetime`, `temp_mean`, `temp_min`, `temp_max` (rounded to 4 decimal places)
- Values are calculated using **sinusoidal interpolation** for realistic daily temperature patterns
- Temperature curve assumptions:
  - Minimum temperature occurs at 6:00 AM
  - Maximum temperature occurs at 3:00 PM (15:00)
  - Smooth transitions throughout the day following a sine wave pattern
- Useful for high-resolution time-series analysis and realistic temperature modeling

## Data Sources

- **Edinburgh Daytime Data**: Solar and daylight information including sunrise/sunset times, twilight periods, and solar noon
- **Strathspey Weather Data**: Daily weather measurements including temperature, rainfall, pressure, wind speed/direction, and sunshine hours

## Notes

- Date parsing extracts year/month from Excel sheet names (YYMM format, e.g., '1112' = November 2011)
- Temperature interpolation uses **sinusoidal modeling** for realistic daily temperature variations
- Sinusoidal curve creates natural temperature patterns with smooth transitions between daily min/max values
- All temperature values are rounded to 4 decimal places for consistency
- Temperature estimation anchor: each day's temperature data is based on noon readings from source data

## Recent Updates

- **Sinusoidal Temperature Modeling**: Replaced linear interpolation with sinusoidal curves for more realistic temperature patterns throughout the day
- **Precision Enhancement**: All temperature outputs now rounded to 4 decimal places
- **Integrated Pipeline**: Main.py now orchestrates the complete workflow from ingestion through output generation