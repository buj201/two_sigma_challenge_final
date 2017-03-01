import pandas as pd
import numpy as np
import os
import itertools

from ..features import build_features

if __name__ == '__main__':
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    years = range(2014,2017)
    months = [str(x).zfill(2) for x in range(1,13)]


    #Note the columns numbers are consistant, but names are not
    column = [1]

    column_name = ['Start Time']


    for year, month in itertools.product(years, months):
        print "Reading data for {}/{}...".format(month, year)

        filename = os.path.join(project_dir, 'data/raw/{}{}-citibike-tripdata.zip'.format(year, month))

        sample = pd.read_csv(filename, usecols=column, nrows=1).loc[0][0]
        if sample.find('-') != -1:
            format='%Y-%m-%d %H:%M:%S'
        else:
            if sample.count(':') == 1:
                format='%m/%d/%Y %H:%M'
            elif sample.count(':') == 2:
                format='%m/%d/%Y %H:%M:%S'
        df = pd.read_csv(filename, usecols=column)
        df.columns = column_name

        df['Start Time'] =  pd.to_datetime(df['Start Time'], format=format)

        df = build_features.format_monthly_data(df)

        filename = os.path.join(project_dir, 'data/interim/{}{}-processed.csv.gz'.format(year, month))
        df.to_csv(filename, index=True, compression='gzip')
