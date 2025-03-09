from demand import VehicleAllocation
from topsis import Topsis
from tradeoff_topsis_copy import MultiObjectiveFleetOptimizer
from evaluation import Evaluation
from summary import Summary
import matplotlib.pyplot as plt
import os
import pandas as pd
from pprint import pprint

def main():
    va = VehicleAllocation()
    tp = Topsis()
    ev = Evaluation()
    summarizer = Summary()
    
    for year in range(2023, 2039):
        print(f"Starting process for year {year}")
        df = va.allocate_vehicles(year)
        df.to_csv(f'data/output/tradeoff/topsis/allocation_output_{year}.csv', index=False)
        print(f"Allocated vehicles for year {year}")

        if os.path.exists(f"data/output/tradeoff/topsis/multi_objective_fleet_allocation_{(year-1)}.csv"):
            print("Merging with previous year vehicles")
            df1 = pd.read_csv(f"data/output/tradeoff/topsis/multi_objective_fleet_allocation_{(year-1)}.csv")
            df1['Operating Year'] = year
            merged_df = pd.concat([df1, df], ignore_index=True, sort=False)
            merged_df = merged_df[merged_df['Available Year'] > (year-5)]
            
        else:
            merged_df = df.copy()
        merged_df.loc[merged_df['Available Year'] < year, 'Cost ($)'] = 0
        print("Initializing Topsis calculation")
        tp_df = tp.apply_topsis(year, merged_df)
        tp_df.to_csv(f'data/output/tradeoff/topsis/topsis_output_{year}.csv', index=False)
        print(f"TOPSIS calculation done for year {year}")
           
        column_mapping = {
            'Unnamed: 0': 'Index',
        } 
        tp_df.rename(columns=column_mapping, inplace=True) 
        
        print(f"Multiobjective Optimization...")
        mo = MultiObjectiveFleetOptimizer(tp_df)
        df = mo.get_optimized_results(year)
        df.to_csv(f'data/output/tradeoff/topsis/multi_objective_fleet_allocation_{year}.csv', index=False)
        print("Optimization done, output saved to file")
        
        
        df = ev.apply_metrics_to_dataframe(df)
        df.to_csv(f'data/output/tradeoff/topsis/multi_objective_fleet_allocation_eval_{year}.csv', index=False)
        print(f"Optimization and Evaluation done for year {year}")
        print(f"Generating summary for year {year}")
        summary_df = summarizer.summarize(df, year)
        summary_df.to_csv('data/output/tradeoff/topsis/multiobjective_summary.csv')
        print("Summary generated")
        
        print()
    
if __name__ == "__main__":
    main()