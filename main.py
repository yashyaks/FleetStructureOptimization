import pandas as pd
import pprint
from utilities.carbon_emmissions import CarbonEmissions
from utilities.costs import Costs

def main(path):
    df = pd.read_csv(path)
    op_year = 2025
    
    ### Carbon Emissions Calculations ###
    carbon_emissions = CarbonEmissions()
    
    carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(op_year)
    print(f"Carbon Emissions Limit for the given year: {carbon_emissions_limit}")
    
    emissions_dict = carbon_emissions.total_carbon_emmissions(df, op_year)
    pprint.pprint(emissions_dict)
        
    ### Costs Calculations ###
    costs = Costs()
    
    
if __name__ == "__main__":
    path = 'sample_opyear_2025.csv'
    main(path)