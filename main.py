import pandas as pd
import pprint
from utilities.carbon_emmissions import CarbonEmissions
from utilities.costs import Costs

def main(path):
    df = pd.read_csv(path)
    op_year = 2025
    
    ### Carbon Emissions Calculations ###
    # carbon_emissions = CarbonEmissions()
    
    # carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(op_year)
    # print(f"Carbon Emissions Limit for the given year: {carbon_emissions_limit}")
    
    # emissions_dict = carbon_emissions.total_carbon_emmissions(df, op_year)
    # pprint.pprint(emissions_dict)
        
    ### Costs Calculations ###
    costs = Costs()
    
    # purchase_summary = costs.buy_costs(df, op_year)
    # pprint.pprint(purchase_summary)
    
    # yearly_insurance_cost_dict = costs.yearly_insurance_cost(df)
    # pprint.pprint(yearly_insurance_cost_dict)
    
    # yearly_maintenance_cost_dict = costs.yearly_maintenance_cost(df)
    # pprint.pprint(yearly_maintenance_cost_dict)
    
    # yearly_fuel_cost_dict = costs.yearly_fuel_cost(df, op_year)
    # pprint.pprint(yearly_fuel_cost_dict)
    
    resale_summary = costs.recievables_from_resale(df, op_year)
    pprint.pprint(resale_summary)
    
if __name__ == "__main__":
    path = 'sample_opyear_2025.csv'
    main(path)