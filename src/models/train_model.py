import numpy as np
import pandas as pd
import pickle
import os

#Models
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LinearRegression

def learn_baseline_model(df, features, target):
    """ Learns baseline linear model on training dataframe.

        Args:
            - df: Pandas Dataframe (train.csv.gz)
            - features: List of features for baseline model
            - target: target for model

        Returns:
            - lr: LinearRegression baseline model
    """
    lr = LinearRegression()
    lr.fit(df[features],df[target])
    return lr

def learn_EN_model(df, baseline_features, target, project_dir):
    """ Uses 5-fold CV to learn elastic net regularized model
        on training dataframe.

        Args:
            - df: Pandas Dataframe (train.csv.gz)
            - features: List of features for baseline model.
                        Note this features are not effectively
                        regularized, since they are scaled prior
                        to fitting.
            - target: target for model
            - project_dir: directory for project (os.path)

        Returns:
            - en: ElasticNet model (note also pickled and
                  saved for later use.
    """

    df = EN_preprocess(df)

    l1_ratio = np.arange(0,1.1,.1)
    alphas = np.logspace(-3,4,8)
    cv = 5
    verbose = 2
    fit_intercept = False #Keep all dummies

    EN = ElasticNetCV(l1_ratio=l1_ratio,
                  alphas=alphas,
                  cv=cv,
                  selection='random',
                  random_state=34631)

    features = list(set(df.columns) - set(['Trip Count']))

    EN.fit(df[features], df['Trip Count'])

    with open(os.path.join(project_dir,'models/EN.pkl'), 'wb') as outfile:
        pickle.dump(EN, outfile)

    return EN

def EN_preprocess(df):
    """ Helper function to preprocess features for EN model

        Args:
            df: Dataframe with baseline features plus 'Day of Week'
                and 'Month'

        Returns:
            df: Processed df
    """
    df['t'] = df['t']/df['t'].max()

    df = df.join(pd.get_dummies(df['Day of Week'], prefix='day',drop_first=False))
    df = df.drop('Day of Week', axis=1)
    df = df.join(pd.get_dummies(df['Month'], prefix='month',drop_first=False))
    df = df.drop('Month', axis=1)

    return df

if __name__ == '__main__':

    baseline_features = ['t','cos_t','sin_t']
    target = 'Trip Count'

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    df = pd.read_csv(os.path.join(project_dir, 'data/processed/train.csv.gz'), parse_dates=[0],index_col=0)
    learn_EN_model(df, baseline_features, target, project_dir)

