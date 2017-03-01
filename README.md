two_sigma_challenge
==============================

Two Sigma Data Clinic Data Test

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks for exploration and development.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py

Reproducing Project
------------

1. Run `make data` to get and clean the raw 2016 citibike trip data, and merge with cleaned NOAA data. Note the NOAA data was (unfortunately) downloaded through a GUI, and its provenance is given in "Order History | Climate Data Online (CDO) | National Climatic Data Center (NCDC).pdf".
2. Run `make models` to train, pickle, and save models. Note for this project, two models were quasi-optimized using grid search over a fixed validation set, specifically an elastic net (l1/l2 regularized linear model) and a Gradient Boosted Regression model (using least squares (l2) loss function). Note we say "quasi-optimized" because additional the hyperparameter searches could have been extended.
3. Run `make model-performance-visuals` to make learning curves for both models. Plots are saved in reports/figures/. TODO
4. Run `make predictions` to make final model, and get final test error.
5. Run `make report` to make final report.
....


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
