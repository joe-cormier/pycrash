Pycrash
==============================

A comprehensive analytical tool for accident reconstruction

## Process

#### Single Vehicle Motion
1. Initial position is chosen and input conditions determines output

#### Impact Simulation
#### Impact Point / Vector
Type of impact definition determined by model used.  
1. choose initial conditions for vehicles and run simulations
2. Use simulations to determine impact location or predefine if known.
    + impact point is defined as a vector, point, normal/tangent vectors on Vehicle 1
    + impact edge defined for Vehicle 2


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Input files for model (may create separate directories for each project)
    │
    ├── docs               <- documentation, tutorials, examples
    │
    ├── notebooks          <- Jupyter notebooks for running various project types
    │
    ├── references         <- published work
    │
    ├── reports            <- output generate from simulations
    │   └── project        <- separate directory for each project
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project - need separate directories?
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
    │       └── visualize.py



--------
