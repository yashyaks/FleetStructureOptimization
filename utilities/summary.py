import pandas as pd

class Summary:
    def __init__(self):
        self.summary_df = pd.DataFrame()
    
    def yearly_cost_total(self, df):
        # hehe = df['cost'] + df['maintenance_cost'] + df['insurance_cost'] + (df['fuel_costs_per_km'] * (df['demand'] * df['DemandFulfillment']))
        # hehe = df['cost'] + df['maintenance_cost'] + df['insurance_cost'] + (df['fuel_costs_per_km'] * df['yearly_range'])
        # return round(hehe.sum(), 0)
        hehe = df['cost'] + df['Operating_Cost']
        return round((df['No_of_vehicles'] * hehe).sum(), 0)
        
    def yearly_carbon_emissions_total(self, df):
        return round((df['No_of_vehicles'] * df['carbon_emissions_per_km'] * (df['DemandFulfillment'] * df['demand'])).sum(), 0)
    
    def summarize(self, df, year):
        """Summarize yearly metrics and store in summary DataFrame"""
        total_cost = self.yearly_cost_total(df)
        total_emissions = self.yearly_carbon_emissions_total(df)
        
        year_summary = pd.DataFrame({
            'Year': [year],
            'TotalCost': [total_cost],
            'TotalCarbonEmissions': [total_emissions]
        })
        
        self.summary_df = pd.concat([self.summary_df, year_summary], ignore_index=True)
        
        return self.summary_df