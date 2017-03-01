import numpy as np
import pandas as pd
import pickle
import os

#Models
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LinearRegression


baseline_features = ['t','cos_t','sin_t']
target = 'Trip Count'

def make_baseline_model(df, features, target):
    """ Learns baseline linear model on training dataframe.

        Args:
            - df: Pandas Dataframe (train.csv.gz)
            - features: List of features for baseline model
            - target: target for model

        Returns:
            - lr: LinearRegression baseline model
    """
    lr = LinearRegression()
    lr.fit(df[baseline_features],df[target])
    return lr

def learn_EN_model(df, baseline_features, target):
    """ Uses 5-fold CV to learn elastic net regularized model
        on training dataframe.

        Args:
            - df: Pandas Dataframe (train.csv.gz)
            - features: List of features for baseline model.
                        Note this features are not effectively
                        regularized, since they are scaled prior
                        to fitting.
            - target: target for model

        Returns:
            - en: ElasticNet model (note also pickled and
                  saved for later use.
    """
    for feature in baseline_features:
        df[feature] = df[feature]*1e6

    df = df.join(pd.get_dummies(df['Day of Week'], prefix='day',drop_first=False))
    df = df.drop('Day of Week', axis=1)
    df = df.join(pd.get_dummies(df['Month'], prefix='month',drop_first=False))
    df = df.drop('Month', axis=1)


    with open(os.path.join(project_dir,'models/GBR.pkl'), 'wb') as outfile:
        pickle.dump(EN_grid_search, outfile)

if __name__ == '__main__':
    #project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    #main(project_dir)
    print 'Not calling main()- note the models are trained using PySpark.'
