import pandas as pd
import random
from typing import List, Dict, Tuple
import numpy as np
import math
import os


def load_and_preprocess_data(csv_path: str) -> pd.DataFrame:
    """Load and preprocess the fleet data from CSV file."""
    df = pd.read_csv(csv_path)
    
    # Rename columns properly
    column_mapping = {
        'Unnamed: 0': 'Index',
        'Distance_demand': 'Distance_demand',
        'Demand (km)': 'Demand',
        'Cost ($)': 'Cost',
        'Yearly range (km)': 'Yearly_Range',
        'insurance_cost': 'Insurance_Cost',
        'maintenance_cost': 'Maintenance_Cost',
        'fuel_costs_per_km': 'Fuel_Costs',
        'Fuel': 'Fuel',
        'Total_Cost': 'Total_Cost',
        'Topsis_Score': 'Topsis_Score',
        # 'num_vehicles': 0
    }
    
    df.rename(columns=column_mapping, inplace=True, errors='ignore')
    # print("Columns after renaming:", df.columns)


    # Calculate Total Cost if missing
    # if 'Total_Cost' not in df.columns:
    #     df['Total_Cost'] = df['Insurance_Cost'] + df['Maintenance_Cost'] + df['Fuel_Costs']

    return df

class FleetOptimizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.vehicles_by_size_distance = self._group_vehicles()
        self.max_vehicles_by_group = self._calculate_max_vehicles()
    
    def _group_vehicles(self) -> Dict:
        """Group vehicles by (Size, Distance_demand) combination"""
        groups = {}
        for _, row in self.data.iterrows():
            key = (row['Size'], row['Distance_demand'])
            if key not in groups:
                groups[key] = []
            groups[key].append({
                'Allocation' : row['Allocation'],
                'Size': row['Size'],
                'Distance_demand': row['Distance_demand'],
                'vehicle_type': row['Vehicle'],
                'yearly_range': row['Yearly_Range'],
                'topsis_score': row['Topsis_Score'],
                'insurance_cost': row['Insurance_Cost'],
                'maintenance_cost': row['Maintenance_Cost'],
                'Cost ($)':row['Cost'],
                'fuel_costs_per_km': row['Fuel_Costs'],
                'fuel': row['Fuel'],
                'demand': row['Demand']
            })
        return groups
    
    def _calculate_max_vehicles(self) -> Dict:
        """Calculate maximum vehicles for each size-distance combination"""
        max_vehicles = {}
        for key, vehicles in self.vehicles_by_size_distance.items():
            # Get demand for this combination
            demand = vehicles[0]['demand']  # All vehicles in the same group have the same demand
            
            # Calculate max vehicles based on the vehicle with highest yearly range
            max_yearly_range = max(v['yearly_range'] for v in vehicles)
            
            # Calculate max vehicles needed and round up to ensure demand is met
            max_vehicles[key] = math.ceil(demand / max_yearly_range)
        
        return max_vehicles

    def get_total_vehicles_for_size_distance(self, size_distance: Tuple) -> int:
        """Get the total number of vehicles for a specific size-distance group"""

        combinations = df.groupby(['Size', 'Distance'])
        scores = []

        for (size, distance), group in combinations:
            total_vehicles = num_vehicles.sum()

        return total_vehicles

    # def calculate_utilization(self, demand: float, vehicle_type: str, vehicles_in_group: List[Dict]) -> float:
    #     """Calculate utilization metric for a vehicle type in a specific demand group"""
    #     total_vehicles_in_group = sum(v['num_vehicles'] for v in vehicles_in_group)
    #     if total_vehicles_in_group == 0:
    #         return 0
    #     vehicle = next(v for v in vehicles_in_group if v['vehicle_type'] == vehicle_type)
    #     return (demand / total_vehicles_in_group) / vehicle['yearly_range'] * 100


    # def calculate_utilization(self, demand: float, num_vehicles: int, yearly_range: float) -> float:
    #     """Calculate utilization metric for a vehicle type"""
    #     if num_vehicles == 0 or yearly_range == 0:
    #         return 0
            
    #     # Use total vehicles across the group rather than individual vehicle count
    #     # This matches the logic in the DataFrame version that uses total_vehicles = group['No_of_vehicles'].sum()
    #     total_vehicles_in_group = self.get_total_vehicles_for_size_distance(size_distance)
        
    #     # Calculate utilization percentage using total vehicles in the group
    #     return (demand / total_vehicles_in_group) / yearly_range * 100

        # vehicles = self.vehicles_by_size_distance[size_distance]
        # solution = self.current_solution[size_distance] if size_distance in self.current_solution else {}
        
        # # Sum all vehicles of all types in this group
        # return sum(solution.values())

    def calculate_utilization(self, demand: float, num_vehicles: int, yearly_range: float) -> float:
        """Calculate utilization metric for a vehicle type"""
        if num_vehicles == 0 or yearly_range == 0:
            return 0
        return (demand / num_vehicles) / yearly_range * 100

    def calculate_demand_fulfillment(self, num_vehicles: int, max_vehicles: int) -> float:
        """Calculate demand fulfillment by fuel type"""
        if max_vehicles == 0:
            return 0
        return num_vehicles / max_vehicles

    def is_valid_solution(self, solution: Dict, size_distance: Tuple) -> bool:
        """Check if the total number of vehicles in the solution is within the dynamic maximum limit"""
        return sum(solution.values()) <= self.max_vehicles_by_group[size_distance]

    # def calculate_total_cost(self, num_vehicles: int, vehicle: Dict) -> float:
    #     """Calculate total cost including insurance, maintenance, and fuel costs"""
    #     return num_vehicles * (
    #         vehicle['insurance_cost'] + 
    #         vehicle['maintenance_cost'] + 
    #         vehicle['fuel_costs_per_km']+
    #         vehicle['Cost ($)']
    #     )

    def calculate_total_cost(self, num_vehicles: int, vehicle: Dict) -> float:
        """Calculate total cost including insurance, maintenance, and fuel costs"""
        if num_vehicles == 0:
            return 0
        return num_vehicles * (
            vehicle['insurance_cost'] + 
            vehicle['maintenance_cost'] + 
            vehicle['Cost ($)']
        ) + vehicle['fuel_costs_per_km'] * (vehicle['demand'] / num_vehicles)


    # def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:
    #     """Generate initial population of fleet combinations"""
    #     population = []
    #     vehicles = self.vehicles_by_size_distance[size_distance]
    #     max_vehicles = self.max_vehicles_by_group[size_distance]
        
    #     while len(population) < population_size:
    #         # Generate a solution
    #         solution = {v['vehicle_type']: 0 for v in vehicles}
    #         remaining_vehicles = max_vehicles
            
    #         # Randomly distribute vehicles while respecting the total maximum
    #         vehicle_types = list(solution.keys())
    #         while remaining_vehicles > 0 and vehicle_types:
    #             vehicle_type = random.choice(vehicle_types)
    #             if random.random() < 0.5:  # 50% chance to add a vehicle
    #                 solution[vehicle_type] += 1
    #                 remaining_vehicles -= 1
    #             else:
    #                 vehicle_types.remove(vehicle_type)
            
    #         if self.is_valid_solution(solution, size_distance):
    #             population.append(solution)
        
    #     return population

    def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:
        """Generate diverse initial population with guaranteed demand fulfillment"""
        population = []
        vehicles = self.vehicles_by_size_distance[size_distance]
        max_vehicles = self.max_vehicles_by_group[size_distance]
        demand = vehicles[0]['demand']  # Assuming all vehicles in the group have the same demand value
        
        # Get all vehicle types and their properties
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        # vehicle_costs = {v['vehicle_type']: v['Total_Cost'] for v in vehicles}

        attempts = 0
        max_attempts = population_size * 10
        
        # --- Add greedy solutions by cost (low to high) ---
                # sorted_vehicles = sorted(vehicles, key=lambda v: v.get('Total_Cost', float('inf')))

        # sorted_by_cost = sorted(vehicles, key=lambda v: v['Total_Cost'])
        sorted_by_cost = sorted(vehicles, key=lambda v: v.get('Total_Cost', float('inf')))
        cost_solution = {v_type: 0 for v_type in vehicle_types}
        
        remaining_demand = demand
        for vehicle in sorted_by_cost:
            vehicle_type = vehicle['vehicle_type']
            while remaining_demand > 0 and sum(cost_solution.values()) < max_vehicles:
                cost_solution[vehicle_type] += 1
                remaining_demand -= vehicle['yearly_range']
        
        if self.is_valid_solution(cost_solution, size_distance):
            population.append(cost_solution)
        
        sorted_by_range = sorted(vehicles, key=lambda v: v['yearly_range'], reverse=True)
        range_solution = {v_type: 0 for v_type in vehicle_types}
        
        remaining_demand = demand
        for vehicle in sorted_by_range:
            vehicle_type = vehicle['vehicle_type']
            while remaining_demand > 0 and sum(range_solution.values()) < max_vehicles:
                range_solution[vehicle_type] += 1
                remaining_demand -= vehicle['yearly_range']
        
        if self.is_valid_solution(range_solution, size_distance):
            population.append(range_solution)
        
       # Generate more random solutions
        while len(population) < population_size and attempts < max_attempts:
            attempts += 1
            
            # Create a new random solution
            solution = {v_type: 0 for v_type in vehicle_types}
            
            # Randomly distribute vehicles to meet demand
            remaining_demand = demand
            while remaining_demand > 0 and sum(solution.values()) < max_vehicles:
                # Select a random vehicle type
                vehicle_type = random.choice(vehicle_types)
                
                # Add one of this type
                solution[vehicle_type] += 1
                remaining_demand -= vehicle_ranges[vehicle_type]
            
            # Check if valid and not duplicate
            if self.is_valid_solution(solution, size_distance) and solution not in population:
                population.append(solution)
        
        # If we couldn't generate enough solutions, make duplicates with small mutations
        while len(population) < population_size:
            if not population:  # Safety check
                base_solution = {v_type: 0 for v_type in vehicle_types}
                # Add vehicles until demand is met
                remaining_demand = demand
                for vt in vehicle_types:
                    while remaining_demand > 0:
                        base_solution[vt] += 1
                        remaining_demand -= vehicle_ranges[vt]
                    if remaining_demand <= 0:
                        break
                population.append(base_solution)
            
            # Take a random solution and mutate it
            base = random.choice(population)
            mutated = self.mutate(base, size_distance, 0.3)
            
            if self.is_valid_solution(mutated, size_distance):
                population.append(mutated)
        
        return population



    # def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:
    #     """Generate initial population of fleet combinations based on sorted vehicle costs"""
    #     population = []
    #     vehicles = self.vehicles_by_size_distance[size_distance]
    #     max_vehicles = self.max_vehicles_by_group[size_distance]
        
    #     # Sort vehicles by cost in ascending order (lower cost is better)
    #     sorted_vehicles = sorted(vehicles, key=lambda v: v.get('Total_Cost', float('inf')))
        
    #     while len(population) < population_size:
    #         # Generate a solution
    #         solution = {v['vehicle_type']: 0 for v in vehicles}
    #         remaining_vehicles = max_vehicles
            
    #         # Create different distributions for variety in the population
    #         if len(population) < population_size // 3:
    #             # First third: Greedy approach - prioritize lowest cost vehicles
    #             for vehicle in sorted_vehicles:
    #                 vehicle_type = vehicle['vehicle_type']
    #                 # Fill with lowest cost vehicles first
    #                 while remaining_vehicles > 0:
    #                     solution[vehicle_type] += 1
    #                     remaining_vehicles -= 1
                        
    #                     # Occasionally stop adding this type to ensure diversity
    #                     if random.random() < 0.3:
    #                         break
    #         elif len(population) < 2 * (population_size // 3):
    #             # Second third: Mixed approach with emphasis on lower cost
    #             for vehicle in sorted_vehicles:
    #                 vehicle_type = vehicle['vehicle_type']
    #                 # Add some of each type, with preference for cheaper ones
    #                 count = min(remaining_vehicles, random.randint(0, max(1, remaining_vehicles // 2)))
    #                 solution[vehicle_type] = count
    #                 remaining_vehicles -= count
    #         else:
    #             # Final third: More diverse combinations for exploration
    #             vehicle_types = [v['vehicle_type'] for v in sorted_vehicles]
    #             while remaining_vehicles > 0 and vehicle_types:
    #                 # Still slightly favor lower-cost vehicles by using the sorted order
    #                 for vehicle_type in vehicle_types[:]:
    #                     if remaining_vehicles <= 0:
    #                         break
    #                     if random.random() < 0.6:  # 60% chance to add
    #                         solution[vehicle_type] += 1
    #                         remaining_vehicles -= 1
    #                     else:
    #                         vehicle_types.remove(vehicle_type)
            
    #         if self.is_valid_solution(solution, size_distance):
    #             population.append(solution)
        
    #     return population
    

    def crossover(self, parent1: Dict, parent2: Dict, size_distance: Tuple) -> Tuple[Dict, Dict]:
        """Perform crossover between two parent solutions while respecting dynamic vehicle limit"""
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = {}
            child2 = {}
            
            for i, vehicle_type in enumerate(parent1.keys()):
                if i < crossover_point:
                    child1[vehicle_type] = parent1[vehicle_type]
                    child2[vehicle_type] = parent2[vehicle_type]
                else:
                    child1[vehicle_type] = parent2[vehicle_type]
                    child2[vehicle_type] = parent1[vehicle_type]
            
            if (self.is_valid_solution(child1, size_distance) and 
                self.is_valid_solution(child2, size_distance)):
                return child1, child2
            
            attempts += 1
        
        # If we can't create valid children, return copies of parents
        return parent1.copy(), parent2.copy()

    def mutate(self, solution: Dict, size_distance: Tuple, mutation_rate: float = 0.1) -> Dict:
        """Mutate a solution while respecting the dynamic vehicle limit"""
        attempts = 0
        max_attempts = 10
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        while attempts < max_attempts:
            mutated_solution = solution.copy()
            total_vehicles = sum(mutated_solution.values())
            
            for vehicle_type in mutated_solution.keys():
                if random.random() < mutation_rate:
                    change = random.choice([-1, 1])
                    if (change == 1 and total_vehicles < max_vehicles) or \
                       (change == -1 and mutated_solution[vehicle_type] > 0):
                        mutated_solution[vehicle_type] += change
                        total_vehicles += change
            
            if self.is_valid_solution(mutated_solution, size_distance):
                return mutated_solution
            
            attempts += 1
        
        return solution  # Return original if no valid mutation found

    def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
        """
        Calculate fitness of a solution based on:
        1. TOPSIS score
        2. Meeting demand requirements
        3. Total cost
        4. Penalty for exceeding maximum vehicles
        """
        if not self.is_valid_solution(solution, size_distance):
            return float('-inf')
            
        vehicles = self.vehicles_by_size_distance[size_distance]
        total_cost = 0
        total_capacity = 0
        weighted_topsis = 0
        
        for vehicle in vehicles:
            num_vehicles = solution[vehicle['vehicle_type']]
            total_cost += self.calculate_total_cost(num_vehicles, vehicle)
            total_capacity += num_vehicles * vehicle['yearly_range']
            weighted_topsis += num_vehicles * vehicle['topsis_score']
        
        # Penalize solutions that don't meet demand
        demand = vehicles[0]['demand']
        demand_penalty = max(0, demand - total_capacity) * 1000
        
        # Normalize costs (lower is better)
        cost_score = 1 / (total_cost + 1)
        
        return weighted_topsis + cost_score - demand_penalty

    def optimize(self, size_distance: Tuple, generations: int = 100) -> Dict:
        """Run genetic algorithm to find optimal fleet combination"""
        population = self.generate_initial_population(size_distance)
        best_solution = None
        best_fitness = float('-inf')
        
        for _ in range(generations):
            # Calculate fitness for all solutions
            fitness_scores = [(solution, self.fitness_function(solution, size_distance))
                            for solution in population]
            
            # Sort by fitness (descending)
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Update best solution if needed
            if fitness_scores[0][1] > best_fitness:
                best_solution = fitness_scores[0][0]
                best_fitness = fitness_scores[0][1]
            
            # Select parents for next generation
            parents = [score[0] for score in fitness_scores[:len(population)//2]]
            
            # Create next generation
            next_generation = parents.copy()
            while len(next_generation) < len(population):
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover(parent1, parent2, size_distance)
                child1 = self.mutate(child1, size_distance)
                child2 = self.mutate(child2, size_distance)
                next_generation.extend([child1, child2])
            
            population = next_generation[:len(population)]
        
        return best_solution

    def get_optimized_results(self) -> pd.DataFrame:
        """Run optimization and return results in the required format"""
        results = []
        
        for size_distance in self.vehicles_by_size_distance.keys():
            best_solution = self.optimize(size_distance)
            max_vehicles = self.max_vehicles_by_group[size_distance]
            
            for vehicle_type, num_vehicles in best_solution.items():
                if num_vehicles > 0:
                    vehicle_data = next(v for v in self.vehicles_by_size_distance[size_distance] 
                                     if v['vehicle_type'] == vehicle_type)
                    total_cost = self.calculate_total_cost(num_vehicles, vehicle_data)

                    # Calculate evaluation metrics
                    utilization = self.calculate_utilization(
                        vehicle_data['demand'],
                        num_vehicles,
                        vehicle_data['yearly_range']
                    )
                    
                    demand_fulfillment = self.calculate_demand_fulfillment(
                        num_vehicles,
                        max_vehicles
                    )

                    Allocation = vehicle_data.get('Allocation')
                    Size = vehicle_data.get('Size')
                    Distance_demand = vehicle_data.get('Distance_demand')

                    results.append({
                        # "Allocation": f"Size {size_distance[0]}, Distance {size_distance[1]}",
                        "Allocation": Allocation,
                        "Size":Size,
                        "Distance":Distance_demand,
                        "Vehicle": vehicle_type,
                        "Cost ($)": round(total_cost, 2),
                        "Fuel": vehicle_data['fuel'],
                        "no_of_vehicles": num_vehicles,
                        "Max Vehicles": max_vehicles,
                        "Demand": vehicle_data['demand'],
                        "Yearly Range": vehicle_data['yearly_range'],
                        "Utilization": round(utilization, 2),
                        "Demand_Fulfillment": round(demand_fulfillment, 2)
                    })

        return pd.DataFrame(results)


def main(csv_path: str):
    """Main function to run the optimization"""
    print("\nRunning optimization with dynamic maximum vehicles...")
    data_df = load_and_preprocess_data(csv_path)
    optimizer = FleetOptimizer(data_df)
    optimized_results = optimizer.get_optimized_results()
    
    # Calculate and print the total cost across all allocations
    total_cost = optimized_results["Cost ($)"].sum()
    print("\nOptimized Fleet Allocation:")
    print(optimized_results)
    print(f"\nTotal Fleet Cost: ${total_cost:,.2f}")
    
    return optimized_results

def process_all_years(input_folder: str, output_folder: str):
    """Process all CSV files in the input folder and save results in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output directory if it doesn't exist
    
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]  # List all CSV files
    yearly_costs = []  # Store total cost for each year
    
    for csv_file in csv_files:
        year = csv_file.split('_')[-1].replace('.csv', '')  # Extract year from filename
        csv_path = os.path.join(input_folder, csv_file)
        
        print(f"\nProcessing {csv_file}...")
        results_df = main(csv_path)  # Run optimization
        
        # Calculate total fleet cost
        total_cost = results_df["Cost ($)"].sum()
        yearly_costs.append({"Year": year, "Total Cost ($)": round(total_cost, 2)})
        
        # Save results
        output_file = os.path.join(output_folder, f"optimized_fleet_allocation_{year}.csv")
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    
    # Save yearly total cost summary
    summary_df = pd.DataFrame(yearly_costs)
    summary_file = os.path.join(output_folder, "yearly_total_cost_summary.csv")
    summary_df.to_csv(summary_file, index=False)
    print(f"\nYearly total cost summary saved to {summary_file}")


# def process_all_years(input_folder: str, output_folder: str):
#     """Process all CSV files in the input folder and save results in the output folder."""
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)  # Create output directory if it doesn't exist
    
#     csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]  # List all CSV files
    
#     for csv_file in csv_files:
#         year = csv_file.split('_')[-1].replace('.csv', '')  # Extract year from filename
#         csv_path = os.path.join(input_folder, csv_file)
        
#         print(f"\nProcessing {csv_file}...")
#         results_df = main(csv_path)  # Run optimization
        
#         # Save results
#         output_file = os.path.join(output_folder, f"optimized_fleet_allocation_{year}.csv")
#         results_df.to_csv(output_file, index=False)
#         print(f"Results saved to {output_file}")


if __name__ == "__main__":
    input_folder = "topsis_result"
    output_folder = "fleet_optimization_results_costmin"
    process_all_years(input_folder, output_folder)


# if __name__ == "__main__":
#     csv_path = "FINAL_CODES/topsis_result/topsis_results_2023.csv"  # Replace with your CSV file path
#     results_df = main(csv_path)
#     # results_df.to_csv("optimized_fleet_allocation_2023.csv", index=False)