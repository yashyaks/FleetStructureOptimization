from utilities.my_sql_operations import MySQLOperations
from utilities.costs import Costs
import pandas as pd

class CarbonEmissions:
    def __init__(self):
        self.my_sql_operations = MySQLOperations().fetch_data
    def carbon_emissions_limit(self, op_year: int):
        """
        Calculates carbon emissions limit
        """
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        query = f"""SELECT carbon_emission FROM carbon_emissions WHERE YEAR = {op_year}"""
        cursor.execute(query)
        carbon_emission_limit = cursor.fetchall()
        return carbon_emission_limit[0][0]
    
    def total_carbon_emmissions(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Calculates total carbon emissions
        """
        costs = Costs()  
        emissions_dict = {}
        total_emissions = 0
        for i in range(len(fleet_details)):
            emissions_from_vehicle = 0
            current_vehicle_details = fleet_details.iloc[i]
            fuel_profile = costs.fuel_profile(current_vehicle_details, op_year)
            vehicle_fuel_consumption = costs.vehicle_fuel_consumption(current_vehicle_details) 
            # print(f"\n{current_vehicle_details['ID']}")     
            emissions_from_vehicle = current_vehicle_details[6]*current_vehicle_details[2]*vehicle_fuel_consumption[2]*fuel_profile[2]
            # print(emissions_from_vehicle,current_vehicle_details[6],current_vehicle_details[2],vehicle_fuel_consumption[2],fuel_profile[2])
            emissions_dict[current_vehicle_details['ID']] = float(emissions_from_vehicle)
            total_emissions += emissions_from_vehicle
        emissions_dict['TOTAL'] = float(total_emissions)
        return emissions_dict
    
    def total_carbon_emmissions_JOIN(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Calculates total carbon emissions USING JOINS
        """     
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT * FROM fuels WHERE year = {op_year}"""
        fuel_data, columns = my_sql_operations.fetch_data(query) 
        fuel_df = pd.DataFrame(fuel_data, columns=columns)
        
        query = f"""SELECT * FROM vehicles_fuels"""
        vehicles_fuels_data, columns = my_sql_operations.fetch_data(query)
        vehicles_fuels_df = pd.DataFrame(vehicles_fuels_data, columns=columns)

        merged_df = pd.merge(
            pd.merge(fleet_details, fuel_df, left_on='Fuel', right_on='fuel', how='left'),
            vehicles_fuels_df, left_on=['ID', 'Fuel'], right_on=['id', 'fuel'], how='left'
        )
        
        merged_df['carbon_emissions'] = (
            merged_df['Distance_per_vehicle(km)'] * 
            merged_df['Num_Vehicles'] * 
            merged_df['emissions_co2_per_unit_fuel'] *
            merged_df['consumption_unitfuel_per_km']
        )
        total_emissions = merged_df['carbon_emissions'].sum()
        
        emissions_dict = merged_df.set_index('ID')['carbon_emissions'].to_dict()
        emissions_dict['TOTAL'] = float(total_emissions)
        
        return emissions_dict

