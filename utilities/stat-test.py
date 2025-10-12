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

# Fetch data
topsis_df = fetch_data('topsis_50_multiobjective_summary_avg')
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