from utilities.my_sql_operations import MySQLOperations
from utilities.calculations import formulas
import pandas as pd

class CarbonEmissions:
    def __init__(self):
        pass
    def carbon_emissions_limit(self, op_year: int):
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        query = f"""SELECT carbon_emission FROM carbon_emissions WHERE YEAR = {op_year}"""
        print('\nquery run on fucntion call carbon_emissions_limits: ', query)
        cursor.execute(query)
        carbon_emission_limit = cursor.fetchall()
        return carbon_emission_limit[0][0]
    
    def total_carbon_emmissions(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Calculates total carbon emissions
        Args:
            current_fleet_details (DataFrame): list of details of vehicles
            op_year (int): operating year
        """
        formula = formulas()  
        total_emissions = 0
        for i in range(len(fleet_details)):
            emissions_from_vehicle = 0
            current_vehicle_details = fleet_details.iloc[i]
            print('\nVehicle ID: ', current_vehicle_details['ID'])
            fuel_profile = formula.fuel_profile(current_vehicle_details, op_year)
            vehicle_fuel_consumption = formula.vehicle_fuel_consumption(current_vehicle_details)            
            emissions_from_vehicle = current_vehicle_details[6]*current_vehicle_details[2]*vehicle_fuel_consumption[2]*fuel_profile[2]
            total_emissions += emissions_from_vehicle
        return total_emissions