from demand import VehicleAllocation
from topsis import Topsis
from tradeoff_topsis import MultiObjectiveFleetOptimizer
from utilities.evaluation import Evaluation
from utilities.summary import Summary
from utilities.costs import Costs
from utilities.carbon_emmissions import CarbonEmissions

from utilities.my_sql_operations import MySQLOperations
import pandas as pd
import os
from pprint import pprint

def optimization(cost_weight, ce_weight, generations, population_size, prev_years, min_year, max_year):
    print(cost_weight, ce_weight, generations, population_size, prev_years)
    va = VehicleAllocation()
    tps = Topsis()
    eval = Evaluation()
    summarizer = Summary()
    sqlops = MySQLOperations()
    costs = Costs()
    ce = CarbonEmissions()
    connection_string = os.getenv('OUTPUT_STRING')
    
    output_list = []
    for year in range(min_year, max_year+1):
        print(f"Starting process for year {year}")
        df = va.allocate_vehicles(year)
        # df.to_csv(f'data/output/tradeoff/topsis/allocation_output_{year}.csv', index=False)
        print(f"Allocated vehicles for year {year}")
        if sqlops.table_exists(f'multi_objective_fleet_allocation_eval_{(year-1)}') == 1:
            print("Merging with previous year vehicles")
            
            # df1 = pd.read_csv(f"data/output/tradeoff/topsis/multi_objective_fleet_allocation_{(year-1)}.csv")
            query = f"""SELECT * FROM multi_objective_fleet_allocation_eval_{(year-1)} WHERE `Operating Year` = {year-1}"""
            vehicles_data, columns = sqlops.fetch_data(query, database='output')
            df1 = pd.DataFrame(vehicles_data, columns=columns)
            df1['Operating Year'] = year
            merged_df = pd.concat([df1, df], ignore_index=True, sort=False)
            merged_df = merged_df[merged_df['Available Year'] > (year-prev_years)]
            merged_df.drop('demand', axis=1, inplace=True)
            ## UPDATING VALUES FOR OPERATING COSTS AND DEMAND COLUMNS
            
            query = f"""SELECT * FROM demand WHERE year = {year};"""
            demand_data, columns = sqlops.fetch_data(query)
            demand_df = pd.DataFrame(demand_data, columns=columns)

            df = pd.merge(
                merged_df, 
                demand_df[['size', 'distance', 'demand']], 
                how='left',
                left_on=['size', 'Distance_demand'],
                right_on=['size', 'distance']
            )
            print(df)
            # df.rename(columns={'demand': 'Demand (km)'}, inplace=True)
            # df.drop('size', axis=1, inplace=True)
            # df.drop('distance', axis=1, inplace=True)
            
            # df['fuel_costs_per_km'] = costs.per_km_fuel_cost_per_vehicle(df, year)
            # df['maintenance_cost'] = costs.yearly_maintenance_cost_per_vehicle(df)
            # df['insurance_cost'] = costs.yearly_insurance_cost_per_vehicle(df)
            
            merged_df = df.copy()
                  
        else:
            merged_df = df.copy()
        

        merged_df['fuel_costs_per_km'] = costs.per_km_fuel_cost_per_vehicle(merged_df, year)
        merged_df['maintenance_cost'] = costs.yearly_maintenance_cost_per_vehicle(merged_df)
        merged_df['insurance_cost'] = costs.yearly_insurance_cost_per_vehicle(merged_df)
        
        merged_df.loc[merged_df['Available Year'] < year, 'cost'] = 0
        print("Initializing Topsis calculation")
        weights = [ce_weight, cost_weight, cost_weight]
        tp_df = tps.apply_topsis(year, merged_df, weights)
        print(f"TOPSIS calculation done for year {year}")
           
        column_mapping = {
            'Unnamed: 0': 'Index',
        } 
        tp_df.rename(columns=column_mapping, inplace=True) 
        print(f"Multiobjective Optimization...")
        mo = MultiObjectiveFleetOptimizer(tp_df, ce_weight, cost_weight)
        df = mo.get_optimized_results(year, generations, population_size)

        # df.to_csv(f'data/output/tradeoff/topsis/multi_objective_fleet_allocation_{year}.csv', index=False)
        print("Optimization done, output saved to file")
        
        # pprint(solutions)
        df = eval.apply_metrics_to_dataframe(df)

        output_list.append(df)
        # df.to_csv(f'data/output/tradeoff/topsis/multi_objective_fleet_allocation_eval_{year}.csv', index=False)
        
        print(f"Optimization and Evaluation done for year {year}")
        print(f"Generating summary for year {year}")
        summary_df = summarizer.summarize(df, year)
        # summary_df.to_csv('data/output/tradeoff/topsis/multiobjective_summary.csv')
        print("Summary generated")
        
        engine = sqlops.create_sqlalchemy_engine(connection_string)
        df.to_sql(f'multi_objective_fleet_allocation_eval_{year}', con=engine, if_exists='replace') 
        summary_df.to_sql('topsis_multiobjective_summary', con=engine, if_exists='replace')
        print()
    
    result = pd.concat(output_list)
    engine = sqlops.create_sqlalchemy_engine(connection_string)
    
    # result.rename(columns=column_mapping, inplace=True)
    result.to_sql(f'combined_multi_objective_fleet_allocation_eval', con=engine, if_exists='replace') 
    
