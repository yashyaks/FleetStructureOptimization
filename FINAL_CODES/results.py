# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# def plot_fleet_data(csv_no_topsis, csv_topsis):
#     data_no_topsis = pd.read_csv(csv_no_topsis)
#     data_topsis = pd.read_csv(csv_topsis)
    
#     years = data_no_topsis['Year']
#     cost_no_topsis = data_no_topsis['Total Cost ($)']
#     emissions_no_topsis = data_no_topsis['Total carbon_emissions_per_km']
    
#     cost_topsis = data_topsis['Total Cost ($)']
#     emissions_topsis = data_topsis['Total carbon_emissions_per_km']
    
#     fig, ax1 = plt.subplots(figsize=(10,5))
    
#     ax1.set_xlabel('Year')
#     ax1.set_ylabel('Total Cost ($)', color='tab:blue')
#     ax1.plot(years, cost_no_topsis, 'o-', label='Cost (No TOPSIS)', color='blue')
#     ax1.plot(years, cost_topsis, 's-', label='Cost (With TOPSIS)', color='cyan')
#     ax1.tick_params(axis='y', labelcolor='tab:blue')
    
#     ax2 = ax1.twinx()
#     ax2.set_ylabel('Total Carbon Emissions per km', color='tab:red')
#     ax2.plot(years, emissions_no_topsis, 'o--', label='Emissions (No TOPSIS)', color='red')
#     ax2.plot(years, emissions_topsis, 's--', label='Emissions (With TOPSIS)', color='orange')
#     ax2.tick_params(axis='y', labelcolor='tab:red')
    
#     fig.tight_layout()
#     fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
#     plt.title('Fleet Management: Cost & Emissions Comparison')
#     plt.show()

# # Example Usage
# plot_fleet_data('multi_objective_fleet_genetic_only/yearly_summary_multi_objective.csv', 'multi_objective_fleet_results/yearly_summary_multi_objective.csv')


import os
import pandas as pd
import re

def extract_year(allocation):
    match = re.search(r'\d{4}$', str(allocation))
    return int(match.group()) if match else None

def combine_csv_files(input_folder, output_file):
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    if not all_files:
        print("No CSV files found in the directory.")
        return
    
    df_list = [pd.read_csv(os.path.join(input_folder, file)) for file in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Extract Year from Allocation column (format: Diesel_S1_2023)
    combined_df['Year'] = combined_df['Allocation'].apply(extract_year)
    
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved as {output_file}")

# Example usage
input_folder = "multi_objective_fleet_results"
output_file = "combined_output.csv"
combine_csv_files(input_folder, output_file)
