import pandas as pd
import numpy as np
from utilities.my_sql_operations import MySQLOperations
from pprint import pprint

class VehicleAllocation:
    def __init__(self):
        self.data_root = './data/'
        
    def per_km_carbon_emmissions_per_vehicle(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Calculates per km carbon emissions for one vehicle
        """     
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT fuel, emissions_co2_per_unit_fuel FROM fuels WHERE year = {op_year}"""
        fuel_data, columns = my_sql_operations.fetch_data(query) 
        fuel_df = pd.DataFrame(fuel_data, columns=columns)

        merged_df = pd.merge(fleet_details, fuel_df, left_on='fuel', right_on='fuel', how='left')
        
        merged_df['carbon_emissions_per_km'] = (
            merged_df['emissions_co2_per_unit_fuel'] *
            merged_df['consumption_unitfuel_per_km']
        )
        return merged_df['carbon_emissions_per_km']
    
    def yearly_insurance_cost_per_vehicle(self, fleet_details: pd.DataFrame):
        """
        Returns Insurance cost for one vehicle
        """
        total_fleet_insurance_cost = 0
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT id, year FROM vehicles"""
        purchase_year_data, columns = my_sql_operations.fetch_data(query) 
        purchase_year_df = pd.DataFrame(purchase_year_data, columns=columns)
        
        query = f"""SELECT end_of_year, insurance_cost_percent FROM cost_profiles"""
        insurance_cost_data, columns = my_sql_operations.fetch_data(query)
        insurance_cost_df = pd.DataFrame(insurance_cost_data, columns=columns)

        eoy_df = pd.merge(fleet_details, purchase_year_df, left_on=['id'], right_on=['id'], how='left')

        eoy_df['End_of_year'] = (
            eoy_df['Operating Year'] - eoy_df['year'] + 1
        )
        
        merged_df = pd.merge(eoy_df, insurance_cost_df, left_on='End_of_year', right_on='end_of_year', how='left')
        
        merged_df['insurance_cost'] = (
            ((merged_df['insurance_cost_percent']/100) * merged_df['cost']) 
        )
        return merged_df['insurance_cost']
            
    def yearly_maintenance_cost_per_vehicle(self, fleet_details: pd.DataFrame):
            """
            Returns Maintenance cost for the operating year for one vehicle
            """
            total_fleet_maintainance_cost = 0
            my_sql_operations = MySQLOperations() 
            
            query = f"""SELECT id, year FROM vehicles"""
            purchase_year_data, columns = my_sql_operations.fetch_data(query) 
            purchase_year_df = pd.DataFrame(purchase_year_data, columns=columns)
            
            query = f"""SELECT end_of_year, maintenance_cost_percent FROM cost_profiles"""
            maintenance_cost_data, columns = my_sql_operations.fetch_data(query)
            maintenance_cost_df = pd.DataFrame(maintenance_cost_data, columns=columns)
            eoy_df = pd.merge(fleet_details, purchase_year_df, left_on=['id'], right_on=['id'], how='left')
                    
            eoy_df['End_of_year'] = (
                eoy_df['Operating Year'] - eoy_df['year'] + 1
            )
            
            merged_df = pd.merge(eoy_df, maintenance_cost_df, left_on='End_of_year', right_on='end_of_year', how='left')
            
            merged_df['maintenance_cost'] = (
                ((merged_df['maintenance_cost_percent']/100) * merged_df['cost'])
            )
            return merged_df['maintenance_cost']
          
    def per_km_fuel_cost_per_vehicle(self, fleet_details: pd.DataFrame, op_year: int):
            """
            Returns per km fuel cost for a vehicle
            """
            yearly_fuel_cost = 0
            my_sql_operations = MySQLOperations() 
            
            query = f"""SELECT fuel, cost_per_unit_fuel FROM fuels WHERE year = {op_year}"""
            fuel_cost_data, columns = my_sql_operations.fetch_data(query) 
            fuel_cost_df = pd.DataFrame(fuel_cost_data, columns=columns)
            
            query = f"""SELECT * FROM vehicles_fuels"""
            fuel_consumption_data, columns = my_sql_operations.fetch_data(query)
            fuel_consumption_df = pd.DataFrame(fuel_consumption_data, columns=columns)
            
            merged_df = pd.merge(fleet_details, fuel_cost_df, left_on='fuel', right_on='fuel', how='left')
            merged_df['fuel_costs_per_km'] = (
                merged_df['consumption_unitfuel_per_km'] *
                merged_df['cost_per_unit_fuel']
            )
            return merged_df['fuel_costs_per_km']
    
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
        
        df['carbon_emissions_per_km'] = self.per_km_carbon_emmissions_per_vehicle(df, year)
        
        df['insurance_cost'] = self.yearly_insurance_cost_per_vehicle(df)
        df['maintenance_cost'] = self.yearly_maintenance_cost_per_vehicle(df)
        df['fuel_costs_per_km'] = self.per_km_fuel_cost_per_vehicle(df, year)
        df['Operating_Cost'] = df['insurance_cost'] + df['maintenance_cost'] + (df['fuel_costs_per_km'] * df['Yearly range (km)'])
        
        return df