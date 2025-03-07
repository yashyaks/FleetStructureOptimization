from demand import VehicleAllocation
from topsis import Topsis
from tradeoff_topsis_copy import MultiObjectiveFleetOptimizer
from evaluation import Evaluation
from summary import Summary
import matplotlib.pyplot as plt
import os

def main():
    
    va = VehicleAllocation()
    tp = Topsis()
    ev = Evaluation()
    summarizer = Summary()
    
    for year in range(2023, 2039):
        print(f"Starting process for year {year}")
        df = va.allocate_vehicles(year)
        print(f"Allocated vehicles for year {year}")
        tp_df = tp.apply_topsis(year, df)
        print(f"TOPSIS calculation done for year {year}")
        
        column_mapping = {
            'Unnamed: 0': 'Index',
            'Allocation': 'Allocation',
            'Size': 'Size',
            'Distance_demand': 'Distance_demand',
            'Demand (km)': 'Demand',
            'Cost ($)': 'Cost',
            'Yearly range (km)': 'Yearly_Range',
            'insurance_cost': 'Insurance_Cost',
            'maintenance_cost': 'Maintenance_Cost',
            'fuel_costs_per_km': 'Fuel_Costs',
            'Fuel': 'Fuel',
            'Total_Cost': 'Total_Cost',
            'Topsis_Score': 'Topsis_Score',
            'carbon_emission_per_km': 'carbon_emissions_per_km'
        }
        
        tp_df.rename(columns=column_mapping, inplace=True) 
        
        print(f"Multiobjective Optimization...")
        mo = MultiObjectiveFleetOptimizer(tp_df)
        df = mo.get_optimized_results(year)
        print("Optimization done, output saved to file; evaluating output")
        df = ev.apply_metrics_to_dataframe(df)
        df.to_csv(f'data/output/tradeoff/notopsis/multi_objective_fleet_allocation_eval_{year}.csv', index=False)
        print(f"Optimization and Evaluation done for year {year}")
        print(f"Generating summary for year {year}")
        summary_df = summarizer.summarize(df, year)
        summary_df.to_csv('data/output/tradeoff/notopsis/multiobjective_summary.csv')
        print("Summary generated")
        
        print()
        
if __name__ == "__main__":
    main()