import os
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Fetch data (3 samples)
data1 = fetch_data('topsis_50_multiobjective_summary_avg')
data2 = fetch_data('topsis_100_multiobjective_summary_avg')
data3 = fetch_data('topsis_250_multiobjective_summary_avg')

def summarize_and_compare_3(A, B, C, metric_name="Metric"):
    """Compute descriptive stats, ANOVA, Kruskal-Wallis, and post-hoc Tukey HSD."""
    groups = [A, B, C]
    names = ["Data1", "Data2", "Data3"]

    print(f"\n=== {metric_name} ===")

    # Descriptive stats
    for g, name in zip(groups, names):
        m, s, n = g.mean(), g.std(ddof=1), len(g)
        tval = stats.t.ppf(1 - 0.025, n - 1)
        ci = (m - tval * s / np.sqrt(n), m + tval * s / np.sqrt(n))
        print(f"{name}: mean±sd = {m:.2f} ± {s:.2f}, 95% CI = {ci}")

    # ANOVA
    f_stat, p_val = stats.f_oneway(A, B, C)
    print(f"\nOne-way ANOVA: F = {f_stat:.3f}, p = {p_val:.4f}")

    # Eta squared effect size
    all_data = np.concatenate([A, B, C])
    grand_mean = np.mean(all_data)
    ssb = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
    sst = sum(((x - grand_mean)**2).sum() for x in groups)
    eta_sq = ssb / sst
    print(f"Effect size (eta²): {eta_sq:.3f}")

    if p_val < 0.05:
        print("--> Statistically significant difference detected among groups.")

        # Tukey post-hoc test
        combined = np.concatenate([A, B, C])
        labels = (["Data1"]*len(A)) + (["Data2"]*len(B)) + (["Data3"]*len(C))
        tukey = pairwise_tukeyhsd(endog=combined, groups=labels, alpha=0.05)
        print("\nTukey HSD post-hoc test:")
        print(tukey.summary())
    else:
        print("--> No statistically significant difference among groups.")

    # Kruskal-Wallis (non-parametric alternative)
    h_stat, p_kw = stats.kruskal(A, B, C)
    print(f"Kruskal–Wallis test: H = {h_stat:.3f}, p = {p_kw:.4f}")

# Run for both metrics
summarize_and_compare_3(data1['TotalCost'].values,
                        data2['TotalCost'].values,
                        data3['TotalCost'].values,
                        "Total Cost")

summarize_and_compare_3(data1['TotalCarbonEmissions'].values, data2['TotalCarbonEmissions'].values, data3['TotalCarbonEmissions'].values, "Total Carbon Emissions")