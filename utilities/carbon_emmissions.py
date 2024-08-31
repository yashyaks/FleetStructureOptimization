from utilities.my_sql_operations import MySQLOperations
from utilities.costs import Costs
import pandas as pd

class CarbonEmissions:
    def __init__(self):
        pass
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