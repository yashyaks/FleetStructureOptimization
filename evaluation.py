import pandas as pd
class Evaluation:
    def __init__(self):
        pass

    def calculate_utilization(self, df):
        combinations = df.groupby(['Size', 'Distance_demand'])
        scores = []

        for (size, distance), group in combinations:
            total_vehicles = group['No_of_vehicles'].sum()
            for _, row in group.iterrows():
                score = (row['Demand (km)'] / total_vehicles) / row['Yearly range (km)'] * 100
                scores.append(score)

        df['Utilization (%)'] = scores
        return df

    def calculate_demand_fulfillment(self, num_vehicles: int, max_vehicles: int) -> float:
        """Calculate demand fulfillment by fuel type"""
        if max_vehicles == 0:
            return 0
        return num_vehicles / max_vehicles
    
    def apply_metrics_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply utilization and demand fulfillment to DataFrame"""
        df = self.calculate_utilization(df)
        df['DemandFulfillment'] = df.apply(lambda row: self.calculate_demand_fulfillment(row['No_of_vehicles'], row['Max Vehicles']), axis=1)
        
        return df