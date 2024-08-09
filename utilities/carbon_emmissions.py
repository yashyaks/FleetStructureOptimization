from utilities.my_sql_operations import MySQLOperations
from utilities.calculations import formulas

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
    
    def total_carbon_emmissions(self, current_fleet_details: list, op_year: int):
        """
        Calculates total carbon emissions
        Args:
            current_fleet_details (list): list of details of vehicles
        """
        formula = formulas()  
        total_emissions = 0
        for i in range(len(current_fleet_details)):
            emissions_from_vehicle = 0
            current_vehicle_details = current_fleet_details[i]
            fuel_profile = formula.fuel_profile(current_vehicle_details, op_year)
            emissions_from_vehicle = current_vehicle_details[8]*current_vehicle_details[10]*fuel_profile[3]*current_vehicle_details[7]
            total_emissions += emissions_from_vehicle
        return total_emissions