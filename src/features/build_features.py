import pandas as pd
import numpy as np
import os

def format_monthly_data(df):
    """ Formats monthly trip data by:
            - Counting number of trips per day
            - Constructing datetime features (day of week and month)

        Args:
            - df: Pandas dataframe with single datetime columns "Start Time"

        Returns:
            - df: Formatted pandas DataFrame

    """
    #Make datetime features
    df['Date'] = df['Start Time'].dt.floor('d')
    df.drop('Start Time', axis=1, inplace=True)
    df = df.groupby('Date').size().to_frame('Trip Count')
    df['Day of Week'] = df.index.dayofweek
    df['Month'] = df.index.month
    df = make_fixed_time_effects_feature(df)

    return df

def make_fixed_time_effects_feature(df):
    """ Note in our model we will assume there is a seasonal pattern
        with a fixed annual frequency, and a linear growth trend
        for system wide usage. This function adds necessary features

        Args:
            -df: pandas dataframe with datetime index

        Returns:
            -df: pandas dataframe with these additional features
    """

    df['t'] = df.index - pd.to_datetime('2014-01-01 00:00:00')
    df['t'] = df['t'].dt.days
    df['cos_t'] = np.cos(2*np.pi*df['t']/365.25)
    df['sin_t'] = np.cos(2*np.pi*df['t']/365.25)

    return df

def format_NOAA_data(project_dir):
    """ Formats daily NOAA data by:
            - Filling missing values using the average of forward/back fill
            - Dropping fields with many missing values

        Args:
            -project_dir: Path to project directory (os.path)

        Returns:
            - df: Formatted pandas DataFrame with datetime index

    """
    df = pd.read_csv(os.path.join(project_dir, 'data/external/NOAA_data.csv.gz'), parse_dates=[0], index_col=0)
    df = df[['PRCP','SNOW','SNWD','TMAX','TMIN','AWND','WSF2','WSF5', 'WT01', 'WT08']]
    df = df.fillna({'WT01':0, 'WT08':0})
    for col in df.columns:
        df[col] = get_forward_back_avg(df[col])
    return df

def get_forward_back_avg(series):
    forward = series.ffill()
    back = series.bfill()
    average = (forward + back)/2.0
    return average


