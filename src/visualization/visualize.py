import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from ..models import train_model
import os
import pickle

def main(project_dir):
    ''' Main function to make plots for report.
        Makes two plots- one for baseline and one for EN model

        Args:
            -parent_dir: project directory

        Returns:
            -None: saves plots in reports/figures/
    '''

    df = pd.read_csv(os.path.join(project_dir, 'data/processed/train.csv.gz'), parse_dates=[0],index_col=0)

    df = df.sort_index()

    baseline_features = ['t','cos_t','sin_t']
    target = 'Trip Count'
    lr = train_model.learn_baseline_model(df, baseline_features, target)

    make_plot(lr, df, baseline_features, target, 'baseline', project_dir)

    with open(os.path.join(project_dir, 'models/EN.pkl'),'rb') as infile:
        EN = pickle.load(infile)

    df = train_model.EN_preprocess(df)

    features = list(set(df.columns) - set(['Trip Count']))

    make_plot(EN, df, features, target, 'final', project_dir)

def make_plot(model, df, features, target, name, project_dir):
    """ Makes plots for the final report. Also writes training
        scores to models/scores/

        Args:
            - model: model with a .predict method
            - df: pandas dataframe with columns in features, and target
            - features: features in model
            - name: string describing model ('baseline' or 'final')

        Returns:
            -None: Saves plots in reports/figures
    """

    predictions = model.predict(df[features])
    score = model.score(df[features],df[target])

    if name == 'baseline':
        outfile_name = os.path.join(project_dir,'models/scores/lr_train_r2.txt')
    elif name == 'final':
        outfile_name = os.path.join(project_dir,'models/scores/EN_train_r2.txt')

    with open(outfile_name, 'w+') as f:
        f.write(str(score))

    f, axarr = plt.subplots(2, sharex=True, figsize=(12,12))
    axarr[0].plot(df.index, predictions, color='k', label='Predicted Trip Count- R^2 = {0:.3f}'.format(score))
    axarr[0].plot(df.index,df['Trip Count'], color='b')
    axarr[0].set_ylabel('Trip Counts')
    axarr[0].set_title('Trip counts with {} model'.format(name))
    axarr[0].legend(loc='upper left')
    axarr[1].plot(df.index,df['Trip Count'] - predictions, color='g', label='Residual from {} model'.format(name))
    axarr[1].set_ylabel('Trip Counts')
    axarr[1].set_xlabel('Date')
    axarr[1].set_title('Residuals from {} model'.format(name))
    axarr[1].legend(loc="upper left")
    axarr[1].set_ylim(-40000,40000)

    fig_name = os.path.join(project_dir, 'reports/figures/{}_plot.png'.format(name))
    f.savefig(fig_name,dpi=f.dpi)

if __name__ == '__main__':
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    plt.rc('text', usetex=True)
    main(project_dir)
