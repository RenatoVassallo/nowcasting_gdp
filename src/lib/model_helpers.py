import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def train_model(model_type, x_train, y_train):
    
    if model_type == "XGBoost":
        model = XGBRegressor(
            n_estimators = 500,
            eta = 0.1,
            max_depth = 3,
            reg_lambda = 1,
            reg_alpha = 0)
    
    elif model_type == "RandomForest":
        model = RandomForestRegressor(
            n_estimators = 100, 
            criterion = "squared_error", 
            max_depth = None, 
            min_samples_split = 0.01, 
            min_samples_leaf = 0.01,
            max_features = "sqrt",
            bootstrap = False)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(x_train, y_train)
    return model

def evaluate_models(models, x_test):
    preds = [model.predict(x_test)[0] for model in models]
    return np.nanmean(preds)