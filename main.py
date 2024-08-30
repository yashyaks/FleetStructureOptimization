import pandas as pd
import pprint
from utilities.carbon_emmissions import CarbonEmissions

def main(path):
    carbon_emissions = CarbonEmissions()
    df = pd.read_csv(path)
    emissions_dict = carbon_emissions.total_carbon_emmissions(df, 2025)
    pprint.pprint(emissions_dict)
    carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(2025)
    print(f"Carbon Emissions Limit for the given year: {carbon_emissions_limit}")
    
if __name__ == "__main__":
    path = 'sample_opyear_2025.csv'
    main(path)