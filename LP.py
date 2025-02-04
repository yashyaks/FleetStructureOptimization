import pandas as pd
from ortools.linear_solver import pywraplp

# Load dataset
df = pd.read_csv("data/something_new_new.csv")

# Extract relevant columns
vehicle_types = df['Vehicle'].unique()
costs = dict(zip(df['ID'], df['Cost ($)']))
insurances = dict(zip(df['ID'], df['insurance_cost']))
maintenances = dict(zip(df['ID'], df['maintenance_cost']))
fuels = dict(zip(df['ID'], df['fuel_costs']))
carbon_emissions = dict(zip(df['ID'], df['carbon_emissions']))
demands = df.groupby('Vehicle').size().to_dict()
types = dict(zip(df['ID'], df['Type']))
years = dict(zip(df['ID'], df['Operating Year']))  # Assuming the column is 'Year' for vehicle year

# Define thresholds
carbon_threshold = 11677957  # Total carbon emissions for 2023 shouldn't exceed this value

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define variables
vehicle_vars = {vehicle: solver.IntVar(0, solver.infinity(), vehicle) for vehicle in df['ID'].unique()}

# Constraints
# Carbon emissions constraint for vehicles in the year 2023
solver.Add(solver.Sum(vehicle_vars[v] * carbon_emissions[v] for v in vehicle_vars if years[v] == 2023) <= carbon_threshold)

# Meet demand for each vehicle type
for v_type in vehicle_types:
    solver.Add(solver.Sum(vehicle_vars[v] for v in df[df['Vehicle'] == v_type]['ID']) >= demands[v_type])

# Objective: Minimize cost considering adjustments for 'Sell' type
total_cost = solver.Sum(
    vehicle_vars[v] * (insurances[v] + maintenances[v] + fuels[v] + costs[v]) 
    if types[v] != 'Sell' 
    else vehicle_vars[v] * (insurances[v] + maintenances[v] + fuels[v] + costs[v] - costs[v])  # Subtract cost for 'Sell' vehicles
    for v in vehicle_vars
)

solver.Minimize(total_cost)

# Solve
status = solver.Solve()

# Print results
if status == pywraplp.Solver.OPTIMAL:
    print("Optimal solution found!")
    for v in vehicle_vars:
        print(f"{v}: {vehicle_vars[v].solution_value()}")
    print(f"Total Cost: {solver.Objective().Value()}")
else:
    print("No optimal solution found.")
