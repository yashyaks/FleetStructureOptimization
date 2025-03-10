import pandas as pd
from scipy.stats import ttest_ind

for year in range(2023, 2024):
    # Load data for each year
    topsis_df = pd.read_csv(f'data/output/tradeoff/topsis/multi_objective_fleet_allocation_eval_{year}.csv')
    no_topsis_df = pd.read_csv(f'data/output/tradeoff/notopsis/multi_objective_fleet_allocation_eval_{year}.csv')
    
    # Group by Size and Distance
    grouped_topsis = topsis_df.groupby(['Size', 'Distance_demand'])
    grouped_no_topsis = no_topsis_df.groupby(['Size', 'Distance_demand'])
        
    topsis_combinations = topsis_df.groupby(['Size', 'Distance_demand'])
    no_topsis_combinations = no_topsis_df.groupby(['Size', 'Distance_demand'])
    
    for (size, distance), topsis_group in topsis_combinations:
        if (size, distance) in no_topsis_combinations.groups:
            no_topsis_group = no_topsis_combinations.get_group((size, distance))
            
            print(
                topsis_group['Total_CE'].sum(),
                no_topsis_group['Total_CE'].sum()
            )
            cost_ttest = ttest_ind(
                topsis_group['Total_Cost'].sum(),
                no_topsis_group['Total_Cost'].sum()
            )
            ce_ttest = ttest_ind(
                topsis_group['Total_CE'].sum(),
                no_topsis_group['Total_CE'].sum()
            )
            
            # Print results
            print(f"Year {year} - Size {size}, Distance {distance}:")
            print("T-test for Cost:", cost_ttest)
            print("T-test for Carbon Emissions:", ce_ttest)
            
            # Interpretation
            if cost_ttest.pvalue < 0.05:
                print("Cost difference is statistically significant.")
            else:
                print("Cost difference is not statistically significant.")
            
            if ce_ttest.pvalue < 0.05:
                print("Carbon Emissions difference is statistically significant.")
            else:
                print("Carbon Emissions difference is not statistically significant.")
            
            print("-" * 50)
    
    