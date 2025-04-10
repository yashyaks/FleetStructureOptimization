import pandas as pd
from main_tradeoff_topsis_parallelize import parallel_optimization
from utilities.my_sql_operations import MySQLOperations
import os
import time

def run_multiple_optimizations(n_runs=50):
    cost_weight, carbon_emissions_weight = 0.5, 0.5
    generations, population_size = 50, 100
    prev_years, min_year, max_year = 7, 2023, 2038

    sqlops = MySQLOperations()
    connection_string = os.getenv('OUTPUT_STRING')
    engine = sqlops.create_sqlalchemy_engine(connection_string)

    # DataFrame to accumulate summary results
    all_runs_df = pd.DataFrame()

    # DataFrame to accumulate timing info
    run_times = []

    for run in range(n_runs):
        print(f"\n🚀 Starting run {run+1}/{n_runs}")
        start_time = time.time()
        parallel_optimization(cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year)
        end_time = time.time()

        duration = end_time - start_time
        print(f"✅ Run {run+1} completed in {duration:.2f} seconds")

        # Save time for this run
        run_times.append({'Run': run + 1, 'ExecutionTimeSeconds': round(duration, 2)})

        # Fetch the summary table from SQL after each run
        summary_df = pd.read_sql('topsis_multiobjective_summary', con=engine)

        # Add a run index to track runs
        summary_df['run'] = run + 1
        all_runs_df = pd.concat([all_runs_df, summary_df], ignore_index=True)

    # Calculate mean TotalCost and TotalCarbonEmissions for each year
    mean_df = all_runs_df.groupby('Year')[['TotalCost', 'TotalCarbonEmissions']].mean().reset_index()

    # Store averaged results
    mean_df.to_sql('topsis_multiobjective_summary_avg', con=engine, if_exists='replace', index=False)
    print("\n📊 Averaged results stored in SQL table: `topsis_multiobjective_summary_avg`")

    # Store run time data
    run_times_df = pd.DataFrame(run_times)
    run_times_df.to_sql('parallel_topsis_run_times', con=engine, if_exists='replace', index=False)
    print("\n⏱️ Execution times stored in SQL table: `parallel_topsis_run_times`")

if __name__ == "__main__":
    run_multiple_optimizations()
