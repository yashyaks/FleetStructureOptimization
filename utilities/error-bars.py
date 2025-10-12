import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("OUTPUT_STRING")
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Fetch data from both tables
df_topsis = fetch_data('topsis_50_multiobjective_summary_all_runs')
df_vanilla = fetch_data('notopsis_multiobjective_summary_all_runs')

# Calculate mean and standard deviation for each year - TOPSIS
yearly_stats_topsis = df_topsis.groupby('Year').agg({
    'TotalCost': ['mean', 'std'],
    'TotalCarbonEmissions': ['mean', 'std']
}).reset_index()

# Calculate mean and standard deviation for each year - Vanilla
yearly_stats_vanilla = df_vanilla.groupby('Year').agg({
    'TotalCost': ['mean', 'std'],
    'TotalCarbonEmissions': ['mean', 'std']
}).reset_index()

# Flatten column names
yearly_stats_topsis.columns = ['Year', 'TotalCost_mean', 'TotalCost_std', 
                                'TotalCarbonEmissions_mean', 'TotalCarbonEmissions_std']
yearly_stats_vanilla.columns = ['Year', 'TotalCost_mean', 'TotalCost_std', 
                                 'TotalCarbonEmissions_mean', 'TotalCarbonEmissions_std']

# ============================================================================
# PLOT 1: Total Cost Comparison
# ============================================================================
fig1, ax1 = plt.subplots(1, 1, figsize=(12, 6))

years = yearly_stats_topsis['Year'].values
x = np.arange(len(years))
width = 0.35

bars1 = ax1.bar(x - width/2, 
                yearly_stats_vanilla['TotalCost_mean'], 
                width,
                yerr=yearly_stats_vanilla['TotalCost_std'],
                capsize=5,
                alpha=0.8,
                color='steelblue',
                edgecolor='black',
                linewidth=1.2,
                label='Vanilla NSGA-II')

bars2 = ax1.bar(x + width/2, 
                yearly_stats_topsis['TotalCost_mean'], 
                width,
                yerr=yearly_stats_topsis['TotalCost_std'],
                capsize=5,
                alpha=0.8,
                color='coral',
                edgecolor='black',
                linewidth=1.2,
                label='TOPSIS Integrated NSGA-II')

ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Cost', fontsize=12, fontweight='bold')
ax1.set_title('Mean Total Cost Comparison: Vanilla vs TOPSIS Integrated NSGA-II', 
              fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(fontsize=11, loc='best')
ax1.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# ============================================================================
# PLOT 2: Total Carbon Emissions Comparison
# ============================================================================
fig2, ax2 = plt.subplots(1, 1, figsize=(12, 6))

bars3 = ax2.bar(x - width/2, 
                yearly_stats_vanilla['TotalCarbonEmissions_mean'], 
                width,
                yerr=yearly_stats_vanilla['TotalCarbonEmissions_std'],
                capsize=5,
                alpha=0.8,
                color='green',
                edgecolor='black',
                linewidth=1.2,
                label='Vanilla NSGA-II')

bars4 = ax2.bar(x + width/2, 
                yearly_stats_topsis['TotalCarbonEmissions_mean'], 
                width,
                yerr=yearly_stats_topsis['TotalCarbonEmissions_std'],
                capsize=5,
                alpha=0.8,
                color='orange',
                edgecolor='black',
                linewidth=1.2,
                label='TOPSIS Integrated NSGA-II')

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Carbon Emissions', fontsize=12, fontweight='bold')
ax2.set_title('Mean Total Carbon Emissions Comparison: Vanilla vs TOPSIS Integrated NSGA-II', 
              fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(years)
ax2.legend(fontsize=11, loc='best')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# Print summary statistics for comparison
print("=" * 80)
print("TOPSIS Integrated NSGA-II Statistics:")
print("=" * 80)
print(yearly_stats_topsis)
print("\n" + "=" * 80)
print("Vanilla NSGA-II Statistics:")
print("=" * 80)
print(yearly_stats_vanilla)