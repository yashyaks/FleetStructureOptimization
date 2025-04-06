import os
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a MySQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

def plot_and_analyze_fleet_data(table_no_topsis, table_topsis, table_demand):
    """
    Plots cost and emissions comparisons using data from MySQL tables.
    Also calculates and prints the total sums and percentage differences.
    """
    data_no_topsis = fetch_data(table_no_topsis)
    data_topsis = fetch_data(table_topsis)
    
    years = data_no_topsis['Year']
    
    # Calculate total sums
    total_emissions_no_topsis = data_no_topsis['TotalCarbonEmissions'].sum()
    total_emissions_topsis = data_topsis['TotalCarbonEmissions'].sum()
    total_cost_no_topsis = data_no_topsis['TotalCost'].sum()
    total_cost_topsis = data_topsis['TotalCost'].sum()
    
    # Calculate percentage differences
    emissions_diff_percent = ((total_emissions_topsis - total_emissions_no_topsis) / total_emissions_no_topsis) * 100
    cost_diff_percent = ((total_cost_topsis - total_cost_no_topsis) / total_cost_no_topsis) * 100
    
    # Print the results
    print("\n--- SUMMARY OF RESULTS ---")
    print(f"Total Carbon Emissions (No TOPSIS): {total_emissions_no_topsis:.2f} kg CO2")
    print(f"Total Carbon Emissions (With TOPSIS): {total_emissions_topsis:.2f} kg CO2")
    print(f"Percentage Difference in Emissions: {emissions_diff_percent:.2f}%")
    print(f"\nTotal Cost (No TOPSIS): {total_cost_no_topsis:.2f}")
    print(f"Total Cost (With TOPSIS): {total_cost_topsis:.2f}")
    print(f"Percentage Difference in Cost: {cost_diff_percent:.2f}%")
    print("------------------------\n")
    
    # Carbon Emissions Plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, data_no_topsis['TotalCarbonEmissions'], 'o-', label='Emissions (No TOPSIS)', color='red')
    plt.plot(years, data_topsis['TotalCarbonEmissions'], 's-', label='Emissions (With TOPSIS)', color='green')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Carbon Emissions (kg CO2)', fontsize=14)
    plt.title('Comparison of Total Emissions Over Years', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

    # Cost Plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, data_no_topsis['TotalCost'], 'o-', label='Cost (No TOPSIS)', color='red')
    plt.plot(years, data_topsis['TotalCost'], 's-', label='Cost (With TOPSIS)', color='green')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Cost', fontsize=14)
    plt.title('Comparison of Total Cost Over Years', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

# Example Usage
plot_and_analyze_fleet_data('notopsis_multiobjective_summary', 'topsis_multiobjective_summary', 'demand')