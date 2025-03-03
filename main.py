from demand import VehicleAllocation
from topsis import Topsis
from tradeoff_topsis_copy import MultiObjectiveFleetOptimizer

from pprint import pprint

def main():
    for year in range(2023,2024):
        va = VehicleAllocation()
        tp = Topsis()
        
        df = va.allocate_vehicles(year)
        tp_df = tp.apply_topsis(year, df)
        
        # Rename columns properly
        column_mapping = {
            'Unnamed: 0': 'Index',
            'Allocation' : 'Allocation',
            'Size': 'Size',
            'Distance_demand': 'Distance_demand',
            'Demand (km)': 'Demand',
            'Cost ($)': 'Cost',
            'Yearly range (km)': 'Yearly_Range',
            'insurance_cost': 'Insurance_Cost',
            'maintenance_cost': 'Maintenance_Cost',
            'fuel_costs_per_km': 'Fuel_Costs',
            'Fuel': 'Fuel',
            'Total_Cost': 'Total_Cost',
            'Topsis_Score': 'Topsis_Score',
            'carbon_emission_per_km': 'carbon_emissions_per_km'
        }
        
        tp_df.rename(columns=column_mapping, inplace=True, errors='ignore') 
        
        mo = MultiObjectiveFleetOptimizer(tp_df)
        df = mo.get_optimized_results(year)

if __name__ == "__main__":
    main()
