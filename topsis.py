import numpy as np
import pandas as pd


class Topsis:
    def __init__(self):
        pass
    
    def topsis_algo(self, df, criteria_columns, weights, impacts):
        
        # Create a copy of the dataframe
        data = df.copy()
        
        # Normalize the decision matrix
        normalized_matrix = data[criteria_columns].copy()
        for col in criteria_columns:
            # Normalize using vector normalization
            normalized_matrix[col] = normalized_matrix[col] / np.sqrt((normalized_matrix[col]**2).sum())
        
        # Apply weights
        weighted_matrix = normalized_matrix.copy()
        for i, col in enumerate(criteria_columns):
            weighted_matrix[col] *= weights[i]
        
        # Determine ideal best and worst solutions
        ideal_best = []
        ideal_worst = []
        for i, col in enumerate(criteria_columns):
            if impacts[i] == '+':
                ideal_best.append(weighted_matrix[col].max())
                ideal_worst.append(weighted_matrix[col].min())
            else:
                ideal_best.append(weighted_matrix[col].min())
                ideal_worst.append(weighted_matrix[col].max())

        # Calculate distances to ideal best and worst solutions
        distance_best = np.sqrt(((weighted_matrix[criteria_columns] - ideal_best)**2).sum(axis=1))
        distance_worst = np.sqrt(((weighted_matrix[criteria_columns] - ideal_worst)**2).sum(axis=1))
        
        # Calculate TOPSIS score
        data['Topsis_Score'] = distance_worst / (distance_best + distance_worst)
        
        # Rank the alternatives
        data['Rank'] = data['Topsis_Score'].rank(method='dense', ascending=True)
        
        return data
    
    def apply_topsis(self, year, df):
        # if df == None:             
        #     df = pd.read_csv(f'data/output/allocation_output_{year}.csv', index_col=False)
        df.reset_index(drop=True, inplace=True)
        
        # Get unique combinations of Size and Distance_x
        combinations = df.groupby(['Size', 'Distance_demand'])

        # Store results
        results = []

        # Perform TOPSIS for each combination
        for (size, distance), group in combinations:
            # Define criteria columns
            criteria_columns = ['carbon_emissions_per_km','Operating_Cost', 'Cost ($)']
            
            # Define weights (equal weights in this case)
            weights = [0.5, 0.5, 0.5]
            
            # Define impact directions (both to be minimized)
            impacts = ['-', '-', '-']
            
            # Perform TOPSIS
            result = self.topsis_algo(group, criteria_columns, weights, impacts)
            
            # Add size and distance info to results
            result['Size'] = size
            result['Distance'] = distance
            
            results.append(result)

        # Combine all results
        final_results = pd.concat(results)
        

        return final_results
    