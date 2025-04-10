import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from statsmodels.stats.weightstats import ztest
import os

# Set up database connection
connection_string = os.getenv('OUTPUT_STRING')
engine = create_engine(connection_string)

# Load execution time data
sequential_df = pd.read_sql("SELECT * FROM topsis_run_times", con=engine)
parallel_df = pd.read_sql("SELECT * FROM parallel_topsis_run_times", con=engine)

# Extract execution times
seq_times = sequential_df['ExecutionTimeSeconds']
par_times = parallel_df['ExecutionTimeSeconds']

# Compute statistics
sequential_avg = seq_times.mean()
sequential_total = seq_times.sum()

parallel_avg = par_times.mean()
parallel_total = par_times.sum()

# Calculate percentage decrease in average execution time
percentage_decrease = ((sequential_avg - parallel_avg) / sequential_avg) * 100

print(f"\n💡 Percentage decrease in average execution time (Parallel vs Sequential): {percentage_decrease:.2f}%")

# Print total times
print(f"Sequential TOPSIS total time for 50 runs: {sequential_total:.2f} seconds")
print(f"Parallel TOPSIS total time for 50 runs: {parallel_total:.2f} seconds")

# Perform Z-test
z_stat, p_value = ztest(seq_times, par_times, alternative='two-sided')
print("\nZ-Test Results:")
print(f"Z-statistic: {z_stat}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("✅ The difference in execution times is statistically significant (p < 0.05).")
else:
    print("ℹ️ The difference in execution times is NOT statistically significant (p ≥ 0.05).")

# Plot average execution times
labels = ['Sequential', 'Parallel']
avg_times = [sequential_avg, parallel_avg]

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, avg_times, color=['skyblue', 'lightgreen'])
plt.ylabel('Average Execution Time (s)')
plt.title('Average Execution Time Comparison (50 Runs)')
plt.ylim(0, max(avg_times) + 20)

# Annotate bar values
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.2f}', ha='center')

plt.tight_layout()
plt.show()
