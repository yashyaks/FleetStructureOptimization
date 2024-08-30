import pandas as pd
from utilities.carbon_emmissions import CarbonEmissions

def main(path):
    carbon_emissions = CarbonEmissions()
    df = pd.read_csv(path)
    total_emissions = carbon_emissions.total_carbon_emmissions(df, 2025)
    print(total_emissions)
    
    
if __name__ == "__main__":
    path = 'sample_opyear_2025.csv'
    main(path)