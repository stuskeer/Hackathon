import pandas as pd
from clean import edinburgh_df, strathspey_df

# combine two dataframes created on clean.py on 'date' column
def combine(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.merge(df1, df2, on='date', how='inner', suffixes=('_edinburgh', '_strathspey'))
    return combined_df

# Combine the dataframes
combined_df = combine(edinburgh_df, strathspey_df)

# Export to CSV in data folder
combined_df.to_csv('data/combined_data.csv', index=False)
print("\nData exported to data/combined_data.csv")