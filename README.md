two_sigma_challenge_final
==============================

Two Sigma Data Clinic Data Test

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets
    │   ├── interim      <- Intermediate processed data.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models and model summaries
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
    │   │   └── get_raw_data.py
    │   │   └── make_dataset.py
    │   │   └── make_train_test_splits.py
    │   │   └── process_raw_trip_data.py
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

1. Run `make data` to get and clean the raw 2016 citibike trip data, get and clean the NOAA data through their API, then merge and save the train/test splits for these datas.
2. Run `make models` to train, pickle, and save models. Note the baseline (simple regression) model is not pickled since the run time is trivial.
3. Run `make plots` to make visuals for report and get training R^2 values.
4. Run `make test_scores` to get final test set R^2 scores.
5. Run `make report` to make final report.
....


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
