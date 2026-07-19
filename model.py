

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import joblib


df_sale = pd.read_csv("cleaned_apartments_sale.csv") 
df_rent = pd.read_csv("cleaned_apartments_rent.csv")  


categorical_cols = ['ville', 'secteur']

encoders_sale = {}
encoders_rent = {}

for col in categorical_cols:
    le_sale = LabelEncoder()
    df_sale[col] = le_sale.fit_transform(df_sale[col])
    encoders_sale[col] = le_sale
    
    le_rent = LabelEncoder()
    df_rent[col] = le_rent.fit_transform(df_rent[col])
    encoders_rent[col] = le_rent

X_sale = df_sale.drop(columns=['prix', 'prix_m2'])
y_sale = df_sale['prix']

X_rent = df_rent.drop(columns=['prix', 'prix_m2'])
y_rent = df_rent['prix']



X_train_sale, X_test_sale, y_train_sale, y_test_sale = train_test_split(
    X_sale, y_sale, test_size=0.2, random_state=42)

X_train_rent, X_test_rent, y_train_rent, y_test_rent = train_test_split(
    X_rent, y_rent, test_size=0.2, random_state=42)


xgb_sale = xgb.XGBRegressor(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb_sale.fit(X_train_sale, y_train_sale)
y_pred_sale = xgb_sale.predict(X_test_sale)

rmse_sale = np.sqrt(mean_squared_error(y_test_sale, y_pred_sale))
mae_sale = mean_absolute_error(y_test_sale, y_pred_sale)
r2_sale = r2_score(y_test_sale, y_pred_sale)

print(f"Sale | XGBoost → RMSE: {rmse_sale:.2f}, MAE: {mae_sale:.2f}, R²: {r2_sale:.2f}")



lr_rent = LinearRegression()
lr_rent.fit(X_train_rent, y_train_rent)
y_pred_rent = lr_rent.predict(X_test_rent)

rmse_rent = np.sqrt(mean_squared_error(y_test_rent, y_pred_rent))
mae_rent = mean_absolute_error(y_test_rent, y_pred_rent)
r2_rent = r2_score(y_test_rent, y_pred_rent)

print(f"Rent | Linear Regression → RMSE: {rmse_rent:.2f}, MAE: {mae_rent:.2f}, R²: {r2_rent:.2f}")


joblib.dump(xgb_sale, "xgboost_sale_model.pkl")
joblib.dump(lr_rent, "linear_regression_rent_model.pkl")
joblib.dump(encoders_sale, "encoders_sale.pkl")
joblib.dump(encoders_rent, "encoders_rent.pkl")

print("Models saved successfully!")
