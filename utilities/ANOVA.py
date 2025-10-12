################ ANOVA ####################
import os
import pandas as pd
from scipy.stats import f_oneway
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Fetch data from database tables
data1 = fetch_data('topsis_50_multiobjective_summary_avg')
data2 = fetch_data('topsis_100_multiobjective_summary_avg')
data3 = fetch_data('topsis_250_multiobjective_summary_avg')   # third sample

# Apply one-way ANOVA (for 3 samples)
cost_anova = f_oneway(data1['TotalCost'], data2['TotalCost'], data3['TotalCost'])
ce_anova = f_oneway(data1['TotalCarbonEmissions'], data2['TotalCarbonEmissions'], data3['TotalCarbonEmissions'])

# Print results
print("ANOVA for Cost:", cost_anova)
print("ANOVA for Carbon Emissions:", ce_anova)

# Interpretation
if cost_anova.pvalue < 0.05:
    print("Cost difference is statistically significant among the three groups.")
else:
    print("Cost difference is not statistically significant among the three groups.")

if ce_anova.pvalue < 0.05:
    print("Carbon Emissions difference is statistically significant among the three groups.")
else:
    print("Carbon Emissions difference is not statistically significant among the three groups.")