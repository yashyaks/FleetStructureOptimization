from scipy import stats

import os
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("OUTPUT_STRING")
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

df = fetch_data('topsis_50_ci_stats')
# Define CI function
def mean_ci(mean, sd, n, conf=0.95):
    alpha = 1 - conf
    dfree = n - 1
    tcrit = stats.t.ppf(1 - alpha / 2, dfree)
    se = sd / np.sqrt(n)
    return mean - tcrit * se, mean + tcrit * se

# Assuming you have the same number of samples per year, e.g., n = 30
n = 50  # change this if you know the actual per-year sample count

# Compute CIs for TotalCost
df['TotalCost_CI_lower'], df['TotalCost_CI_upper'] = zip(*df.apply(
    lambda row: mean_ci(row['TotalCost_mean'], row['TotalCost_std'], n), axis=1))

# If you also have Carbon Emissions in same CSV:
if 'TotalCarbonEmissions_mean' in df.columns and 'TotalCarbonEmissions_std' in df.columns:
    df['TotalCarbonEmissions_CI_lower'], df['TotalCarbonEmissions_CI_upper'] = zip(*df.apply(
        lambda row: mean_ci(row['TotalCarbonEmissions_mean'], row['TotalCarbonEmissions_std'], n), axis=1))

# Save results
df.to_csv("summary_with_CI_topsis.csv", index=False)

print(df.head())