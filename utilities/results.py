import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_fleet_data(csv_no_topsis, csv_topsis, csv_demand):
    data_no_topsis = pd.read_csv(csv_no_topsis)
    data_topsis = pd.read_csv(csv_topsis)
    data_demand = pd.read_csv(csv_demand)
    
    years = data_no_topsis['Year']
    cost_no_topsis = data_no_topsis['TotalCost']
    emissions_no_topsis = data_no_topsis['TotalCarbonEmissions']
    
    cost_topsis = data_topsis['TotalCost']
    emissions_topsis = data_topsis['TotalCarbonEmissions']
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Total Carbon Emissions (kg Co2)', fontsize=14)
    ax1.plot(years, emissions_no_topsis, 'o-', label='Emissions (No TOPSIS)', color='red')
    ax1.plot(years, emissions_topsis, 's-', label='Emissions (With TOPSIS)', color='green')
    ax1.tick_params(axis='y', labelsize=14)
    ax1.tick_params(axis='x', labelsize=14)
    
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Total Cost', color='tab:red', fontsize=14)
    # ax2.plot(years, cost_no_topsis, 'o--', label='Cost (No TOPSIS)', color='blue')
    # ax2.plot(years, cost_topsis, 's--', label='Cost (With TOPSIS)', color='cyan')
    # ax2.tick_params(axis='y', labelcolor='tab:red', labelsize=14)
    
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), fontsize=14)
    plt.title('Comparison of Total Emissions Over Years', fontsize=16)
    plt.show()

# Example Usage
plot_fleet_data('data/output/tradeoff/notopsis/multiobjective_summary.csv', 
                'data/output/tradeoff/topsis/multiobjective_summary.csv', 
                'data/demand.csv')
