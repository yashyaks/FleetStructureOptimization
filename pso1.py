import numpy as np
import pandas as pd

# Load datasets
demand = pd.read_csv('data/demand.csv')
vehicles = pd.read_csv('data/vehicles.csv')
vehicle_fuels = pd.read_csv('data/vehicles_fuels.csv')
fuels = pd.read_csv('data/fuels.csv')
carbon_emissions = pd.read_csv('data/carbon_emissions.csv')

# Constants
NUM_PARTICLES = 50
MAX_ITERATIONS = 100
NUM_YEARS = 16

# PSO Hyperparameters
INERTIA_WEIGHT = 0.7
COGNITIVE_CONSTANT = 1.5
SOCIAL_CONSTANT = 1.5

# Helper Functions
from utilities.costs import Costs
cost_calculator = Costs()

def evaluate_constraints(solution):
    """
    Checks if the solution satisfies all constraints.
    """
    is_feasible = True
    penalty = 0

    for year in range(NUM_YEARS):
        yearly_decisions = solution[year]
        yearly_demand = demand[demand['Year'] == 2023 + year]
        
        # Constraint: Total yearly demand must be met
        for _, row in yearly_demand.iterrows():
            size, distance, demand_km = row['Size'], row['Distance'], row['Demand']
            satisfied_demand = sum(
                decision['Distance_per_vehicle(km)'] * decision['Num_Vehicles']
                for decision in yearly_decisions
                if decision['Type'] == 'Use' and decision['Distance_bucket'] == distance and decision['Size'] == size
            )

            if satisfied_demand < demand_km:
                is_feasible = False
                penalty += (demand_km - satisfied_demand) * 100  # Arbitrary penalty weight

        # Constraint: Total carbon emissions must not exceed the limit
        carbon_limit = carbon_emissions.loc[carbon_emissions['Year'] == 2023 + year, 'Total Carbon emission limit'].values[0]
        total_emissions = sum(
            decision['Distance_per_vehicle(km)'] * decision['Num_Vehicles'] * 
            vehicle_fuels.loc[vehicle_fuels['ID'] == decision['ID'], 'Fuel Consumption (unit_fuel/km)'].values[0] * 
            fuels.loc[fuels['Fuel'] == decision['Fuel'], 'Emissions (CO2/unit_fuel)'].values[0]
            for decision in yearly_decisions if decision['Type'] == 'Use'
        )

        if total_emissions > carbon_limit:
            is_feasible = False
            penalty += (total_emissions - carbon_limit) * 1000  # Arbitrary penalty weight

    return is_feasible, penalty

def initialize_particles():
    """
    Initialize particle positions and velocities randomly while ensuring feasibility.
    """
    particles = []
    velocities = []
    for _ in range(NUM_PARTICLES):
        particle = []
        for year in range(NUM_YEARS):
            yearly_decisions = [
                {
                    'Operating Year': 2023 + year,
                    'ID': np.random.choice(vehicles['ID']),
                    'Num_Vehicles': np.random.randint(1, 10),
                    'Type': np.random.choice(['Buy', 'Use', 'Sell']),
                    'Fuel': np.random.choice(fuels['Fuel']),
                    'Distance_bucket': np.random.choice(['D1', 'D2', 'D3', 'D4']),
                    'Distance_per_vehicle(km)': np.random.uniform(100, 500),
                }
                for _ in range(len(vehicles))
            ]
            particle.append(yearly_decisions)
        velocity = np.random.rand(NUM_YEARS, len(vehicles))
        particles.append(particle)
        velocities.append(velocity)
    return particles, velocities

def update_velocity(velocity, position, best_position, global_best, w, c1, c2):
    """
    Update the velocity of a particle.
    """
    r1, r2 = np.random.rand(), np.random.rand()
    cognitive = c1 * r1 * (best_position - position)
    social = c2 * r2 * (global_best - position)
    return w * velocity + cognitive + social

def update_position(position, velocity):
    """
    Update the position of a particle.
    """
    new_position = position + velocity
    # Ensure the new position respects the constraints
    new_position = np.clip(new_position, 0, 1)
    return new_position

# PSO Implementation
# PSO Implementation
cost_calculator = Costs()  # Create an instance of the Costs class

particles, velocities = initialize_particles()
local_best_positions = particles.copy()
local_best_costs = [float('inf')] * NUM_PARTICLES
global_best_position = None
global_best_cost = float('inf')

for iteration in range(MAX_ITERATIONS):
    for i in range(NUM_PARTICLES):
        # Convert the particle to a DataFrame
        # fleet_details = pd.DataFrame(particles[i])
        fleet_details = pd.DataFrame(
        [decision for year_decisions in particles[i] for decision in year_decisions]
)  # Flatten particle data into a DataFrame

        op_year = 2023 + (iteration % NUM_YEARS)  # Example dynamic year assignment

        # Evaluate the particle
        total_cost = cost_calculator.total_fleet_cost(fleet_details, op_year)
        is_feasible, penalty = evaluate_constraints(particles[i])
        if not is_feasible:
            total_cost += penalty
        
        # Update local best
        if total_cost < local_best_costs[i]:
            local_best_costs[i] = total_cost
            local_best_positions[i] = particles[i].copy()

        # Update global best
        if total_cost < global_best_cost:
            global_best_cost = total_cost
            global_best_position = particles[i].copy()

    # Update velocities and positions
    for i in range(NUM_PARTICLES):
        velocities[i] = update_velocity(velocities[i], particles[i], local_best_positions[i], global_best_position, INERTIA_WEIGHT, COGNITIVE_CONSTANT, SOCIAL_CONSTANT)
        particles[i] = update_position(particles[i], velocities[i])

    print(f"Iteration {iteration + 1}/{MAX_ITERATIONS}, Global Best Cost: {global_best_cost}")

# Output the best solution
solution = global_best_position
# Convert the solution to a DataFrame and save to CSV
solution_df = pd.DataFrame(solution)
solution_df.to_csv('solution.csv', index=False)
