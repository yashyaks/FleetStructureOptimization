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
    # demand = data_demand['demand']
    print(data_topsis)
    cost_topsis = data_topsis['TotalCost']
    emissions_topsis = data_topsis['TotalCarbonEmissions']
    
    fig, ax1 = plt.subplots(figsize=(10,5))
    print(emissions_no_topsis)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Carbon Emissions', color='tab:blue')
    ax1.plot(years, emissions_no_topsis, 'o-', label='Emissions (No TOPSIS)', color='red')
    ax1.plot(years, emissions_topsis, 's-', label='Emissions (With TOPSIS)', color='orange')
    # ax1.plot(years, emissions_no_topsis, 'o-', label='Demand', color='blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Total Cost', color='tab:red')
    # ax2.plot(years, cost_no_topsis, 'o--', label='Cost (No TOPSIS)', color='blue')
    # ax2.plot(years, cost_topsis, 's--', label='Cost (With TOPSIS)', color='cyan')
    # ax2.tick_params(axis='y', labelcolor='tab:red')
    
    
    
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.title('Fleet Management: Demand & Cost Comparison')
    plt.show()

# Example Usage
plot_fleet_data('data/output/tradeoff/notopsis/multiobjective_summary.csv', 'data/output/tradeoff/topsis/multiobjective_summary.csv', 'data/demand.csv')

