import pandas as pd
from clean import edinburgh_df, strathspey_df

# combine two dataframes created on clean.py on 'date' column
def combine(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.merge(df1, df2, on='date', how='inner', suffixes=('_edinburgh', '_strathspey'))
    return combined_df

# Combine the dataframes
combined_df = combine(edinburgh_df, strathspey_df)

# Export to CSV in data folder
combined_df.to_csv('dataOut/combined_data.csv', index=False)
print("\nData exported to dataOut/combined_data.csv")

# Filter data for 2012
combined_df_2012 = combined_df[combined_df['date'].dt.year == 2012].copy()

# Create minute-level time series for 2012
start_date = '2012-01-01 00:00:00'
end_date = '2012-12-31 23:59:00'
minute_range = pd.date_range(start=start_date, end=end_date, freq='T')  # 'T' = minute frequency

# Create dataframe with minute timestamps
minute_df = pd.DataFrame({'datetime': minute_range})

# Prepare temperature data from combined_df_2012
# Assuming we have temp_mean, temp_min, temp_max from Strathspey data
temp_data = combined_df_2012[['date', 'temp_mean', 'temp_min', 'temp_max']].copy()

# Convert temperature columns to numeric (they may be strings)
temp_data['temp_mean'] = pd.to_numeric(temp_data['temp_mean'], errors='coerce')
temp_data['temp_min'] = pd.to_numeric(temp_data['temp_min'], errors='coerce')
temp_data['temp_max'] = pd.to_numeric(temp_data['temp_max'], errors='coerce')

# Set date as datetime with time at noon for interpolation
temp_data['datetime'] = pd.to_datetime(temp_data['date']) + pd.Timedelta(hours=12)
temp_data = temp_data.drop('date', axis=1)

# Sort by datetime
temp_data = temp_data.sort_values('datetime')

# Merge with minute_df and interpolate
minute_df = minute_df.merge(temp_data, on='datetime', how='left')

# Interpolate temperature values for every minute using linear interpolation
minute_df['temp_mean'] = minute_df['temp_mean'].interpolate(method='linear', limit_direction='both')
minute_df['temp_min'] = minute_df['temp_min'].interpolate(method='linear', limit_direction='both')
minute_df['temp_max'] = minute_df['temp_max'].interpolate(method='linear', limit_direction='both')

# Export to CSV
minute_df.to_csv('dataOut/temperature_minute_2012.csv', index=False)
print(f"\nTemperature estimates for every minute in 2012 exported to dataOut/temperature_minute_2012.csv")
print(f"Total records: {len(minute_df)}")
print(f"\nSample data:")
print(minute_df.head(10))


