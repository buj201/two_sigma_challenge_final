import pandas as pd
import numpy as np
from ..models import train_model
import os
import pickle

def main(project_dir):
    """ Last script to run in modeling pipline. Gets test set scores.

        Args:
            -project_dir: Project directory

        Returns:
            -None: writes to disk for consumption in LaTeX report
    """

    train = pd.read_csv(os.path.join(project_dir, 'data/processed/train.csv.gz'), parse_dates=[0],index_col=0)

    test = pd.read_csv(os.path.join(project_dir, 'data/processed/test.csv.gz'), parse_dates=[0],index_col=0)

    baseline_features = ['t','cos_t','sin_t']
    target = 'Trip Count'
    lr = train_model.learn_baseline_model(train, baseline_features, target)

    lr_test_score = lr.score(test[baseline_features], test[target])

    with open(os.path.join(project_dir, 'models/EN.pkl'),'rb') as infile:
        EN = pickle.load(infile)

    test = train_model.EN_preprocess(test)

    features = list(set(test.columns) - set(['Trip Count']))

    EN_test_score = EN.score(test[features], test[target])

    with open(os.path.join(project_dir,'models/scores/lr_test_r2.txt'), 'w+') as f:
        f.write(str(lr_test_score))

    with open(os.path.join(project_dir,'models/scores/EN_test_r2.txt'), 'w+') as f:
        f.write(str(EN_test_score))

if __name__ == '__main__':
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    main(project_dir)
