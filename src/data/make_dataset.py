import itertools
import numpy as np
import pandas as pd
import os
from ..features import build_features
from . import make_train_test_splits

#Preprocessing
from sklearn.preprocessing import StandardScaler

#Model Selection
from sklearn.model_selection import train_test_split

def main(project_dir):

    """ Runs all data processing and cleaning, turning raw and external data
        (from data/raw and data/external) into final tidy data frame for
        modeling (saved in data/processed)/.

        Args:
            -project_dir: Path to project directory (os.path)

        Returns:
            - None (data saved in data/processed)

    """
    #Read in and clean trips data and weather data
    print 'Formatting NOAA data...'
    NOAA = build_features.format_NOAA_data(project_dir)

    print 'Joining monthly trips datasets...'
    all_trips = join_monthly_data(project_dir)

    #Merge datasets on date
    print 'Merging NOAA and trips dataset by date...'
    merged = all_trips.join(NOAA, how='left')
    for feature, count in merged.count().iteritems():
        assert count == merged.shape[0], '{} is missing {} values.'.format(feature, merged.shape[0] - count)

    #Make train/test splits and save
    make_train_test_splits.make_train_test_splits(merged, project_dir)

def join_monthly_data(project_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned trip data, which is returned (as Pandas DataFrame) for
        merging with NOAA data.

        Args:
            -project_dir: Path to project directory (os.path)

        Return:
            - raw_data: Pandas DataFrame
    """

    #Note the columns numbers are consistant, but names are not

    first = True

    years = range(2014,2017)
    months = [str(x).zfill(2) for x in range(1,13)]

    for year, month in itertools.product(years, months):
        filename = os.path.join(project_dir, 'data/interim/{}{}-processed.csv.gz'.format(year, month))
        df = pd.read_csv(filename, parse_dates=[0], index_col=0)

        if first:
            all_data = df
            first = False
        else:
            all_data = all_data.append(df, ignore_index=False)

    #Add rolling average from 7 day window, 7 days in past
    #This assumes use case of making predictions a week in advance
    #to schedule maintenance
    rolling_avg = all_data['Trip Count'].rolling(window=7,center=False).mean().shift(6)
    rolling_avg.name = 'Last_week_average'

    all_data = all_data.join(rolling_avg)
    all_data.dropna(axis=0, how='any', inplace=True)

    return all_data

if __name__ == '__main__':
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    main(project_dir)
