from utilities.my_sql_operations import MySQLOperations

class formulas:
    def __init__(self):
        pass
    
    def vehciles_that_can_be_purchased_in_year(self, year: int):
        """
        Returns the details of every vehicle available for purchase in a given year
        Args:
            year (int): year of interest
        Returns:
            vehicle_details (list): list of details of vehicles
        """
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        query = f"""SELECT * FROM vehicles WHERE year = {year}"""
        print('\nquery run on fucntion call vehciles_purchased_in_year: ', query)
        cursor.execute(query)
        vehicle_details = cursor.fetchall()
        return vehicle_details
    
    def cost_of_buying_vehicles_in_year(self, vehicle_details: list, units_purchased: list):
        """
        Returns the cost of buying vehicles in a given year
        Args:
            vehicle_details (list): list of details of vehicles
            units_purchased (list): list containing the IDs and the number of units purchased
        Returns:
            purchase_summary (dict): cost of buying vehicles in a given year
        """
        purchase_summary = {}
        total_cost = 0
        count = 0
        for i in range(len(units_purchased)):
            for j in range(len(vehicle_details)):
                if units_purchased[i][0] == vehicle_details[j][0]:
                    cost = 0
                    cost = units_purchased[i][1]*vehicle_details[j][4]
                    purchase_summary[count] = [units_purchased[i][1], vehicle_details[j][0], cost]
                    total_cost += cost
                    count += 1
        purchase_summary['total'] = total_cost
        return purchase_summary


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
        Extracts fuel profile for the vehicle
        Args:
            current_vehicle_details (tuple): list of details of vehicles
                (ID, vehicle, size_bucket, year_of_purchase, cost, yearly_range, distance_bucket, number_of_vehicles, distance_per_vehicle, fuel, cosumption_unitfuel_per_km)
            op_year (int): operating year
        Returns:
            fuel_profile (list): list of fuel profile information
        """
        connection = MySQLOperations().create_connection('fleet-data')
        cursor = connection.cursor()
        print(current_vehicle_details)
        query = f""" SELECT * FROM fuels WHERE YEAR = {op_year} AND FUEL = '{current_vehicle_details[9]}' """
        print('\nquery run on fucntion call fuel_profile: ', query)
        cursor.execute(query)
        fuel_profile = cursor.fetchall()
        return fuel_profile[0]
        
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
        handle this constraint: Distance_per_vehicle(km) Should > 0 and <= Yearly range of that
model.
        """
        yearly_fuel_cost = 0
        for i in range(len(current_fleet_details)):
            current_vehicle_details = current_fleet_details[i]
            total_yearly_vehicle_fuel_cost = 0
            fuel_profile = self.fuel_profile(current_vehicle_details, op_year)
            total_yearly_vehicle_fuel_cost = current_vehicle_details[8]*current_vehicle_details[10]*fuel_profile[3]*current_vehicle_details[7]
            yearly_fuel_cost += total_yearly_vehicle_fuel_cost
            
            return yearly_fuel_cost
        
    def recievables_from_sale_of_vehicle(self, fleet_for_resale: list, op_year: int):
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
    
    def total_fleet_cost_for_current_op_year(self, vehicle_details:list, units_purchased: list, current_fleet_details: list, fleet_for_resale: list,op_year: int):
        """
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