import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

# Load dataset
df = pd.read_csv("data/cloud_usage_enriched.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Aggregate daily CO2e
daily = df.groupby("date")["co2e_kg"].sum().reset_index()

# Lag features
daily["lag_7"] = daily["co2e_kg"].shift(7)
daily["lag_14"] = daily["co2e_kg"].shift(14)

# Rolling mean
daily["rolling_7"] = daily["co2e_kg"].rolling(7).mean()

# Day of week
daily["dow"] = daily["date"].dt.dayofweek

# Remove NaNs
daily = daily.dropna()

# Train/Test Split
train = daily.iloc[:-30]
test = daily.iloc[-30:]

features = ["lag_7", "lag_14", "rolling_7", "dow"]

X_train = train[features]
y_train = train["co2e_kg"]

X_test = test[features]
y_test = test["co2e_kg"]

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# RMSE
rmse = root_mean_squared_error(y_test, y_pred)

print("RMSE:", rmse)

# Plot
plt.figure(figsize=(10,5))
plt.plot(test["date"], y_test, label="Actual")
plt.plot(test["date"], y_pred, label="Predicted")
plt.legend()
plt.title("Actual vs Predicted CO2e")
plt.tight_layout()

plt.savefig("model/forecast_plot.png")
plt.close()

# Save model
joblib.dump(model, "model/co2e_model.pkl")

print("Model saved!")
print("Forecast plot saved!")