import os
import pandas as pd
import numpy as np
from config.params import *
from config.paths import dir_input_raw, dir_input_cleaned, dir_output
from lib.data_helpers import gen_lagged_data, flatten_data, mean_fill_dataset
from lib.model_helpers import train_model, evaluate_models

def execute():
    # Load data
    metadata = pd.read_csv(os.path.join(dir_input_raw, "meta_data.csv"))
    data     = pd.read_csv(os.path.join(dir_input_cleaned, "data_tf.csv"), parse_dates=["date"])
    data     = data.set_index("date").asfreq("MS")

    # Prepare datasets
    data_train = data[start_train: end_train]
    data_val   = data[start_val: end_val]
    data_train_val = pd.concat([data_train, data_val])     
    data_train_val.reset_index(inplace=True)
    
    dates         = data_val.dropna().index.strftime("%Y-%m-%d").to_list()  # Quarterly dates
    actual_values = data_val[target].dropna().values                        # Quarterly GDP values      

    # Initialize predictions
    pred_dict = {lag: [] for lag in lags_to_test}

    for date in dates:
        # Generate training data
        train = data_train_val.loc[data_train_val.date <= str(pd.to_datetime(date) - pd.tseries.offsets.DateOffset(months=3))[:10],:] 
        transformed_train = flatten_data(mean_fill_dataset(train, train), target, 4)
        transformed_train = transformed_train.loc[transformed_train.date.dt.month.isin([3,6,9,12]),:].dropna(axis=0, how="any").reset_index(drop=True)
        x_train = transformed_train.drop(columns=["date", target])
        y_train = transformed_train[target]

        # Train models
        models = [train_model(model_type, x_train, y_train) for _ in range(10)]

        for lag in lags_to_test:
            lagged_test = gen_lagged_data(metadata, data_train_val, date, lag)
            transformed_test = flatten_data(mean_fill_dataset(train, lagged_test), target, 4)
            x_test = transformed_test.loc[transformed_test["date"] == date].drop(["date", target], axis=1)

            pred = evaluate_models(models, x_test)
            pred_dict[lag].append(pred)

    # Save results
    pd.DataFrame(pred_dict).to_csv(os.path.join(dir_output, f"predictions_{model_type}.csv"), index=False)