from utilities.my_sql_operations import MySQLOperations
import pandas as pd
"""
ALL INPUT NEEDS TO COME FROM CSV
"""
class Costs:
    def __init__(self):
        pass
    
    def buy_costs(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Returns the cost of buying vehicles in a given year
        """
        purchase_summary = {}
        vehciles_to_buy = fleet_details[fleet_details['Type'] == 'Buy']
        
        my_sql_operations = MySQLOperations() 
        query = f"""SELECT id, cost FROM vehicles WHERE year = {op_year}"""
        vehicle_costs, columns = my_sql_operations.fetch_data(query) 
        vehicle_costs_df = pd.DataFrame(vehicle_costs, columns=columns)
        merged_df = pd.merge(vehciles_to_buy, vehicle_costs_df, left_on='ID', right_on='id', how='left')
        merged_df['line_item_cost'] = (
            merged_df['cost'] * 
            merged_df['Num_Vehicles']
        )
        total_cost = merged_df['line_item_cost'].sum()
        
        purchase_summary = merged_df.set_index('ID')['line_item_cost'].to_dict()
        purchase_summary['TOTAL'] = float(total_cost)
        
        return purchase_summary

    def cost_profiles(self, year_of_purchase: int, op_year: int):
        """
        MOVE TO A UTILITY CLASS
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
    
    def yearly_insurance_cost(self, current_fleet_details: list, op_year: int):
        """
        Returns Insurance cost for the operating year
        Args:
            current_fleet_details (list): list of details of vehicles
                (ID, vehicle, size_bucket, year_of_purchase, cost, yearly_range, distance_bucket, number_of_vehicles, distance_per_vehicle, fuel, cosumption_unitfuel_per_km)
            op_year (int): operating year
        Returns:
            yearly_insurance_cost (int): yearly insurance cost
        """
        total_fleet_insurance_cost = 0
        for i in range(len(current_fleet_details)):
            cost_profile = self.cost_profiles(current_fleet_details[i][3], op_year)
            insurance_percent = cost_profile[2]
            print('insurance_details: ', current_fleet_details[i], insurance_percent )
            insurance_cost = current_fleet_details[i][4]*insurance_percent*current_fleet_details[i][7]
            total_fleet_insurance_cost += insurance_cost
        return total_fleet_insurance_cost
    
    def yearly_maintenance_cost(self, current_fleet_details: list, op_year: int):
        """
        Returns Maintenance cost for the operating year
        Args:
            current_fleet_details (list): list of details of vehicles
                (ID, vehicle, size_bucket, year_of_purchase, cost, yearly_range, distance_bucket, number_of_vehicles, distance_per_vehicle, fuel, cosumption_unitfuel_per_km)
            op_year (int): operating year
        Returns:
            yearly_maintenance_cost (int): yearly maintenance cost
        """
        total_fleet_maintenance_cost = 0
        for i in range(len(current_fleet_details)):
            cost_profile = self.cost_profiles(current_fleet_details[i][3], op_year)
            maintenance_percent = cost_profile[3]
            print('maintenance_details: ', current_fleet_details[i], maintenance_percent )
            maintenance_cost = current_fleet_details[i][4]*maintenance_percent*current_fleet_details[i][7]
            total_fleet_maintenance_cost += maintenance_cost
        return total_fleet_maintenance_cost
            
    def fuel_profile(self, current_vehicle_details: tuple, op_year: int):
        """
        MOVE TO A UTILITY CLASS
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
        
    def yearly_fuel_cost(self, current_fleet_details: list, op_year: int):
        """
        Returns yearly fuel cost
        Args:
            current_fleet_details (list): list of details of vehicles
                (ID, vehicle, size_bucket, year_of_purchase, cost, yearly_range, distance_bucket, number_of_vehicles, distance_per_vehicle, fuel, cosumption_unitfuel_per_km)
            op_year (int): operating year
        Returns:
            yearly_fuel_cost (int): yearly fuel cost
        """
        """
        handle this constraint: Distance_per_vehicle(km) Should > 0 and <= Yearly range of that model.
        """
        yearly_fuel_cost = 0
        for i in range(len(current_fleet_details)):
            current_vehicle_details = current_fleet_details[i]
            total_yearly_vehicle_fuel_cost = 0
            fuel_profile = self.fuel_profile(current_vehicle_details, op_year)
            total_yearly_vehicle_fuel_cost = current_vehicle_details[8]*current_vehicle_details[10]*fuel_profile[3]*current_vehicle_details[7]
            yearly_fuel_cost += total_yearly_vehicle_fuel_cost
            
            return yearly_fuel_cost
        
    def sell_costs(self, fleet_for_resale: list, op_year: int):
        """
        Returns total recievables from sale of vehicles
        Args:
            fleet_for_resale (list): list of details of vehicles
            (ID, vehicle, year_of_purchase, cost, number_of_vehicles)
            op_year (int): operating year
        Returns:
            recievables (int): total recievables from sale of vehicles
        """
        total_recievables = 0
        for i in range(len(fleet_for_resale)):
            recievables = 0
            current_vehicle_details = fleet_for_resale[i]
            cost_profile = self.cost_profiles(current_vehicle_details[2], op_year)
            recievables = current_vehicle_details[3]*(cost_profile[1]/100)*current_vehicle_details[4]
            total_recievables += recievables
        return recievables
    
    def total_fleet_cost(self, vehicle_details:list, units_purchased: list, current_fleet_details: list, fleet_for_resale: list,op_year: int):
        """
        RETURN A DICTIONARY RETURNING ALL DETAILS
        Returns total cost of operating the fleet
        Args:
            vehicle_details (list): list of details of vehicles
            units_purchased (list): list containing the IDs and the number of units purchased
            current_fleet_details (list): list of details of vehicles
            fleet_for_resale (list): list of details of vehicles
        """
        total_cost = 0
        purchase_summary = self.cost_of_buying_vehicles_in_year(vehicle_details, units_purchased)
        total_cost += purchase_summary['total']
        total_cost += self.yearly_fuel_cost(current_fleet_details, op_year)
        total_cost += self.yearly_maintenance_cost(current_fleet_details, op_year)
        total_cost += self.yearly_insurance_cost(current_fleet_details, op_year)
        total_cost -= self.recievables_from_sale_of_vehicle(fleet_for_resale, op_year)
        return total_cost