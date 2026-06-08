from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI(title="GreenOps API")

# Load dataset
df = pd.read_csv("data/cloud_usage_enriched.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Load trained model
model = joblib.load("model/co2e_model.pkl")


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/metrics/summary")
def metrics_summary():
    """Summary metrics"""

    total_co2e = float(df["co2e_kg"].sum())
    total_cost = float(df["cost_usd"].sum())

    top_team = (
        df.groupby("team")["co2e_kg"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("region")["co2e_kg"]
        .sum()
        .idxmax()
    )

    return {
        "total_co2e": total_co2e,
        "total_cost": total_cost,
        "top_team": top_team,
        "top_region": top_region,
    }


@app.get("/metrics/daily")
def metrics_daily():
    """Daily CO2e values"""

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    daily["date"] = daily["date"].astype(str)

    return daily.to_dict(orient="records")


@app.get("/forecast")
def forecast():
    """30-day forecast"""

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    # Same features used during training
    daily["lag_7"] = daily["co2e_kg"].shift(7)
    daily["lag_14"] = daily["co2e_kg"].shift(14)
    daily["rolling_7"] = daily["co2e_kg"].rolling(7).mean()
    daily["dow"] = daily["date"].dt.dayofweek

    daily = daily.dropna()

    latest = daily.tail(30)

    X = latest[["lag_7", "lag_14", "rolling_7", "dow"]]

    preds = model.predict(X)

    return {
        "forecast": preds.tolist()
    }