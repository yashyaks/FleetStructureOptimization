import pandas as pd
import pprint
from utilities.carbon_emmissions import CarbonEmissions
from utilities.costs import Costs
import time

def main(path):
    df = pd.read_csv(path)
    op_year = 2025

    ### Carbon Emissions Calculations ###
    carbon_emissions = CarbonEmissions()
    
    carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(op_year)
    print(f"Carbon Emissions Limit for the given year: {carbon_emissions_limit}")
    
    emissions_dict = carbon_emissions.total_carbon_emmissions(df, op_year)
    print("Emissions Details: ")
    pprint.pprint(emissions_dict)
        
    ### Costs Calculations ###
    costs = Costs()
    
    purchase_summary = costs.buy_costs(df, op_year)
    print("Purchase Summary: ")
    pprint.pprint(purchase_summary)
    
    yearly_insurance_cost_dict = costs.yearly_insurance_cost(df)
    print("Yearly Insurance Cost: ")
    pprint.pprint(yearly_insurance_cost_dict)
    
    yearly_maintenance_cost_dict = costs.yearly_maintenance_cost(df)
    print("Yearly Maintenance Cost: ")
    pprint.pprint(yearly_maintenance_cost_dict)
    
    yearly_fuel_cost_dict = costs.yearly_fuel_cost(df, op_year)
    print("Yearly Fuel Cost: ")
    pprint.pprint(yearly_fuel_cost_dict)
    
    resale_summary = costs.recievables_from_resale(df, op_year)
    print("Resale Summary: ")
    pprint.pprint(resale_summary)
    
    total_fleet_summary = costs.total_fleet_cost(df, op_year)
    print("Total Fleet Summary: ")
    pprint.pprint(total_fleet_summary)
    
if __name__ == "__main__":
    # start_time = time.time()
    path = 'sample_opyear_2025.csv'
    main(path)
    # end_time = time.time()
    # print("Total time taken: ", end_time - start_time)