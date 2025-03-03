class Evaluation:
    def __init__(self):
        pass
    
    def calculate_utilization(self, demand: float, num_vehicles: int, yearly_range: float) -> float:
        """Calculate utilization metric for a vehicle type"""
        if num_vehicles == 0 or yearly_range == 0:
            return 0
        return (demand / num_vehicles) / yearly_range * 100

    def calculate_demand_fulfillment(self, num_vehicles: int, max_vehicles: int) -> float:
        """Calculate demand fulfillment by fuel type"""
        if max_vehicles == 0:
            return 0
        return num_vehicles / max_vehicles
 
    
    
                    # utilization = self.calculate_utilization(
                    #     vehicle_data['demand'],
                    #     num_vehicles,
                    #     vehicle_data['yearly_range']
                    # )

                    # demand_fulfillment = self.calculate_demand_fulfillment(
                    #     num_vehicles,
                    #     max_vehicles
                    # )