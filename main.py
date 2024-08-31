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
    
    start_time = time.time()
    emissions_dict = carbon_emissions.total_carbon_emmissions(df, op_year)
    # pprint.pprint(emissions_dict)
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"time taken with approach 1: {time_taken}")
    
    start_time = time.time()
    emissions_dict = carbon_emissions.total_carbon_emmissions_JOIN(df, op_year)
    # pprint.pprint(emissions_dict)
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"time taken with approach 2: {time_taken}")
    
    # carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(op_year)
    # print(f"Carbon Emissions Limit for the given year: {carbon_emissions_limit}")
    
    # ### Costs Calculations ###
    # costs = Costs()
    
    
if __name__ == "__main__":
    path = 'sample_opyear_2025.csv'
    main(path)