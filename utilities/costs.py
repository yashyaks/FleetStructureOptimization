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
 
    def yearly_insurance_cost(self, fleet_details: pd.DataFrame):
        """
        Returns Insurance cost for the operating year
        """
        total_fleet_insurance_cost = 0
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT id, year, cost FROM vehicles"""
        purchase_year_data, columns = my_sql_operations.fetch_data(query) 
        purchase_year_df = pd.DataFrame(purchase_year_data, columns=columns)
        
        query = f"""SELECT end_of_year, insurance_cost_percent FROM cost_profiles"""
        insurance_cost_data, columns = my_sql_operations.fetch_data(query)
        insurance_cost_df = pd.DataFrame(insurance_cost_data, columns=columns)
        
        eoy_df = pd.merge(fleet_details, purchase_year_df, left_on=['ID'], right_on=['id'], how='left')
                
        eoy_df['End_of_year'] = (
            eoy_df['Operating Year'] - eoy_df['year'] + 1
        )
        
        merged_df = pd.merge(eoy_df, insurance_cost_df, left_on='End_of_year', right_on='end_of_year', how='left')
        
        merged_df['insurance_cost'] = (
            ((merged_df['insurance_cost_percent']/100) * merged_df['cost']) * merged_df['Num_Vehicles'] 
        )
        total_fleet_insurance_cost = merged_df['insurance_cost'].sum()
        
        yearly_insurance_cost_dict = merged_df.set_index('ID')['insurance_cost'].to_dict()
        yearly_insurance_cost_dict['TOTAL'] = float(total_fleet_insurance_cost)
        
        return yearly_insurance_cost_dict
            
    def yearly_maintenance_cost(self, fleet_details: pd.DataFrame):
        """
        Returns Maintenance cost for the operating year
        """
        total_fleet_maintainance_cost = 0
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT id, year, cost FROM vehicles"""
        purchase_year_data, columns = my_sql_operations.fetch_data(query) 
        purchase_year_df = pd.DataFrame(purchase_year_data, columns=columns)
        
        query = f"""SELECT end_of_year, maintenance_cost_percent FROM cost_profiles"""
        maintenance_cost_data, columns = my_sql_operations.fetch_data(query)
        maintenance_cost_df = pd.DataFrame(maintenance_cost_data, columns=columns)
        
        eoy_df = pd.merge(fleet_details, purchase_year_df, left_on=['ID'], right_on=['id'], how='left')
                
        eoy_df['End_of_year'] = (
            eoy_df['Operating Year'] - eoy_df['year'] + 1
        )
        
        merged_df = pd.merge(eoy_df, maintenance_cost_df, left_on='End_of_year', right_on='end_of_year', how='left')
        
        merged_df['maintenance_cost'] = (
            ((merged_df['maintenance_cost_percent']/100) * merged_df['cost']) * merged_df['Num_Vehicles'] 
        )
        total_fleet_maintainance_cost = merged_df['maintenance_cost'].sum()

        yearly_maintainance_cost_dict = merged_df.set_index('ID')['maintenance_cost'].to_dict()
        yearly_maintainance_cost_dict['TOTAL'] = float(total_fleet_maintainance_cost)
        
        return yearly_maintainance_cost_dict
          
    def yearly_fuel_cost(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Returns yearly fuel cost
        """
        yearly_fuel_cost = 0
        my_sql_operations = MySQLOperations() 
        
        query = f"""SELECT fuel, cost_per_unit_fuel FROM fuels WHERE year = {op_year}"""
        fuel_cost_data, columns = my_sql_operations.fetch_data(query) 
        fuel_cost_df = pd.DataFrame(fuel_cost_data, columns=columns)
        
        query = f"""SELECT * FROM vehicles_fuels"""
        fuel_consumption_data, columns = my_sql_operations.fetch_data(query)
        fuel_consumption_df = pd.DataFrame(fuel_consumption_data, columns=columns)
        
        merged_df = pd.merge(
            pd.merge(fleet_details, fuel_cost_df, left_on='Fuel', right_on='fuel', how='left'),
            fuel_consumption_df, left_on=['ID', 'Fuel'], right_on=['id', 'fuel'], how='left'
        )
        
        merged_df['fuel_costs'] = (
            merged_df['Distance_per_vehicle(km)'] * 
            merged_df['Num_Vehicles'] * 
            merged_df['consumption_unitfuel_per_km'] *
            merged_df['cost_per_unit_fuel']
        )
        yearly_fuel_cost = merged_df['fuel_costs'].sum()
        
        yearly_fuel_cost_dict = merged_df.set_index('ID')['fuel_costs'].to_dict()
        yearly_fuel_cost_dict['TOTAL'] = float(yearly_fuel_cost)
        
        return yearly_fuel_cost_dict
        
    def recievables_from_resale(self, fleet_details: pd.DataFrame, op_year: int):
        """
        Returns total recievables from resale of vehicles
        """
        vehicles_to_buy = fleet_details[fleet_details['Type'] == 'Sell']
        
        my_sql_operations = MySQLOperations() 
        query = f"""SELECT id, year, cost FROM vehicles WHERE year <= {op_year}"""
        vehicle_costs, columns = my_sql_operations.fetch_data(query) 
        vehicle_costs_df = pd.DataFrame(vehicle_costs, columns=columns)
        
        query = f"""SELECT end_of_year, resale_value_percent FROM cost_profiles"""
        resale_value_data, columns = my_sql_operations.fetch_data(query)
        resale_value_df = pd.DataFrame(resale_value_data, columns=columns)

        eoy_df = pd.merge(vehicles_to_buy, vehicle_costs_df, left_on='ID', right_on='id', how='left')
                
        eoy_df['End_of_year'] = (
            eoy_df['Operating Year'] - eoy_df['year'] + 1
        )
        
        merged_df = pd.merge(eoy_df, resale_value_df, left_on='End_of_year', right_on='end_of_year', how='left')
        
        merged_df['line_item_value'] = (
            ((merged_df['resale_value_percent']/100) * merged_df['cost']) * merged_df['Num_Vehicles']
        )
        
        total_value = merged_df['line_item_value'].sum()
        
        resale_summary = merged_df.set_index('ID')['line_item_value'].to_dict()
        resale_summary['TOTAL'] = float(total_value)
        
        return resale_summary
        
    def total_fleet_cost(self, fleet_Details:pd.DataFrame,op_year: int):
        """
        Returns a Dictionary of all details
        """
        net_expenditure = 0
        total_fleet_summary = {}
        purchase_summary = self.buy_costs(fleet_Details, op_year)
        yearly_insurance_cost_dict = self.yearly_insurance_cost(fleet_Details)
        yearly_maintenance_cost_dict = self.yearly_maintenance_cost(fleet_Details)
        yearly_fuel_cost_dict = self.yearly_fuel_cost(fleet_Details, op_year)
        resale_summary = self.recievables_from_resale(fleet_Details, op_year)
        
        total_fleet_summary['Purchase'] = purchase_summary['TOTAL']
        total_fleet_summary['Insurance'] = yearly_insurance_cost_dict['TOTAL']
        total_fleet_summary['Maintenance'] = yearly_maintenance_cost_dict['TOTAL']
        total_fleet_summary['Fuel'] = yearly_fuel_cost_dict['TOTAL']
        total_fleet_summary['Resale'] = resale_summary['TOTAL']
        
        net_expenditure = total_fleet_summary['Purchase'] + total_fleet_summary['Insurance'] + total_fleet_summary['Maintenance'] + total_fleet_summary['Fuel'] - total_fleet_summary['Resale']
        
        total_fleet_summary['Net'] = net_expenditure
        
        return total_fleet_summary