# import os
# import matplotlib.pyplot as plt
# import pandas as pd
# from sqlalchemy import create_engine

# # Fetch DB_URL from environment variable
# DB_URL = os.getenv("OUTPUT_STRING")

# # Create SQLAlchemy engine
# engine = create_engine(DB_URL)

# def fetch_data(table_name):
#     """Fetches data from a MySQL table using SQLAlchemy."""
#     query = f"SELECT * FROM {table_name}"
#     return pd.read_sql(query, engine)

# def plot_and_analyze_fleet_data(table_no_topsis, table_topsis, table_demand):
#     """
#     Plots cost and emissions comparisons using data from MySQL tables.
#     Also calculates and prints the total sums and percentage differences.
#     """
#     data_no_topsis = fetch_data(table_no_topsis)
#     data_topsis = fetch_data(table_topsis)
    
#     years = data_no_topsis['Year']
    
#     # Calculate total sums
#     total_emissions_no_topsis = data_no_topsis['TotalCarbonEmissions'].sum()
#     total_emissions_topsis = data_topsis['TotalCarbonEmissions'].sum()
#     total_cost_no_topsis = data_no_topsis['TotalCost'].sum()
#     total_cost_topsis = data_topsis['TotalCost'].sum()
    
#     # Calculate percentage differences
#     emissions_diff_percent = ((total_emissions_topsis - total_emissions_no_topsis) / total_emissions_no_topsis) * 100
#     cost_diff_percent = ((total_cost_topsis - total_cost_no_topsis) / total_cost_no_topsis) * 100
    
#     # Print the results
#     print("\n--- SUMMARY OF RESULTS ---")
#     print(f"Total Carbon Emissions (No TOPSIS): {total_emissions_no_topsis:.2f} kg CO2")
#     print(f"Total Carbon Emissions (With TOPSIS): {total_emissions_topsis:.2f} kg CO2")
#     print(f"Percentage Difference in Emissions: {emissions_diff_percent:.2f}%")
#     print(f"\nTotal Cost (No TOPSIS): {total_cost_no_topsis:.2f}")
#     print(f"Total Cost (With TOPSIS): {total_cost_topsis:.2f}")
#     print(f"Percentage Difference in Cost: {cost_diff_percent:.2f}%")
#     print("------------------------\n")
    
#     # Carbon Emissions Plot
#     plt.figure(figsize=(10, 6))
#     plt.plot(years, data_no_topsis['TotalCarbonEmissions'], 'o-', label='Emissions (No TOPSIS)', color='red')
#     plt.plot(years, data_topsis['TotalCarbonEmissions'], 's-', label='Emissions (With TOPSIS)', color='green')
#     plt.xlabel('Year', fontsize=14)
#     plt.ylabel('Total Carbon Emissions (kg CO2)', fontsize=14)
#     plt.title('Comparison of Total Emissions Over Years', fontsize=16)
#     plt.legend(fontsize=12)
#     plt.grid(True)
#     plt.show()

#     # Cost Plot
#     plt.figure(figsize=(10, 6))
#     plt.plot(years, data_no_topsis['TotalCost'], 'o-', label='Cost (No TOPSIS)', color='red')
#     plt.plot(years, data_topsis['TotalCost'], 's-', label='Cost (With TOPSIS)', color='green')
#     plt.xlabel('Year', fontsize=14)
#     plt.ylabel('Total Cost', fontsize=14)
#     plt.title('Comparison of Total Cost Over Years', fontsize=16)
#     plt.legend(fontsize=12)
#     plt.grid(True)
#     plt.show()

# # Example Usage
# plot_and_analyze_fleet_data('topsis_multiobjective_summary_avg', 'parallel_topsis_multiobjective_summary_avg', 'demand')


import os
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")
DB_URL = 'mysql+pymysql://root:mysqlrootpassword@127.0.0.1:3306/output?ssl_disabled=true'
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Fetch data
topsis_df = fetch_data('topsis_multiobjective_summary_avg')
no_topsis_df = fetch_data('notopsis_multiobjective_summary_avg')

# Extract metrics of interest
A_cost = topsis_df['TotalCost'].values
B_cost = no_topsis_df['TotalCost'].values
A_ce = topsis_df['TotalCarbonEmissions'].values
B_ce = no_topsis_df['TotalCarbonEmissions'].values

def summarize_and_compare(A, B, metric_name="Metric"):
    """Compute descriptive stats, CIs, effect sizes, t-test, and Mann–Whitney."""
    mA, sA, nA = A.mean(), A.std(ddof=1), len(A)
    mB, sB, nB = B.mean(), B.std(ddof=1), len(B)

    # 95% t-based CI
    alpha = 0.05
    tA = stats.t.ppf(1 - alpha/2, nA - 1)
    ciA = (mA - tA * sA / np.sqrt(nA), mA + tA * sA / np.sqrt(nA))

    tB = stats.t.ppf(1 - alpha/2, nB - 1)
    ciB = (mB - tB * sB / np.sqrt(nB), mB + tB * sB / np.sqrt(nB))

    # Welch's t-test
    t_stat, p_val = stats.ttest_ind(A, B, equal_var=False)

    # Mann-Whitney U test
    u_stat, p_mw = stats.mannwhitneyu(A, B, alternative='two-sided')

    # Cohen’s d
    s_pooled = np.sqrt(((nA - 1) * sA*2 + (nB - 1) * sB*2) / (nA + nB - 2))
    cohens_d = (mA - mB) / s_pooled

    print(f"\n=== {metric_name} ===")
    print(f"Topsis mean±sd: {mA:.2f} ± {sA:.2f}, 95% CI: {ciA}")
    print(f"No-Topsis mean±sd: {mB:.2f} ± {sB:.2f}, 95% CI: {ciB}")
    print(f"Welch t-test: t={t_stat:.3f}, p={p_val:.4f}")
    print(f"Mann-Whitney U: U={u_stat:.2f}, p={p_mw:.4f}")
    print(f"Cohen's d (effect size): {cohens_d:.3f}")

    if p_val < 0.05:
        print(f"--> Statistically significant difference in {metric_name}.")
    else:
        print(f"--> No statistically significant difference in {metric_name}.")

# Run comparisons
summarize_and_compare(A_cost, B_cost, "Total Cost")
summarize_and_compare(A_ce, B_ce, "Total Carbon Emissions")