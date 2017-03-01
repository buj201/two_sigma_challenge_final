import numpy as np
import pandas as pd
import os

#Preprocessing
from sklearn.preprocessing import StandardScaler

#Model Selection
from sklearn.model_selection import train_test_split


def make_train_test_splits(df, project_dir):
    """ Makes training/test splits and saves to data/processed.

    """

    categorical_features = ['Day of Week',
                            'WT01',
                            'WT08']

    continuous_features = ['PRCP',
                           'SNOW',
                           'SNWD',
                           'TMAX',
                           'TMIN',
                           'AWND',
                           'WSF2',
                           'WSF5']

    print 'Formatting categorical features...'
    for feature in categorical_features:
        df[feature] = map_cat_feature_to_target_range(df[feature])

    print 'Splitting into training/validation and test data...'
    df_train, df_test = train_test_split(df, test_size = 0.1, random_state=85645)

    print 'Scaling continuous features...'
    sc = StandardScaler()
    df_train.loc[:,continuous_features] = sc.fit_transform(df_train[continuous_features])
    df_test.loc[:,continuous_features] = sc.transform(df_test[continuous_features])

    print 'Saving train/test data...'
    train_path = os.path.join(project_dir,'data/processed/train.csv.gz')
    df_train.to_csv(train_path, index=True, compression='gzip')
    test_path = os.path.join(project_dir,'data/processed/test.csv.gz')
    df_test.to_csv(test_path, index=True, compression='gzip')

def map_cat_feature_to_target_range(series):
    vals = series.unique()
    mapping = dict(zip(vals,range(len(vals))))
    return series.apply(lambda x: mapping[x])
