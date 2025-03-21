# import time
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# import numpy as np
# from concurrent.futures import ProcessPoolExecutor
# import argparse

# # Import both implementations
# from tradeoff_topsis import MultiObjectiveFleetOptimizer as SerialOptimizer
# from tradeoff_topsis_parellel import MultiObjectiveFleetOptimizer as ParallelOptimizer

# class PerformanceComparison:
#     def __init__(self):
#         self.results = {
#             'year': [],
#             'serial_time': [],
#             'parallel_time': [],
#             'speedup': [],
#             'dataset_size': []
#         }
        
#     def run_serial(self, year, df):
#         """Run the serial implementation and measure time"""
#         start_time = time.time()
#         optimizer = SerialOptimizer(df)
#         result = optimizer.get_optimized_results(year)
#         end_time = time.time()
#         return result, end_time - start_time
    
#     def run_parallel(self, year, df):
#         """Run the parallel implementation and measure time"""
#         start_time = time.time()
#         optimizer = ParallelOptimizer(df)
#         result = optimizer.get_optimized_results(year)
#         end_time = time.time()
#         return result, end_time - start_time
    
#     def compare_performance(self, years=None, iterations=3):
#         """Compare performance across multiple years with multiple iterations for reliability"""
#         if years is None:
#             years = range(2023, 2039)  # Default to all years in your range
        
#         for year in years:
#             print(f"Comparing performance for year {year}")
#             # Load data for the year
#             try:
#                 input_path = f"data/output/tradeoff/topsis/topsis_output_{year}.csv"
#                 if not os.path.exists(input_path):
#                     print(f"Warning: Data for year {year} not found at {input_path}. Skipping.")
#                     continue
                
#                 df = pd.read_csv(input_path)
#                 dataset_size = len(df)
                
#                 # Run multiple iterations and take average for more reliable measurements
#                 serial_times = []
#                 parallel_times = []
                
#                 for i in range(iterations):
#                     print(f"  Running iteration {i+1}/{iterations}")
                    
#                     # Run serial implementation
#                     _, serial_time = self.run_serial(year, df.copy())
#                     serial_times.append(serial_time)
                    
#                     # Run parallel implementation
#                     _, parallel_time = self.run_parallel(year, df.copy())
#                     parallel_times.append(parallel_time)
                
#                 # Calculate average times
#                 avg_serial_time = sum(serial_times) / len(serial_times)
#                 avg_parallel_time = sum(parallel_times) / len(parallel_times)
#                 speedup = avg_serial_time / avg_parallel_time if avg_parallel_time > 0 else 0
                
#                 # Store results
#                 self.results['year'].append(year)
#                 self.results['serial_time'].append(avg_serial_time)
#                 self.results['parallel_time'].append(avg_parallel_time)
#                 self.results['speedup'].append(speedup)
#                 self.results['dataset_size'].append(dataset_size)
                
#                 print(f"  Average Serial Time: {avg_serial_time:.2f}s")
#                 print(f"  Average Parallel Time: {avg_parallel_time:.2f}s")
#                 print(f"  Speedup: {speedup:.2f}x")
#                 print(f"  Dataset Size: {dataset_size} rows")
#                 print()
                
#             except Exception as e:
#                 print(f"Error processing year {year}: {e}")
#                 continue
        
#         # Convert results to DataFrame for easier analysis
#         self.results_df = pd.DataFrame(self.results)
        
#     def save_results(self, output_dir="performance_results"):
#         """Save results to CSV file"""
#         if not hasattr(self, 'results_df'):
#             print("No results to save. Run comparison first.")
#             return
            
#         os.makedirs(output_dir, exist_ok=True)
#         output_path = os.path.join(output_dir, "performance_comparison_results.csv")
#         self.results_df.to_csv(output_path, index=False)
#         print(f"Results saved to {output_path}")
    
#     def plot_execution_times(self, output_dir="performance_results"):
#         """Plot execution times comparison between serial and parallel implementations"""
#         if not hasattr(self, 'results_df'):
#             print("No results to plot. Run comparison first.")
#             return
            
#         os.makedirs(output_dir, exist_ok=True)
        
#         # Set the style
#         plt.style.use('ggplot')
#         sns.set_palette("Set2")
        
#         # Plot 1: Execution time comparison by year
#         plt.figure(figsize=(12, 6))
        
#         width = 0.35
#         x = np.arange(len(self.results_df['year']))
        
#         plt.bar(x - width/2, self.results_df['serial_time'], width, label='Serial Implementation')
#         plt.bar(x + width/2, self.results_df['parallel_time'], width, label='Parallel Implementation')
        
#         plt.xlabel('Year')
#         plt.ylabel('Execution Time (seconds)')
#         plt.title('Execution Time Comparison: Serial vs Parallel Implementation')
#         plt.xticks(x, self.results_df['year'])
#         plt.legend()
#         plt.grid(True, linestyle='--', alpha=0.7)
        
#         # Rotate x-axis labels for better readability
#         plt.xticks(rotation=45)
#         plt.tight_layout()
        
#         output_path = os.path.join(output_dir, "execution_time_comparison.png")
#         plt.savefig(output_path, dpi=300)
#         print(f"Execution time comparison plot saved to {output_path}")
        
#         # Plot 2: Speedup by year
#         plt.figure(figsize=(12, 6))
#         plt.plot(self.results_df['year'], self.results_df['speedup'], 'o-', linewidth=2, markersize=8)
#         plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='No Speedup')
        
#         plt.xlabel('Year')
#         plt.ylabel('Speedup (Serial Time / Parallel Time)')
#         plt.title('Speedup Achieved by Parallel Implementation')
#         plt.grid(True, linestyle='--', alpha=0.7)
#         plt.legend()
        
#         # Add value labels above points
#         for i, speedup in enumerate(self.results_df['speedup']):
#             plt.annotate(f"{speedup:.2f}x", 
#                          (self.results_df['year'][i], speedup), 
#                          textcoords="offset points", 
#                          xytext=(0,10), 
#                          ha='center')
        
#         plt.tight_layout()
#         output_path = os.path.join(output_dir, "speedup_comparison.png")
#         plt.savefig(output_path, dpi=300)
#         print(f"Speedup comparison plot saved to {output_path}")
        
#         # Plot 3: Execution time vs Dataset size
#         plt.figure(figsize=(12, 6))
#         plt.scatter(self.results_df['dataset_size'], self.results_df['serial_time'], label='Serial', s=100, alpha=0.7)
#         plt.scatter(self.results_df['dataset_size'], self.results_df['parallel_time'], label='Parallel', s=100, alpha=0.7)
        
#         # Add trend lines
#         sns.regplot(x='dataset_size', y='serial_time', data=self.results_df, 
#                    scatter=False, ci=None, label='Serial Trend')
#         sns.regplot(x='dataset_size', y='parallel_time', data=self.results_df, 
#                    scatter=False, ci=None, label='Parallel Trend')
        
#         plt.xlabel('Dataset Size (rows)')
#         plt.ylabel('Execution Time (seconds)')
#         plt.title('Execution Time vs Dataset Size')
#         plt.grid(True, linestyle='--', alpha=0.7)
#         plt.legend()
        
#         # Add year labels to points
#         for i, year in enumerate(self.results_df['year']):
#             plt.annotate(str(year), 
#                          (self.results_df['dataset_size'][i], self.results_df['serial_time'][i]), 
#                          textcoords="offset points", 
#                          xytext=(5,5), 
#                          ha='left')
#             plt.annotate(str(year), 
#                          (self.results_df['dataset_size'][i], self.results_df['parallel_time'][i]), 
#                          textcoords="offset points", 
#                          xytext=(5,5), 
#                          ha='left')
        
#         plt.tight_layout()
#         output_path = os.path.join(output_dir, "execution_time_vs_dataset_size.png")
#         plt.savefig(output_path, dpi=300)
#         print(f"Execution time vs dataset size plot saved to {output_path}")
        
#         # Plot 4: Memory usage comparison if available
#         # This would require additional instrumentation in your code

# def main():
#     parser = argparse.ArgumentParser(description='Compare performance between serial and parallel implementations')
#     parser.add_argument('--years', type=int, nargs='+', help='Specific years to compare (default: all years)')
#     parser.add_argument('--iterations', type=int, default=3, help='Number of iterations for reliable measurements (default: 3)')
#     parser.add_argument('--output', type=str, default='performance_results', help='Output directory for results and plots')
    
#     args = parser.parse_args()
    
#     comparison = PerformanceComparison()
#     comparison.compare_performance(years=args.years, iterations=args.iterations)
#     comparison.save_results(output_dir=args.output)
#     comparison.plot_execution_times(output_dir=args.output)

# if __name__ == "__main__":
#     main()



# import time
# import pandas as pd
# import subprocess

# def run_script(script_name):
#     """Runs a Python script and measures execution time."""
#     start_time = time.time()
#     subprocess.run(["python", script_name], check=True)
#     end_time = time.time()
#     return end_time - start_time

# def compare_results(file_serial, file_parallel):
#     """Loads the results from both methods and compares them."""
#     df_serial = pd.read_csv(file_serial)
#     df_parallel = pd.read_csv(file_parallel)
    
#     # Comparing execution performance
#     performance_comparison = {
#         'Total Cost Difference': df_serial['Total_Cost'].sum() - df_parallel['Total_Cost'].sum(),
#         'Total Carbon Emissions Difference': df_serial['Total_CE'].sum() - df_parallel['Total_CE'].sum(),
#         'Average Utilization (%) Difference': df_serial['Utilization (%)'].mean() - df_parallel['Utilization (%)'].mean(),
#         'Demand Fulfillment Difference': df_serial['DemandFulfillment'].sum() - df_parallel['DemandFulfillment'].sum()
#     }
    
#     return performance_comparison

# def main():
#     serial_time = run_script("main_tradeoff_topsis.py")
#     parallel_time = run_script("main_tradeoff_topsis_parallel.py")
    
#     print(f"Serial Execution Time: {serial_time:.2f} seconds")
#     print(f"Parallel Execution Time: {parallel_time:.2f} seconds")
    
#     # result_file_serial = "data/output/tradeoff/topsis/combined_multi_objective_fleet_allocation_eval.csv"
#     # result_file_parallel = "data/output/tradeoff/topsis_parallel/combined_multi_objective_fleet_allocation_eval.csv"
    
#     # comparison = compare_results(result_file_serial, result_file_parallel)
    
#     print("Performance Comparison:")
#     for metric, value in comparison.items():
#         print(f"{metric}: {value}")
    
#     print("Parallel Execution Speedup:", serial_time / parallel_time)
    
# if __name__ == "__main__":
#     main()



import time
import subprocess
import matplotlib.pyplot as plt

def run_script(script_name):
    """Runs a Python script and measures execution time."""
    start_time = time.time()
    subprocess.run(["python", script_name], check=True)
    end_time = time.time()
    return end_time - start_time

def main():
    serial_time = run_script("main_tradeoff_topsis.py")
    parallel_time = run_script("main_tradeoff_topsis_parallel.py")
    
    print(f"Serial Execution Time: {serial_time:.2f} seconds")
    print(f"Parallel Execution Time: {parallel_time:.2f} seconds")
    
    # Plotting execution times
    labels = ['Serial', 'Parallel']
    times = [serial_time, parallel_time]
    
    plt.figure(figsize=(6, 4))
    plt.bar(labels, times, color=['red', 'green'])
    plt.xlabel("Execution Type")
    plt.ylabel("Time (seconds)")
    plt.title("Execution Time Comparison")
    plt.show()
    
if __name__ == "__main__":
    main()

