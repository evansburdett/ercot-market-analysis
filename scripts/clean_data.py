import pandas as pd

# 1. Load Data
df = pd.read_csv("data/dart_hourly_unified.csv")

# 2. Rename & Sort
df.rename(columns={"Unnamed: 0": "Datetime"}, inplace=True)
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.sort_values("Datetime", inplace=True)

# 3. Create "Forecast Error" Variables
# Interpretation: Positive = More wind than predicted. Negative = Less wind than predicted.
df["wind_error"] = df["wind_gen"] - df["wind_cophsl"]

# 4. Create "DART Spread" Variables (Target Variable)
# Interpretation: Spread = Day Ahead - Real Time
# If Spread > 0: DA was overpriced (Longs win). If Spread < 0: RT spiked (Shorts win).
df["spread_north"] = df["dam_hub_HB_NORTH"] - df["rtm_hub_HB_NORTH"]
df["spread_west"] = df["dam_hub_HB_WEST"] - df["rtm_hub_HB_WEST"]
df["spread_south"] = df["dam_hub_HB_SOUTH"] - df["rtm_hub_HB_SOUTH"]

# 5. Drop Rows with Missing Critical Data
# We drop rows where we lack price data or wind forecast data
clean_df = df.dropna(subset=["wind_error", "spread_north", "spread_west"])

# 6. Select Final Columns for Analysis
final_df = clean_df[
    [
        "Datetime",
        "hour",
        "is_weekend",
        "wind_error",
        "spread_north",
        "spread_west",
        "spread_south",
    ]
]

# 7. Export
final_df.to_csv("data/evan_project_data.csv", index=False)
print(f"Cleaned dataset saved with {len(final_df)} observations.")
