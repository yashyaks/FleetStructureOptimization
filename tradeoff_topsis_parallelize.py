import pandas as pd
import numpy as np
import math
import random 
from typing import List, Dict, Tuple
import multiprocessing as mp
from pprint import pprint

class MultiObjectiveFleetOptimizer:
    def __init__(self, data: pd.DataFrame, emission_weight: float = 0.5, cost_weight: float = 0.5):
        self.data = data
        self.emission_weight = emission_weight
        self.cost_weight = cost_weight
        self.vehicles_by_size_distance = self._group_vehicles()
        self.max_vehicles_by_group = self._calculate_max_vehicles()
        
        total_weight = emission_weight + cost_weight
        self.emission_weight = emission_weight / total_weight
        self.cost_weight = cost_weight / total_weight
    
    def _group_vehicles(self) -> Dict:
        groups = {}
        for _, row in self.data.iterrows():
            key = (row['size'], row['Distance_demand'])
            if key not in groups:
                groups[key] = []
            groups[key].append({
                'Allocation' : row['Allocation'],
                'Operating Year': row['Operating Year'],
                'Size': row['size'],
                'Distance_demand': row['Distance_demand'],
                'demand': row['demand'],
                'ID': row['id'],
                'vehicle_type': row['vehicle'],
                'Available Year': row ['Available Year'],
                'Cost ($)': row['cost'],
                'Yearly range (km)': row['yearly_range'],
                'Distance_vehicle': row['Distance_vehicle'],
                'Fuel': row['fuel'],
                'Consumption (unit_fuel/km)': row['consumption_unitfuel_per_km'],
                'carbon_emissions_per_km': row['carbon_emissions_per_km'],
                'insurance_cost': row['insurance_cost'],
                'maintenance_cost': row['maintenance_cost'],
                'fuel_costs_per_km': row['fuel_costs_per_km'],
                'Operating_Cost': row['Operating_Cost'],
                'Topsis_Score': row['Topsis_Score'],
                'Rank': row['Rank']
            })
        return groups
    
    def _calculate_max_vehicles(self) -> Dict:
        max_vehicles = {}
        for key, vehicles in self.vehicles_by_size_distance.items():

            demand = vehicles[0]['demand']
            
            max_yearly_range = max(v['Yearly range (km)'] for v in vehicles)
            
            max_vehicles[key] = math.ceil(demand / max_yearly_range)
        
        return max_vehicles

    def is_valid_solution(self, solution: Dict, size_distance: Tuple) -> bool:
        if sum(solution.values()) == 0:
            return False
        return sum(solution.values()) <= self.max_vehicles_by_group[size_distance]

    def calculate_total_cost(self, num_vehicles: int, vehicle: Dict) -> float:
        if num_vehicles == 0:
            return 0
        return num_vehicles * (
            vehicle['insurance_cost'] + 
            vehicle['maintenance_cost'] + 
            vehicle['Cost ($)']
        ) + vehicle['fuel_costs_per_km'] * (vehicle['demand'] / num_vehicles)

    def calculate_total_emissions(self, num_vehicles: int, vehicle: Dict) -> float:
        if num_vehicles == 0:
            return 0
        
        distance_per_vehicle = vehicle['demand'] / num_vehicles
        
        return vehicle['carbon_emissions_per_km'] * distance_per_vehicle * num_vehicles

    def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:

        population = []
        vehicles = self.vehicles_by_size_distance[size_distance]
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        topsis_scores = [v['Rank'] for v in vehicles]
        total_topsis = sum(topsis_scores)
        normalized_topsis = [score/total_topsis for score in topsis_scores] if total_topsis > 0 else [1/len(topsis_scores)] * len(topsis_scores)
        # prob = [(1 - x)/10 for x in normalized_topsis]
        vehicle_types = [v['ID'] for v in vehicles]
        # pprint(normalized_topsis)
        while len(population) < population_size:

            solution = {v_type: 0 for v_type in vehicle_types}
            remaining_vehicles = max_vehicles
            
            while remaining_vehicles > 0:
                selected_idx = np.random.choice(range(len(vehicle_types)), p=normalized_topsis)
                selected_type = vehicle_types[selected_idx]
                
                if solution[selected_type] < remaining_vehicles and random.random() < 0.7:
                    solution[selected_type] += 1
                    remaining_vehicles -= 1
                elif random.random() < 0.2:
                    break
            
            if self.is_valid_solution(solution, size_distance):
                population.append(solution)
        
        return population

    def crossover(self, parent1: Dict, parent2: Dict, size_distance: Tuple) -> Tuple[Dict, Dict]:
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
        attempts = 0
        max_attempts = 10
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        while attempts < max_attempts:
            mutated_solution = solution.copy()
            total_vehicles = sum(mutated_solution.values())
            
            for vehicle_type in mutated_solution.keys():
                if random.random() < mutation_rate:
                    change = random.choice([-1, 1, -mutated_solution[vehicle_type]])
                    
                    if ((change == 1 and total_vehicles < max_vehicles) or 
                        (change < 0 and mutated_solution[vehicle_type] + change >= 0)):
                        mutated_solution[vehicle_type] += change
                        total_vehicles += change
            
            if self.is_valid_solution(mutated_solution, size_distance):
                return mutated_solution
            
            attempts += 1
        
        return solution

    def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
        if not self.is_valid_solution(solution, size_distance):
            return float('-inf')
            
        vehicles = self.vehicles_by_size_distance[size_distance]
        vehicle_dict = {v['ID']: v for v in vehicles}
        demand = vehicles[0]['demand']

        total_cost = 0
        total_emissions = 0
        total_capacity = 0
        weighted_topsis = 0
        
        for vehicle_type, num_vehicles in solution.items():
            if num_vehicles > 0:
                vehicle = vehicle_dict[vehicle_type]
                total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
                total_capacity += num_vehicles * vehicle['Yearly range (km)']
                weighted_topsis += num_vehicles * vehicle['Rank']
        
        demand_penalty = max(0, demand - total_capacity) * 1000
        if demand_penalty > 0:  # Solution doesn't meet demand
            return float('-inf')
        
        max_possible_cost = max(self.calculate_total_cost(self.max_vehicles_by_group[size_distance], v) 
                                    for v in vehicles)
        max_possible_emissions = max(self.calculate_total_emissions(self.max_vehicles_by_group[size_distance], v) 
                                   for v in vehicles)
        
        normalized_cost = 1 - (total_cost / max_possible_cost if max_possible_cost > 0 else 0)
        normalized_emissions = 1 - (total_emissions / max_possible_emissions if max_possible_emissions > 0 else 0)
        
        multi_objective_score = (
            self.cost_weight * normalized_cost + 
            self.emission_weight * normalized_emissions +
            1 * (weighted_topsis / sum(solution.values()) if sum(solution.values()) > 0 else 0)
        )
        
        return multi_objective_score

    def pareto_rank(self, population: List[Dict], size_distance: Tuple) -> List[Tuple[Dict, int]]:

        solution_metrics = []
        
        # Calculate metrics for each solution
        for solution in population:
            if not self.is_valid_solution(solution, size_distance):
                solution_metrics.append((solution, float('inf'), float('inf')))
                continue
                
            vehicles = self.vehicles_by_size_distance[size_distance]
            vehicle_dict = {v['ID']: v for v in vehicles}
            
            total_cost = 0
            total_emissions = 0
            total_capacity = 0
            
            for vehicle_type, num_vehicles in solution.items():
                if num_vehicles > 0:
                    vehicle = vehicle_dict[vehicle_type]
                    total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                    total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
                    total_capacity += num_vehicles * vehicle['Yearly range (km)']
            
            demand = vehicles[0]['demand']
            if total_capacity < demand:
                solution_metrics.append((solution, float('inf'), float('inf')))
            else:
                solution_metrics.append((solution, total_cost, total_emissions))
        
        ranks = []
        remaining = solution_metrics.copy()
        rank = 0
        
        while remaining:
            pareto_front = []
            for i, (sol, cost, emissions) in enumerate(remaining):
                is_dominated = False
                
                for _, other_cost, other_emissions in remaining:

                    if (other_cost < cost and other_emissions <= emissions) or \
                       (other_cost <= cost and other_emissions < emissions):
                        is_dominated = True
                        break
                
                if not is_dominated:
                    pareto_front.append((sol, rank))
                    
            remaining = [(sol, cost, emissions) for (sol, cost, emissions) in remaining 
                         if not any(sol is p_sol for p_sol, _ in pareto_front)]
            
            ranks.extend(pareto_front)
            rank += 1
        return ranks

    def non_dominated_sorting(self, population: List[Dict], size_distance: Tuple):
        ranks = self.pareto_rank(population, size_distance)
        ranks.sort(key=lambda x: x[1], reverse=True)  # Sort by rank (lower is better)
        return ranks

    def optimize(self, size_distance: Tuple, generations: int = 100, population_size: int = 50) -> Dict:
        population = self.generate_initial_population(size_distance, population_size)
        best_solution = None
        best_fitness = float('-inf')
        
        for gen in range(generations):
            offspring = []
            while len(offspring) < population_size:
                parent1 = self.tournament_selection(population, size_distance)
                parent2 = self.tournament_selection(population, size_distance)
                
                child1, child2 = self.crossover(parent1, parent2, size_distance)
                
                child1 = self.mutate(child1, size_distance)
                child2 = self.mutate(child2, size_distance)
                
                offspring.extend([child1, child2])
            
            combined = population + offspring[:population_size]
            
            ranked_solutions = self.non_dominated_sorting(combined, size_distance)
            
            new_population = []
            current_rank = 0
            
            while len(new_population) < population_size and current_rank <= max(r for _, r in ranked_solutions):
                current_front = [sol for sol, rank in ranked_solutions if rank == current_rank]
                
                if len(new_population) + len(current_front) <= population_size:
                    new_population.extend(current_front)
                else:
                    sorted_front = self.crowding_distance_sort(current_front, size_distance)
                    remaining_slots = population_size - len(new_population)
                    new_population.extend(sorted_front[:remaining_slots])
                
                current_rank += 1
            
            population = new_population
            
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
        if len(solutions) <= 2:
            return solutions

        metrics = []
        for i, solution in enumerate(solutions):
            vehicles = self.vehicles_by_size_distance[size_distance]
            vehicle_dict = {v['ID']: v for v in vehicles}
            
            total_cost = 0
            total_emissions = 0
            
            for vehicle_type, num_vehicles in solution.items():
                if num_vehicles > 0:
                    vehicle = vehicle_dict[vehicle_type]
                    total_cost += self.calculate_total_cost(num_vehicles, vehicle)
                    total_emissions += self.calculate_total_emissions(num_vehicles, vehicle)
            
            metrics.append((i, solution, total_cost, total_emissions))
        
        distances = [0.0] * len(solutions)
        
        cost_sorted = sorted(metrics, key=lambda x: x[2])
        
        distances[cost_sorted[0][0]] = float('inf')
        distances[cost_sorted[-1][0]] = float('inf')
        
        cost_range = cost_sorted[-1][2] - cost_sorted[0][2]
        if cost_range > 0:
            for i in range(1, len(cost_sorted) - 1):
                idx = cost_sorted[i][0]
                distances[idx] += (cost_sorted[i+1][2] - cost_sorted[i-1][2]) / cost_range
        
        emissions_sorted = sorted(metrics, key=lambda x: x[3])
        
        if distances[emissions_sorted[0][0]] != float('inf'):
            distances[emissions_sorted[0][0]] = float('inf')
        if distances[emissions_sorted[-1][0]] != float('inf'):
            distances[emissions_sorted[-1][0]] = float('inf')
        
        emissions_range = emissions_sorted[-1][3] - emissions_sorted[0][3]
        if emissions_range > 0:
            for i in range(1, len(emissions_sorted) - 1):
                idx = emissions_sorted[i][0]
                distances[idx] += (emissions_sorted[i+1][3] - emissions_sorted[i-1][3]) / emissions_range
        
        solution_distances = [(solutions[i], distances[i]) for i in range(len(solutions))]
        
        sorted_pairs = sorted(solution_distances, key=lambda x: x[1], reverse=True)
        
        return [pair[0] for pair in sorted_pairs]
    
        # New method: Process a single size_distance group
    def _process_size_distance(self, size_distance: Tuple, generations, population_size) -> List[Dict]:
        results = []
        best_solution = self.optimize(size_distance, generations, population_size)
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        if best_solution is None:
            return results
            
        print(f"Processed {size_distance}: {best_solution}")
        
        for vehicle_type, num_vehicles in best_solution.items():
            if num_vehicles > 0:
                vehicle_data = next(v for v in self.vehicles_by_size_distance[size_distance] if v['ID'] == vehicle_type)
                total_cost = self.calculate_total_cost(num_vehicles, vehicle_data)
                total_emissions = self.calculate_total_emissions(num_vehicles, vehicle_data)
                Allocation = vehicle_data.get('Allocation')
                Size = vehicle_data.get('Size')
                Distance_demand = vehicle_data.get('Distance_demand')
                results.append({
                    "Allocation": Allocation,
                    "Operating Year": vehicle_data["Operating Year"],
                    "size": Size,
                    "Distance_demand": Distance_demand,
                    "demand": vehicle_data['demand'],
                    "id": vehicle_type,
                    "vehicle": vehicle_data['vehicle_type'],
                    "Available Year": vehicle_data['Available Year'],
                    "cost": vehicle_data['Cost ($)'],
                    "yearly_range": vehicle_data['Yearly range (km)'],
                    "Distance_vehicle": vehicle_data['Distance_vehicle'],
                    "fuel": vehicle_data['Fuel'],
                    "consumption_unitfuel_per_km": vehicle_data['Consumption (unit_fuel/km)'],
                    "carbon_emissions_per_km": vehicle_data['carbon_emissions_per_km'],
                    "insurance_cost": vehicle_data['insurance_cost'],
                    "maintenance_cost": vehicle_data['maintenance_cost'],
                    "fuel_costs_per_km": vehicle_data['fuel_costs_per_km'],
                    "Operating_Cost": vehicle_data['Operating_Cost'],
                    'Topsis_Score': vehicle_data['Topsis_Score'],
                    'Rank': vehicle_data['Rank'],
                    "No_of_vehicles": num_vehicles,
                    "Max Vehicles": max_vehicles,               
                })
        
        return results

    def get_optimized_results(self, year, generations: int = 100, population_size: int = 50) -> pd.DataFrame:
        all_results = []
        
        # Prepare input as tuples (size_distance, generations, population_size)
        input_args = [(size_distance, generations, population_size) for size_distance in self.vehicles_by_size_distance.keys()]
        
        with mp.Pool(processes=mp.cpu_count()) as pool:
            all_results = pool.starmap(self._process_size_distance, input_args)

        # Flatten the list of lists
        flattened_results = [item for sublist in all_results for item in sublist]

        df = pd.DataFrame(flattened_results)
        return df
