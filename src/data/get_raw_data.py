import urllib2
import itertools
import os
import requests
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import dotenv

def get_bike_data(project_dir):
    ''' Get raw bike share data and saw in data/raw directory.
        See https://www.citibikenyc.com/system-data for description
        of raw Citi Bike Trip Histories dataset.

        Args:
            -project_dir: Path to project directory (os.path)

        Returns:
            -None: Writes bike data to data/raw
    '''

    baseurl = 'https://s3.amazonaws.com/tripdata/'

    years = range(2014,2017)
    months = [str(x).zfill(2) for x in range(1,13)]

    for year, month in itertools.product(years, months):
        print "Getting data for {}/{}...".format(month, year)
        filename = '{}{}-citibike-tripdata.zip'.format(year, month)
        request = urllib2.urlopen(baseurl + filename)
        with open(os.path.join(project_dir, 'data/raw/', filename), 'w') as f:
            f.write(request.read())

def get_weather_data(project_dir):
    """ Main function for getting weather data from NOAA

        Args:
            -project_dir: Path to project directory (os.path)

        Returns:
            -None: Writes weather data to data/external
    """
    all_years = get_all_years_data(range(2014,2017))
    filename = os.path.join(project_dir, 'data/external/NOAA_data.csv.gz')
    all_years.to_csv(filename, index=True, compression='gzip')

def get_all_year_data(year):
    """ Helper function that fetches all NOAA data for
        Station GHCND:USW00094728 (Central Park, NY)
        for the input year through the NOAA API.

        Args:
            - year: (int) year to get data. Note the station
                    only has data for a certain subset of
                    years (including the years of interest)
                    for this project

        Returns:
            - Data: "Results" dictionary from json API response
    """
    offset=0
    found_all = False
    data = []
    while not found_all:
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?"
        url = url + 'datasetid=GHCND&stationid=GHCND:USW00094728&startdate={0}-01-01&enddate={0}-12-31'.format(year)
        url = url + '&limit=1000&offset={}'.format(offset*1000+1)

        # replace 'myToken' with the actual token, below
        headers = {'token': os.getenv('NOAA_TOKEN')}
        response = requests.get(url, headers = headers)

        print 'Year: {}, Offset:{}, Response: {}'.format(year, offset, response)
        response = response.json()

        if len(response) == 0:
            found_all = True
        else:
            data.extend(response['results'])
            offset += 1

    return data

def get_year_dataframe(year):
    """ Helper function that converts the JSON data fetched
        through the API to a pandas dataframe

        Args:
            - year: (int) year to get data

        Returns:
            - df: (Pandas DataFrame)
    """
    json_data = get_all_year_data(year)
    df = json_normalize(json_data)
    df.drop(['attributes','station'], axis=1, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S')
    df = df.pivot(index='date',columns='datatype',values='value')
    if year % 4 != 0:
        assert df.shape[0] == 365
    else:
        assert df.shape[0] == 366
    return df

def get_all_years_data(year_range):
    """ Helper function that accepts a range of years,
        fetches NOAA data through API, and returns dataframe

        Args:
            - year: (int) year to get data

        Returns:
            - df: (Pandas DataFrame)
    """
    first_year = True
    for year in year_range:
        df = get_year_dataframe(year)
        if first_year:
            all_years = df
            first_year = False
        else:
            all_years = all_years.append(df)

    return all_years

if __name__ == '__main__':
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)
    get_weather_data(project_dir)
    get_bike_data(project_dir)
