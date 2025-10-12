import pandas as pd
from main_tradeoff_notopsis import optimization
from utilities.my_sql_operations import MySQLOperations
import os
import time

def run_multiple_optimizations(n_runs=1):
    cost_weight, carbon_emissions_weight = 0.5, 0.5
    generations, population_size = 50, 100
    prev_years, min_year, max_year = 7, 2023, 2038
    
    table_prefix = "notopsis"

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
        optimization(cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year, table_prefix)
        end_time = time.time()

        duration = end_time - start_time
        print(f"✅ Run {run+1} completed in {duration:.2f} seconds")

        # Save time for this run
        run_times.append({'Run': run + 1, 'ExecutionTimeSeconds': round(duration, 2)})

        # Fetch the summary table from SQL after each run
        summary_df = pd.read_sql(f'{table_prefix}_multiobjective_summary', con=engine)

        # Add a run index to track runs
        summary_df['run'] = run + 1
        all_runs_df = pd.concat([all_runs_df, summary_df], ignore_index=True)

    # Calculate mean TotalCost and TotalCarbonEmissions for each year
    # mean_df = all_runs_df.groupby('Year')[['TotalCost', 'TotalCarbonEmissions']].mean().reset_index()

    # all_runs_df.to_sql(f'{table_prefix}_multiobjective_summary_all_runs', con=engine, if_exists='replace', index=False)
    # print(f"\n📊 All runs' results stored in SQL table: {f'{table_prefix}_multiobjective_summary_all_runs'}")
    # # Store averaged results
    # mean_df.to_sql(f'{table_prefix}_multiobjective_summary_avg', con=engine, if_exists='replace', index=False)
    # print(f"\n📊 Averaged results stored in SQL table: `{table_prefix}_multiobjective_summary_avg`")

    # Store run time data
    run_times_df = pd.DataFrame(run_times)
    # run_times_df.to_sql(f'{table_prefix}_run_times', con=engine, if_exists='replace', index=False)
    # print(f"\n⏱️ Execution times stored in SQL table: `{table_prefix}_run_times`")

if __name__ == "__main__":
    run_multiple_optimizations()
