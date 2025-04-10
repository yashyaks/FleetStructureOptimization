import pandas as pd

def generate_buy_sell_use_plan(df):
    df_aggregated = df.groupby(["Operating Year", "id"]) ["No_of_vehicles"].sum().reset_index()
    df_aggregated = df_aggregated.sort_values(by=["Operating Year"])
    previous_year_counts = {}
    buy_sell_use_plan = []
    
    for _, row in df_aggregated.iterrows():
        year = row["Operating Year"]
        vehicle_id = row["id"]
        required_vehicles = row["No_of_vehicles"]
        prev_count = previous_year_counts.get(vehicle_id, 0)
        
        if required_vehicles > prev_count:
            use = prev_count
            buy = required_vehicles - prev_count
            sell = 0
        elif required_vehicles < prev_count:
            use = required_vehicles
            sell = prev_count - required_vehicles
            buy = 0
        else:
            use = required_vehicles
            buy = sell = 0
        
        buy_sell_use_plan.append({
            "Operating Year": year,
            "Vehicle ID": vehicle_id,
            "Use": use,
            "Buy": buy,
            "Sell": sell
        })
        
        previous_year_counts[vehicle_id] = required_vehicles
        
    
    return pd.DataFrame(buy_sell_use_plan)
