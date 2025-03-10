import pandas as pd
from scipy.stats import ttest_ind

# Read data from CSV files
topsis_df = pd.read_csv('data/output/tradeoff/topsis/multiobjective_summary.csv')
no_topsis_df = pd.read_csv('data/output/tradeoff/notopsis/multiobjective_summary.csv')

# Merge data on the 'Year' column
df = pd.merge(topsis_df, no_topsis_df, on='Year', suffixes=('_Topsis', '_NoTopsis'))

# Apply t-test
cost_ttest = ttest_ind(df['TotalCost_Topsis'], df['TotalCost_NoTopsis'])
ce_ttest = ttest_ind(df['TotalCarbonEmissions_Topsis'], df['TotalCarbonEmissions_NoTopsis'])

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
