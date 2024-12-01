import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv  
from config.paths import dir_input_raw, dir_input_cleaned

# Growth rate calculation function
def growth_rate(df):
    """
    Compute the growth rate for all columns (except 'date'), handling missing values appropriately.
    For quarterly data, growth rate is calculated for available values only, and NaNs are left as-is.
    """
    # Iterate over all columns except 'date'
    for col in df.columns[1:]:
        # Extract the series and drop missing values
        series = df[['date', col]].dropna(subset=[col])
        
        # Calculate the growth rate for the non-NaN values
        series[col] = series[col].pct_change()  # This is equivalent to (current / previous) - 1
        
        # Merge the calculated growth rates back into the original DataFrame
        df = df.drop(columns=[col]).merge(series, on='date', how='left')
    
    return df


def execute():
    
    # Load the API key from the .env file
    load_dotenv()
    api_key = os.getenv('FRED_API_KEY')
    fred = Fred(api_key=api_key)

    # Load the metadata
    meta_data = pd.read_csv(os.path.join(dir_input_raw, 'meta_data.csv'))

    # Generate a date sequence from 1900-01-01 to the first day of the current month
    data = pd.DataFrame({
        'date': pd.date_range(start='1900-01-01', 
                            end=pd.Timestamp.now().replace(day=1), 
                            freq='MS')
    })

    # Iterate over the metadata and fetch data from FRED
    for series_id in meta_data['series'].str.upper():
        print(f"Fetching data for series: {series_id}")
        tmp = fred.get_series(series_id)
        
        # Convert the series to a DataFrame
        tmp_df = pd.DataFrame({
            'date': tmp.index,
            series_id.lower(): tmp.values
        })
        
        # Merge with the main data frame
        data = pd.merge(data, tmp_df, on='date', how='left')

    # Find the first GDP value that's not NaN
    first_gdp_date = data.loc[data['gdpc1'].notna(), 'date'].min()

    # Filter out rows before the first GDP value
    data = data[data['date'] >= first_gdp_date].sort_values(by='date', ascending=False)

    # Move quarterly values to the last month of the quarter instead of the first
    for i, row in meta_data.iterrows():
        series_id = row['series'].lower()
        frequency = row['freq']
        
        if frequency == 'q':  # if quarterly
            data[series_id] = data[series_id].shift(-2)

    # Write the final data to a CSV file
    data.to_csv(os.path.join(dir_input_cleaned, 'data_raw.csv'), index=False)
    
    # Apply the growth rate transformation
    data = data.sort_values(by='date')
    data = growth_rate(data)
    
    data.to_csv(os.path.join(dir_input_cleaned, 'data_tf.csv'), index=False)
    print(f"FRED dataset saved to input/cleaned/data_tf.csv")