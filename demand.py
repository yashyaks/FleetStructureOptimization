import pandas as pd
from utilities.my_sql_operations import MySQLOperations
from utilities.carbon_emmissions import CarbonEmissions
from utilities.costs import Costs

class VehicleAllocation:
    def __init__(self):
        pass
  
    def allocate_vehicles(self, year):
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT * FROM vehicles"""
        vehicles_data, columns = my_sql_operations.fetch_data(query)
        vehicles_df = pd.DataFrame(vehicles_data, columns=columns)
                
        query = f"""SELECT * FROM demand"""
        demand_data, columns = my_sql_operations.fetch_data(query)
        demand_df = pd.DataFrame(demand_data, columns=columns)
                
        query = f"""SELECT * FROM vehicles_fuels"""
        vehicle_fuels_data, columns = my_sql_operations.fetch_data(query)
        vehicle_fuels_df = pd.DataFrame(vehicle_fuels_data, columns=columns)

        distance_mapping = {"D1": 1, "D2": 2, "D3": 3, "D4": 4}
        
        vehicles_df['Distance_categorical'] = vehicles_df['distance'].map(distance_mapping)
        demand_df['Distance_categorical'] = demand_df['distance'].map(distance_mapping)

        demand_df = demand_df[demand_df['year'] == year].copy()
        available_vehicles = vehicles_df[vehicles_df['year'] == year]

        def find_allocations(row):
            size_needed = row['size']
            distance_needed = row['Distance_categorical']
            allocated_vehicles = available_vehicles[
                (available_vehicles['size'] == size_needed) & 
                (available_vehicles['Distance_categorical'] >= distance_needed)
            ]['id'].tolist() 
            
            return allocated_vehicles
        
        demand_df['Allocation'] = demand_df.apply(find_allocations, axis=1)  
        
        df_exploded = demand_df.explode("Allocation")
        df = pd.merge(df_exploded[['Allocation', 'year', 'size', 'distance', 'demand']], vehicles_df[['id','vehicle', 'year', 'cost', 'yearly_range', 'distance']], how='left', left_on='Allocation', right_on='id')
        
        df = df.rename(columns={'year_x': 'Operating Year', 'year_y': 'Available Year', 'distance_x': 'Distance_demand', 'distance_y': 'Distance_vehicle'})
        
        df = pd.merge(df, vehicle_fuels_df, how='left', left_on='id', right_on='id')
        ce = CarbonEmissions()
        df['carbon_emissions_per_km'] = ce.per_km_carbon_emmissions_per_vehicle(df, year)
        costs = Costs()
        df['insurance_cost'] = costs.yearly_insurance_cost_per_vehicle(df)
        df['maintenance_cost'] = costs.yearly_maintenance_cost_per_vehicle(df)
        df['fuel_costs_per_km'] = costs.per_km_fuel_cost_per_vehicle(df, year)
        df['Operating_Cost'] = df['insurance_cost'] + df['maintenance_cost'] + (df['fuel_costs_per_km'] * df['yearly_range'])
        
        
        return df