# 1) Make FRED data
# ===========================================================
make_fred = False # Whether to build the FRED dataset

# 2) Run Rolling Nowcasting
# ===========================================================
train_models = True
model_type = "XGBoost"  # Choose from "XGBoost", "RandomForest", "OLS", "MLP"
lags_to_test = list(range(-2, 3))
target = "gdpc1"
gdp_lag = 1
start_train = "1947-01-01"
end_train = "2005-02-01"
start_val = "2005-03-01"
end_val = "2010-03-01"