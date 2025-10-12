import os
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Fetch DB_URL from environment variable
DB_URL = os.getenv("OUTPUT_STRING")

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def fetch_data(table_name):
    """Fetches data from a SQL table using SQLAlchemy."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

def plot_and_analyze_fleet_data(table1, table2, label1="Table 1", label2="Table 2"):
    """
    Generic function to compare two tables for cost and emissions.
    Automatically reports increase/decrease percentages.
    """
    data1 = fetch_data(table1)
    data2 = fetch_data(table2)
    # data3 = fetch_data(table3)
    
    years = data1['Year']
    
    # Calculate totals
    total_emissions1 = data1['TotalCarbonEmissions'].sum()
    total_emissions2 = data2['TotalCarbonEmissions'].sum()
    total_cost1 = data1['TotalCost'].sum()
    total_cost2 = data2['TotalCost'].sum()

    
    # Calculate percentage differences (relative to table1)
    emissions_diff_percent = ((total_emissions2 - total_emissions1) / total_emissions1) * 100
    cost_diff_percent = ((total_cost2 - total_cost1) / total_cost1) * 100
    
    # Helper for formatting increase/decrease
    def format_change(pct):
        if pct > 0:
            return f"Increased by {pct:.2f}%"
        elif pct < 0:
            return f"Reduced by {abs(pct):.2f}%"
        else:
            return "No change"
    
    # Print results
    print("\n--- SUMMARY OF RESULTS ---")
    print(f"Total Carbon Emissions ({label1}): {total_emissions1:.2f} kg CO2")
    print(f"Total Carbon Emissions ({label2}): {total_emissions2:.2f} kg CO2")
    print(f"Change in Emissions: {format_change(emissions_diff_percent)}")
    print(f"\nTotal Cost ({label1}): {total_cost1:.2f}")
    print(f"Total Cost ({label2}): {total_cost2:.2f}")
    print(f"Change in Cost: {format_change(cost_diff_percent)}")
    print("------------------------\n")
    
    # Emissions Plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, data1['TotalCarbonEmissions'], 'o-', label=f'Emissions ({label1})', color='red')
    plt.plot(years, data2['TotalCarbonEmissions'], 's-', label=f'Emissions ({label2})', color='green')
    # plt.plot(years, data3['TotalCarbonEmissions'], 's-', label=f'Emissions ({label3})', color='blue')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Carbon Emissions (kg CO2)', fontsize=14)
    plt.title(f'Comparison of Total Emissions: {label1} vs {label2}', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

    # Cost Plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, data1['TotalCost'], 'o-', label=f'Cost ({label1})', color='red')
    plt.plot(years, data2['TotalCost'], 's-', label=f'Cost ({label2})', color='green')
    # plt.plot(years, data3['TotalCost'], 's-', label=f'Cost ({label3})', color='blue')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Cost', fontsize=14)
    plt.title(f'Comparison of Total Cost: {label1} vs {label2}', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

# Example Usage:
plot_and_analyze_fleet_data(
    "topsis_50_multiobjective_summary_avg",
    "notopsis_multiobjective_summary_avg", 
    # "topsis_250_multiobjective_summary_avg", 
    label1="TOPSIS NSGA-II",
    label2="NSGA-II without TOPSIS", 
    # label3="TOPSIS NSGA-II (250 generations)",

)