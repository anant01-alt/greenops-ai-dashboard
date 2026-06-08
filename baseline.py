import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("data/cloud_usage_dataset.xlsx")

# Remove rows with missing values
print("Rows before cleaning:", len(df))
df = df.dropna()
print("Rows after cleaning:", len(df))

# Basic exploration
print("\nShape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nFirst 10 Rows:")
print(df.head(10))

print("\nNull Values:")
print(df.isnull().sum())

# Cost analysis
print("\nTotal Cost:")
print(df["cost_usd"].sum())

print("\nAverage Daily Cost:")
print(df.groupby("date")["cost_usd"].sum().mean())

# CO2e calculation
df["co2e_kg"] = (
    (df["cpu_hours"] * 0.0002)
    + (df["storage_gb"] * 0.00006 / 30)
    + (df["data_transfer_gb"] * 0.001)
)

print("\nTotal CO2e:")
print(df["co2e_kg"].sum())

print("\nCO2e by Service Type:")
print(df.groupby("service_type")["co2e_kg"].sum())

print("\nCO2e by Team:")
print(df.groupby("team")["co2e_kg"].sum())

# Daily CO2e line chart
daily_co2e = df.groupby("date")["co2e_kg"].sum()

plt.figure(figsize=(10, 5))
daily_co2e.plot()
plt.title("Daily CO2e")
plt.xlabel("Date")
plt.ylabel("CO2e (kg)")
plt.tight_layout()
plt.savefig("data/daily_co2e.png")
plt.close()

# CO2e by region bar chart
region_co2e = df.groupby("region")["co2e_kg"].sum()

plt.figure(figsize=(8, 5))
region_co2e.plot(kind="bar")
plt.title("CO2e by Region")
plt.xlabel("Region")
plt.ylabel("CO2e (kg)")
plt.tight_layout()
plt.savefig("data/co2e_by_region.png")
plt.close()

print("\nCharts saved successfully!")

# Save enriched dataset
df.to_csv("data/cloud_usage_enriched.csv", index=False)

print("Enriched dataset saved!")