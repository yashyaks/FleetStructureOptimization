from utilities.my_sql_operations import MySQLOperations

class formulas:
    def __init__(self):
        pass
    
    def vehciles_purchased_in_year(self, year):
        """
        Returns the details of every vehicle available for purchase in a given year
        Args:
            year (int): year of interest
        Returns:
            vehicle_details (list): list of details of vehicles
        """
        connection = MySQLOperations().create_connection('fleet_data')
        cursor = connection.cursor()
        query = f"""SELECT * FROM vehicles WHERE year = {year}"""
        print('query run on fucntion call vehciles_purchased_in_year: ', query)
        cursor.execute(query)
        vehicle_details = cursor.fetchall()
        return vehicle_details
    
    def cost_of_buying_vehicles_in_year(self, vehicle_details, units_purchased):
        """
        Returns the cost of buying vehicles in a given year
        Args:
            connection: connection object to the specified MySQL database.
            vehicle_details (list): list of details of vehicles
            units_purchased (list): list containing the IDs and the number of units purchased
        Returns:
            purchase_summary (dict): cost of buying vehicles in a given year
        """
        purchase_summary = {}
        total_cost = 0
        count = 0
        for i in range(len(vehicle_details)):
            for j in range(len(units_purchased)):
                if vehicle_details[i][0] == units_purchased[j][0]:
                    cost = 0
                    cost = vehicle_details[i][4]*units_purchased[j][1]
                    purchase_summary[count] = [vehicle_details[i][0], units_purchased[j][1], cost]
                    total_cost += cost
                    count += 1
        purchase_summary['total'] = total_cost
        return purchase_summary