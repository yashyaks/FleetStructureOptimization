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
        'Allocation' : 'Allocation',
        'Size': 'Size',
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
        'carbon_emission_per_km': 'carbon_emissions_per_km'  # Add carbon emission column
    }
    
    df.rename(columns=column_mapping, inplace=True, errors='ignore')

    return df

class MultiObjectiveFleetOptimizer:
    def __init__(self, data: pd.DataFrame, emission_weight: float = 0.5, cost_weight: float = 0.5):
        """
        Initialize the optimizer with weights for each objective
        
        Args:
            data: DataFrame with vehicle data
            emission_weight: Weight for carbon emission objective (0-1)
            cost_weight: Weight for cost objective (0-1)
        """
        self.data = data
        self.emission_weight = emission_weight
        self.cost_weight = cost_weight
        self.vehicles_by_size_distance = self._group_vehicles()
        self.max_vehicles_by_group = self._calculate_max_vehicles()
        
        # Normalize the weights to ensure they sum to 1
        total_weight = emission_weight + cost_weight
        self.emission_weight = emission_weight / total_weight
        self.cost_weight = cost_weight / total_weight
    
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
                'cost': row['Cost'],
                'fuel_costs_per_km': row['Fuel_Costs'],
                'fuel': row['Fuel'],
                'demand': row['Demand'],
                'carbon_emissions_per_km': row['carbon_emissions_per_km']  # Carbon emission per km
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

    # def calculate_utilization(self, demand: float, vehicle_data: pd.DataFrame, yearly_range: float) -> float:
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
        # Ensure solution has at least one vehicle
        if sum(solution.values()) == 0:
            return False
        return sum(solution.values()) <= self.max_vehicles_by_group[size_distance]

    def calculate_total_cost(self, num_vehicles: int, vehicle: Dict) -> float:
        """Calculate total cost including insurance, maintenance, and fuel costs"""
        if num_vehicles == 0:
            return 0
        return num_vehicles * (
            vehicle['insurance_cost'] + 
            vehicle['maintenance_cost'] + 
            vehicle['cost']
        ) + vehicle['fuel_costs_per_km'] * (vehicle['demand'] / num_vehicles)

    def calculate_total_emissions(self, num_vehicles: int, vehicle: Dict) -> float:
        """Calculate total carbon emissions for a vehicle type"""
        if num_vehicles == 0:
            return 0
        
        # Calculate distance per vehicle
        distance_per_vehicle = vehicle['demand'] / num_vehicles
        
        # Calculate total emissions
        return vehicle['carbon_emissions_per_km'] * distance_per_vehicle * num_vehicles

    def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:
        """Generate initial population of fleet combinations with TOPSIS score weighting"""
        population = []
        vehicles = self.vehicles_by_size_distance[size_distance]
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        # Calculate normalized TOPSIS scores for biasing initial population
        topsis_scores = [v['topsis_score'] for v in vehicles]
        total_topsis = sum(topsis_scores)
        normalized_topsis = [score/total_topsis for score in topsis_scores] if total_topsis > 0 else [1/len(topsis_scores)] * len(topsis_scores)
        
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        
        while len(population) < population_size:
            # Generate a solution
            solution = {v_type: 0 for v_type in vehicle_types}
            remaining_vehicles = max_vehicles
            
            # Weighted distribution based on TOPSIS scores
            while remaining_vehicles > 0:
                # Use TOPSIS scores to bias selection
                selected_idx = np.random.choice(range(len(vehicle_types)), p=normalized_topsis)
                selected_type = vehicle_types[selected_idx]
                
                if solution[selected_type] < remaining_vehicles and random.random() < 0.7:  # 70% chance to add
                    solution[selected_type] += 1
                    remaining_vehicles -= 1
                elif random.random() < 0.2:  # 20% chance to stop adding vehicles (for diversity)
                    break
            
            if self.is_valid_solution(solution, size_distance):
                population.append(solution)
        
        return population

    def crossover(self, parent1: Dict, parent2: Dict, size_distance: Tuple) -> Tuple[Dict, Dict]:
        """Perform crossover between two parent solutions while respecting constraints"""
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

    def mutate(self, solution: Dict, size_distance: Tuple, mutation_rate: float = 0.2) -> Dict:
        """Mutate a solution while respecting constraints"""
        attempts = 0
        max_attempts = 10
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        while attempts < max_attempts:
            mutated_solution = solution.copy()
            total_vehicles = sum(mutated_solution.values())
            
            for vehicle_type in mutated_solution.keys():
                if random.random() < mutation_rate:
                    # Either increase, decrease, or set to zero
                    change = random.choice([-1, 1, -mutated_solution[vehicle_type]])
                    
                    # Apply change if valid
                    if ((change == 1 and total_vehicles < max_vehicles) or 
                        (change < 0 and mutated_solution[vehicle_type] + change >= 0)):
                        mutated_solution[vehicle_type] += change
                        total_vehicles += change
            
            if self.is_valid_solution(mutated_solution, size_distance):
                return mutated_solution
            
            attempts += 1
        
        return solution  # Return original if no valid mutation found

    def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
        """
        Multi-objective fitness function that minimizes both carbon emissions and cost
        while also considering TOPSIS score and demand fulfillment
        """
        if not self.is_valid_solution(solution, size_distance):
            return float('-inf')
            
        vehicles = self.vehicles_by_size_distance[size_distance]
        vehicle_dict = {v['vehicle_type']: v for v in vehicles}
        demand = vehicles[0]['demand']
        
        # Initialize metrics
        total_cost = 0
        total_emissions = 0
        total_capacity = 0
        weighted_topsis = 0
        
        # Calculate metrics for each vehicle in the solution
        for vehicle_type, num_vehicles in solution.items():
            if num_vehicles > 0:
                vehicle = vehicle_dict[vehicle_type]
                total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
                total_capacity += num_vehicles * vehicle['yearly_range']
                weighted_topsis += num_vehicles * vehicle['topsis_score']
        
        # Demand fulfillment penalty
        demand_penalty = max(0, demand - total_capacity) * 1000
        if demand_penalty > 0:  # Solution doesn't meet demand
            return float('-inf')
        
        # Normalize cost and emissions between 0 and 1 using historical data or estimates
        # Here we use simple normalization for demonstration
        # In a real scenario, you'd normalize against known min/max values
        max_possible_cost = max(self.calculate_total_cost(self.max_vehicles_by_group[size_distance], v) 
                              for v in vehicles)
        max_possible_emissions = max(self.calculate_total_emissions(self.max_vehicles_by_group[size_distance], v) 
                                   for v in vehicles)
        
        # Normalize (lower values are better)
        normalized_cost = 1 - (total_cost / max_possible_cost if max_possible_cost > 0 else 0)
        normalized_emissions = 1 - (total_emissions / max_possible_emissions if max_possible_emissions > 0 else 0)
        
        # Combine objectives using weights
        multi_objective_score = (
            self.cost_weight * normalized_cost + 
            self.emission_weight * normalized_emissions +
            0.9 * (weighted_topsis / sum(solution.values()) if sum(solution.values()) > 0 else 0)  # Small TOPSIS bonus
        )
        
        return multi_objective_score


    # def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
    #     """
    #     Enhanced multi-objective fitness function that emphasizes cost, emissions,
    #     TOPSIS score, and strict demand fulfillment.
    #     """
    #     if not self.is_valid_solution(solution, size_distance):
    #         return float('-inf')

    #     vehicles = self.vehicles_by_size_distance[size_distance]
    #     vehicle_dict = {v['vehicle_type']: v for v in vehicles}
    #     demand = vehicles[0]['demand']

    #     # Initialize metrics
    #     total_cost = 0
    #     total_emissions = 0
    #     total_capacity = 0
    #     weighted_topsis = 0
    #     total_vehicles = sum(solution.values())

    #     # Compute the metrics
    #     for vehicle_type, num_vehicles in solution.items():
    #         if num_vehicles > 0:
    #             vehicle = vehicle_dict[vehicle_type]
    #             total_cost += self.calculate_total_cost(num_vehicles, vehicle)
    #             total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
    #             total_capacity += num_vehicles * vehicle['yearly_range']
    #             weighted_topsis += num_vehicles * vehicle['topsis_score']

    #     # Stronger penalty for demand fulfillment
    #     demand_penalty = max(0, demand - total_capacity) * 5000  # Increased penalty weight

    #     # Normalize cost and emissions
    #     max_possible_cost = max(self.calculate_total_cost(self.max_vehicles_by_group[size_distance], v) for v in vehicles)
    #     max_possible_emissions = max(self.calculate_total_emissions(self.max_vehicles_by_group[size_distance], v) for v in vehicles)

    #     normalized_cost = 1 - (total_cost / max_possible_cost if max_possible_cost > 0 else 0)
    #     normalized_emissions = 1 - (total_emissions / max_possible_emissions if max_possible_emissions > 0 else 0)

    #     # More emphasis on TOPSIS score
    #     normalized_topsis = (weighted_topsis / total_vehicles) if total_vehicles > 0 else 0

    #     # Apply non-linear transformation to emphasize cost & emission reduction
    #     normalized_cost = normalized_cost ** 2  # Quadratic scaling
    #     normalized_emissions = normalized_emissions ** 2  

    #     # Adjusted weights
    #     multi_objective_score = (
    #         self.cost_weight * normalized_cost + 
    #         self.emission_weight * normalized_emissions +
    #         1.2 * normalized_topsis  # Increased TOPSIS weight
    #     ) - demand_penalty  # Stronger penalty

    #     return multi_objective_score if total_capacity >= demand else float('-inf')  # Hard constraint


    def pareto_rank(self, population: List[Dict], size_distance: Tuple) -> List[Tuple[Dict, int]]:
        """
        Apply Pareto ranking to the population based on the two objectives:
        cost and emissions.
        
        Returns: List of (solution, rank) pairs where lower rank is better
        """
        solution_metrics = []
        
        # Calculate metrics for each solution
        for solution in population:
            if not self.is_valid_solution(solution, size_distance):
                solution_metrics.append((solution, float('inf'), float('inf')))
                continue
                
            vehicles = self.vehicles_by_size_distance[size_distance]
            vehicle_dict = {v['vehicle_type']: v for v in vehicles}
            
            total_cost = 0
            total_emissions = 0
            total_capacity = 0
            
            for vehicle_type, num_vehicles in solution.items():
                if num_vehicles > 0:
                    vehicle = vehicle_dict[vehicle_type]
                    total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                    total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
                    total_capacity += num_vehicles * vehicle['yearly_range']
            
            # Check if demand is met
            demand = vehicles[0]['demand']
            if total_capacity < demand:
                solution_metrics.append((solution, float('inf'), float('inf')))
            else:
                solution_metrics.append((solution, total_cost, total_emissions))
        
        # Pareto ranking
        ranks = []
        remaining = solution_metrics.copy()
        rank = 0
        
        while remaining:
            pareto_front = []
            for i, (sol, cost, emissions) in enumerate(remaining):
                is_dominated = False
                
                for _, other_cost, other_emissions in remaining:
                    # Check if solution is dominated (both objectives are worse)
                    if (other_cost < cost and other_emissions <= emissions) or \
                       (other_cost <= cost and other_emissions < emissions):
                        is_dominated = True
                        break
                
                if not is_dominated:
                    pareto_front.append((sol, rank))
                    
            # Remove pareto front from remaining solutions
            remaining = [(sol, cost, emissions) for (sol, cost, emissions) in remaining 
                         if not any(sol is p_sol for p_sol, _ in pareto_front)]
            
            ranks.extend(pareto_front)
            rank += 1
        
        return ranks

    def non_dominated_sorting(self, population: List[Dict], size_distance: Tuple):
        """
        Sort the population into non-dominated fronts based on cost and emissions.
        Returns sorted population with rank information
        """
        ranks = self.pareto_rank(population, size_distance)
        ranks.sort(key=lambda x: x[1])  # Sort by rank (lower is better)
        return ranks

    def optimize(self, size_distance: Tuple, generations: int = 100, population_size: int = 50) -> Dict:
        """Run NSGA-II style genetic algorithm to find optimal fleet combination"""
        # Initial population
        population = self.generate_initial_population(size_distance, population_size)
        best_solution = None
        best_fitness = float('-inf')
        
        for gen in range(generations):
            # Create offspring through crossover and mutation
            offspring = []
            while len(offspring) < population_size:
                # Tournament selection
                parent1 = self.tournament_selection(population, size_distance)
                parent2 = self.tournament_selection(population, size_distance)
                
                # Crossover
                child1, child2 = self.crossover(parent1, parent2, size_distance)
                
                # Mutation
                child1 = self.mutate(child1, size_distance)
                child2 = self.mutate(child2, size_distance)
                
                # Add to offspring
                offspring.extend([child1, child2])
            
            # Combine parent and offspring populations
            combined = population + offspring[:population_size]
            
            # Non-dominated sorting
            ranked_solutions = self.non_dominated_sorting(combined, size_distance)
            
            # Create new population
            new_population = []
            current_rank = 0
            
            while len(new_population) < population_size and current_rank <= max(r for _, r in ranked_solutions):
                # Get solutions of current rank
                current_front = [sol for sol, rank in ranked_solutions if rank == current_rank]
                
                if len(new_population) + len(current_front) <= population_size:
                    # Add all solutions in current front
                    new_population.extend(current_front)
                else:
                    # Sort current front by diversity (crowding distance)
                    sorted_front = self.crowding_distance_sort(current_front, size_distance)
                    remaining_slots = population_size - len(new_population)
                    new_population.extend(sorted_front[:remaining_slots])
                
                current_rank += 1
            
            # Update population
            population = new_population
            
            # Update best solution if needed
            for solution in population:
                fitness = self.fitness_function(solution, size_distance)
                if fitness > best_fitness:
                    best_solution = solution
                    best_fitness = fitness
        
        return best_solution

    def tournament_selection(self, population: List[Dict], size_distance: Tuple, tournament_size: int = 3) -> Dict:
        """Tournament selection based on fitness"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: self.fitness_function(x, size_distance))

    def crowding_distance_sort(self, solutions: List[Dict], size_distance: Tuple) -> List[Dict]:
        """Sort solutions by crowding distance for diversity preservation"""
        if len(solutions) <= 2:
            return solutions
            
        # Calculate metrics for each solution
        metrics = []
        for i, solution in enumerate(solutions):
            vehicles = self.vehicles_by_size_distance[size_distance]
            vehicle_dict = {v['vehicle_type']: v for v in vehicles}
            
            total_cost = 0
            total_emissions = 0
            
            for vehicle_type, num_vehicles in solution.items():
                if num_vehicles > 0:
                    vehicle = vehicle_dict[vehicle_type]
                    total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                    total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
            
            # Store the index along with the solution and metrics
            metrics.append((i, solution, total_cost, total_emissions))
        
        # Use a list to store distances, indexed by the original solution indices
        distances = [0.0] * len(solutions)
        
        # Sort by cost
        cost_sorted = sorted(metrics, key=lambda x: x[2])
        
        # Boundary solutions get infinite distance
        distances[cost_sorted[0][0]] = float('inf')
        distances[cost_sorted[-1][0]] = float('inf')
        
        # Calculate distances for cost objective
        cost_range = cost_sorted[-1][2] - cost_sorted[0][2]
        if cost_range > 0:
            for i in range(1, len(cost_sorted) - 1):
                idx = cost_sorted[i][0]
                distances[idx] += (cost_sorted[i+1][2] - cost_sorted[i-1][2]) / cost_range
        
        # Sort by emissions
        emissions_sorted = sorted(metrics, key=lambda x: x[3])
        
        # Boundary solutions get infinite distance (but don't overwrite existing infinite values)
        if distances[emissions_sorted[0][0]] != float('inf'):
            distances[emissions_sorted[0][0]] = float('inf')
        if distances[emissions_sorted[-1][0]] != float('inf'):
            distances[emissions_sorted[-1][0]] = float('inf')
        
        # Calculate distances for emissions objective
        emissions_range = emissions_sorted[-1][3] - emissions_sorted[0][3]
        if emissions_range > 0:
            for i in range(1, len(emissions_sorted) - 1):
                idx = emissions_sorted[i][0]
                distances[idx] += (emissions_sorted[i+1][3] - emissions_sorted[i-1][3]) / emissions_range
        
        # Create pairs of (solution, distance) for sorting
        solution_distances = [(solutions[i], distances[i]) for i in range(len(solutions))]
        
        # Sort solutions by crowding distance (descending)
        sorted_pairs = sorted(solution_distances, key=lambda x: x[1], reverse=True)
        
        # Return just the sorted solutions
        return [pair[0] for pair in sorted_pairs]

    def get_optimized_results(self) -> pd.DataFrame:
        """Run optimization and return results in the required format"""
        results = []
        
        for size_distance in self.vehicles_by_size_distance.keys():
            best_solution = self.optimize(size_distance)
            max_vehicles = self.max_vehicles_by_group[size_distance]
            
            if best_solution is None:
                continue
                
            for vehicle_type, num_vehicles in best_solution.items():
                if num_vehicles > 0:
                    vehicle_data = next(v for v in self.vehicles_by_size_distance[size_distance] 
                                     if v['vehicle_type'] == vehicle_type)
                    total_cost = self.calculate_total_cost(num_vehicles, vehicle_data)
                    total_emissions = self.calculate_total_emissions(num_vehicles, vehicle_data)


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
                        "carbon_emissions_per_km": round(total_emissions, 2),
                        "Fuel": vehicle_data['fuel'],
                        "No_of_vehicles": num_vehicles,
                        "Max Vehicles": max_vehicles,
                        "Demand": vehicle_data['demand'],
                        "Yearly Range": vehicle_data['yearly_range'],
                        "Utilization (%)": round(utilization, 2),
                        "Demand_Fulfillment (%)": round(demand_fulfillment * 100, 2)
                    })

        return pd.DataFrame(results)


def process_all_years(input_folder: str, output_folder: str, emission_weight: float = 0.5, cost_weight: float = 0.5):
    """Process all CSV files in the input folder and save results in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output directory if it doesn't exist
    
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]  # List all CSV files
    yearly_results = []  # Store results for each year
    
    for csv_file in csv_files:
        year = csv_file.split('_')[-1].replace('.csv', '')  # Extract year from filename
        csv_path = os.path.join(input_folder, csv_file)
        
        print(f"\nProcessing {csv_file}...")
        results_df = main(csv_path, emission_weight, cost_weight)  # Run optimization
        
        # Calculate totals
        total_cost = results_df["Cost ($)"].sum()
        total_emissions = results_df["carbon_emissions_per_km"].sum()
        
        yearly_results.append({
            "Year": year, 
            "Total Cost ($)": round(total_cost, 2), 
            "Total carbon_emissions_per_km": round(total_emissions, 2)
        })
        
        # Save individual year results
        output_file = os.path.join(output_folder, f"multi_objective_fleet_allocation_{year}.csv")
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    
    # Save yearly summary
    summary_df = pd.DataFrame(yearly_results)
    summary_file = os.path.join(output_folder, "yearly_summary_multi_objective.csv")
    summary_df.to_csv(summary_file, index=False)
    print(f"\nYearly summary saved to {summary_file}")


def main(csv_path: str, emission_weight: float = 0.5, cost_weight: float = 0.5):
    """Main function to run the multi-objective optimization"""
    print(f"\nRunning multi-objective optimization (Cost Weight: {cost_weight}, Emission Weight: {emission_weight})...")
    data_df = load_and_preprocess_data(csv_path)
    
    optimizer = MultiObjectiveFleetOptimizer(data_df, emission_weight, cost_weight)
    optimized_results = optimizer.get_optimized_results()
    
    # Calculate and print the total cost and emissions across all allocations
    total_cost = optimized_results["Cost ($)"].sum()
    total_emissions = optimized_results["carbon_emissions_per_km"].sum()
    
    print("\nOptimized Fleet Allocation:")
    print(optimized_results)
    print(f"\nTotal Fleet Cost: ${total_cost:,.2f}")
    print(f"Total Carbon Emissions: {total_emissions:,.2f} kg CO2")
    
    return optimized_results


if __name__ == "__main__":
    # Define weights for the objectives (must sum to 1.0)
    emission_weight = 0.5
    cost_weight = 0.5  
    
    # Run for a single file
    # csv_path = "topsis_result/topsis_results_2023.csv"
    # results_df = main(csv_path, emission_weight, cost_weight)
    # results_df.to_csv("multi_objective_fleet_allocation_2023.csv", index=False)
    
    # Or process all files in a folder
    input_folder = "topsis_result"
    output_folder = "multi_objective_fleet_results"
    process_all_years(input_folder, output_folder, emission_weight, cost_weight)
    