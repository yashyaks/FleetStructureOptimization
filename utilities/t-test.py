import os
import pandas as pd
from scipy.stats import ttest_ind
from sqlalchemy import create_engine

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Fetch data from database tables
topsis_df = fetch_data('topsis_multiobjective_summary')
no_topsis_df = fetch_data('notopsis_multiobjective_summary')

# Apply t-test
cost_ttest = ttest_ind(topsis_df['TotalCost'], no_topsis_df['TotalCost'])
ce_ttest = ttest_ind(topsis_df['TotalCarbonEmissions'], no_topsis_df['TotalCarbonEmissions'])

# Print results
print("T-test for Cost:", cost_ttest)
print("T-test for Carbon Emissions:", ce_ttest)

# Interpretation
if cost_ttest.pvalue < 0.05:
    print("Cost difference is statistically significant.")
else:
    print("Cost difference is not statistically significant.")

if ce_ttest.pvalue < 0.05:
    print("Carbon Emissions difference is statistically significant.")
else:
    print("Carbon Emissions difference is not statistically significant.")