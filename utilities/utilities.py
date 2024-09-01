from utilities.my_sql_operations import MySQLOperations

class Utilities:
    def __init__(self):
        pass
    
    def cost_profiles(self, year_of_purchase: int, op_year: int):
        """
        Returns cost profile (resale, insurance, maintenance) for the age of the vehicle
        Args:
            op_year (int): operating year
        Returns:
            cost_profile (list): list of cost profile information
        """
        connection = MySQLOperations().create_connection('fleet-data')
        end_of_year = op_year - year_of_purchase
        cursor = connection.cursor()
        query = f"""SELECT * FROM cost_profiles WHERE end_of_year = {end_of_year}"""
        print('\nquery run on fucntion call cost_profiles: ', query)
        cursor.execute(query)
        cost_profile = cursor.fetchall()
        return cost_profile[0]
    
    def fuel_profile(self, current_vehicle_details: tuple, op_year: int):
        """
        Extracts fuel profile for the vehicle
        """
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        query = f""" SELECT * FROM fuels WHERE YEAR = {op_year} AND FUEL = '{current_vehicle_details.iloc[4]}' """
        cursor.execute(query)
        fuel_profile = cursor.fetchall()
        return fuel_profile[0]
    
    def vehicle_fuel_consumption(self, current_vehicle_details: tuple):
        """
        MOVE TO A UTILITY CLASS
        Extracts consumption_unitfuel_per_km from vehicles_fuels
        """
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        query = f""" SELECT * FROM vehicles_fuels WHERE ID = '{current_vehicle_details.iloc[1]}' """
        cursor.execute(query)
        fuel_consumption_profile = cursor.fetchall()
        return fuel_consumption_profile[0]
        