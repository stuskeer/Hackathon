import pandas as pd
import numpy as np
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

# Create a function to apply sinusoidal temperature variation within each day
def apply_sinusoidal_temperature(minute_df, temp_data):
    """
    Apply sinusoidal temperature variation to each day based on daily min/max/mean values.
    Temperature follows a sine curve with minimum at sunrise and maximum in early afternoon.
    """
    result_df = minute_df.copy()
    result_df['temp_mean'] = np.nan
    result_df['temp_min'] = np.nan
    result_df['temp_max'] = np.nan
    
    # Get daily temperature values
    daily_temps = temp_data.set_index('datetime')
    
    # Group minutes by date
    result_df['date_only'] = result_df['datetime'].dt.date
    
    for date in result_df['date_only'].unique():
        # Get minutes for this date
        day_mask = result_df['date_only'] == date
        day_minutes = result_df[day_mask].copy()
        
        # Find the closest daily temperature readings (before and after)
        date_datetime = pd.Timestamp(date)
        noon_datetime = date_datetime + pd.Timedelta(hours=12)
        
        # Get temperature values for this day (from noon reading)
        if noon_datetime in daily_temps.index:
            day_temp_mean = daily_temps.loc[noon_datetime, 'temp_mean']
            day_temp_min = daily_temps.loc[noon_datetime, 'temp_min']
            day_temp_max = daily_temps.loc[noon_datetime, 'temp_max']
        else:
            # If exact noon time not found, interpolate from nearest days
            nearest_idx = daily_temps.index.get_indexer([noon_datetime], method='nearest')[0]
            day_temp_mean = daily_temps.iloc[nearest_idx]['temp_mean']
            day_temp_min = daily_temps.iloc[nearest_idx]['temp_min']
            day_temp_max = daily_temps.iloc[nearest_idx]['temp_max']
        
        # Skip if we don't have valid temperature data
        if pd.isna(day_temp_mean) or pd.isna(day_temp_min) or pd.isna(day_temp_max):
            continue
        
        # Calculate sinusoidal temperature for each minute
        # Assume: minimum temp at 6 AM, maximum temp at 3 PM (15:00)
        hour_of_day = day_minutes['datetime'].dt.hour + day_minutes['datetime'].dt.minute / 60.0
        
        # For temp_mean: use a sine wave that peaks at 3 PM and has minimum at 6 AM
        # Shift sine wave so minimum is at hour 6 and maximum at hour 15
        phase_shift = (hour_of_day - 6) * (2 * np.pi / 24)  # 24-hour cycle
        sine_value = np.sin(phase_shift - np.pi/2)  # -1 to 1
        
        # Scale sine wave to go from day_temp_min to day_temp_max
        amplitude = (day_temp_max - day_temp_min) / 2
        midpoint = (day_temp_max + day_temp_min) / 2
        temp_mean_curve = midpoint + amplitude * sine_value
        
        # For temp_min and temp_max, apply similar but shifted curves
        # temp_min follows a similar pattern but stays closer to minimum
        temp_min_curve = day_temp_min + amplitude * 0.5 * (sine_value + 1)
        
        # temp_max follows similar pattern but stays closer to maximum  
        temp_max_curve = day_temp_max - amplitude * 0.5 * (1 - sine_value)
        
        # Assign calculated values back to result dataframe
        result_df.loc[day_mask, 'temp_mean'] = temp_mean_curve.values
        result_df.loc[day_mask, 'temp_min'] = temp_min_curve.values
        result_df.loc[day_mask, 'temp_max'] = temp_max_curve.values
    
    # Drop the temporary date column
    result_df = result_df.drop('date_only', axis=1)
    
    # Fill any remaining NaN values with interpolation for edge cases
    result_df['temp_mean'] = result_df['temp_mean'].interpolate(method='linear', limit_direction='both')
    result_df['temp_min'] = result_df['temp_min'].interpolate(method='linear', limit_direction='both')
    result_df['temp_max'] = result_df['temp_max'].interpolate(method='linear', limit_direction='both')
    
    return result_df

# Apply sinusoidal temperature estimation
minute_df = apply_sinusoidal_temperature(minute_df, temp_data)

# Round temperature columns to 4 decimal places
minute_df['temp_mean'] = minute_df['temp_mean'].round(4)
minute_df['temp_min'] = minute_df['temp_min'].round(4)
minute_df['temp_max'] = minute_df['temp_max'].round(4)

# Export to CSV
minute_df.to_csv('dataOut/temperature_minute_2012.csv', index=False)
print(f"\nTemperature estimates for every minute in 2012 exported to dataOut/temperature_minute_2012.csv")
print(f"Total records: {len(minute_df)}")
print(f"\nSample data:")
print(minute_df.head(10))


