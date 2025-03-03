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
        'Allocation': 'Allocation',
        'Size':'Size',
        'Distance_demand': 'Distance_demand',
        'Demand (km)': 'Demand',
        'Cost ($)': 'Cost',
        'Yearly range (km)': 'Yearly_Range',
        'insurance_cost': 'Insurance_Cost',
        'maintenance_cost': 'Maintenance_Cost',
        'fuel_costs_per_km': 'Fuel_Costs',
        'Fuel': 'Fuel',
        'carbon emissions per km': 'carbon_emissions_per_km',
        'Total_Cost': 'Total_Cost',
        'Topsis_Score': 'Topsis_Score',
    }
    
    df.rename(columns=column_mapping, inplace=True, errors='ignore')
    return df

class FleetOptimizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.vehicles_by_size_distance = self._group_vehicles()
        self.max_vehicles_by_group = self._calculate_max_vehicles()
        self.total_carbon_emissions = 0
    
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
                'carbon_emissions_per_km': row['carbon_emissions_per_km'],
                'demand': row['Demand'],
                'fuel': row['Fuel']
            })
        return groups
    
    def _calculate_max_vehicles(self) -> Dict:
        """Calculate maximum vehicles for each size-distance combination"""
        max_vehicles = {}
        for key, vehicles in self.vehicles_by_size_distance.items():
            demand = vehicles[0]['demand']
            max_yearly_range = max(v['yearly_range'] for v in vehicles)
            # Add a small buffer to ensure demand is met even with rounding issues
            max_vehicles[key] = math.ceil(demand / max_yearly_range)
        return max_vehicles

    def calculate_utilization(self, demand: float, num_vehicles: int, yearly_range: float) -> float:
        """Calculate utilization metric for a vehicle type"""
        if num_vehicles == 0 or yearly_range == 0:
            return 0
        return min(100, (demand / num_vehicles) / yearly_range * 100)  # Cap at 100%

    def calculate_demand_fulfillment(self, total_capacity: float, demand: float) -> float:
        """Calculate demand fulfillment percentage"""
        if demand == 0:
            return 100.0
        return min(100.0, (total_capacity / demand) * 100)

    def demand_deficit(self, solution: Dict, size_distance: Tuple) -> float:
        """Calculate how much demand is not met by the current solution"""
        vehicles = self.vehicles_by_size_distance[size_distance]
        demand = vehicles[0]['demand']
        total_capacity = sum(solution[v['vehicle_type']] * v['yearly_range'] for v in vehicles)
        
        return max(0, demand - total_capacity)

    def calculate_emissions(self, solution: Dict, size_distance: Tuple) -> float:
        """Calculate total carbon emissions for a solution"""
        vehicles = self.vehicles_by_size_distance[size_distance]
        total_emissions = 0
        
        # Calculate how much of the demand is satisfied by each vehicle type
        demand = vehicles[0]['demand']
        total_capacity = sum(solution[v['vehicle_type']] * v['yearly_range'] for v in vehicles)
        
        # If demand is not fully met, return infinity (extremely high penalty)
        if total_capacity < demand:
            return float('inf')
        
        # Calculate actual distance covered by each vehicle type
        remaining_demand = demand
        
        # Sort vehicles by emissions (lowest first) to prioritize cleaner vehicles when allocating demand
        sorted_vehicles = sorted(vehicles, key=lambda v: v['carbon_emissions_per_km'])
        
        for vehicle in sorted_vehicles:
            vehicle_type = vehicle['vehicle_type']
            num_vehicles = solution[vehicle_type]
            
            if num_vehicles > 0:
                # Calculate how much distance this vehicle type can cover
                vehicle_capacity = num_vehicles * vehicle['yearly_range']
                assigned_demand = min(vehicle_capacity, remaining_demand)
                remaining_demand -= assigned_demand
                
                # Calculate emissions for this portion of demand
                emissions = vehicle['carbon_emissions_per_km'] * assigned_demand
                total_emissions += emissions
                
                # If all demand is allocated, break
                if remaining_demand <= 0:
                    break
        
        return total_emissions

    def is_valid_solution(self, solution: Dict, size_distance: Tuple) -> bool:
        """Check if the solution is valid (meets vehicle limits and demand)"""
        # Check if we don't exceed max vehicles per group
        if sum(solution.values()) > self.max_vehicles_by_group[size_distance]:
            return False
            
        # Check if demand is fully met (strict requirement)
        vehicles = self.vehicles_by_size_distance[size_distance]
        total_capacity = sum(solution[v['vehicle_type']] * v['yearly_range'] for v in vehicles)
        demand = vehicles[0]['demand']
        
        # Must satisfy at least 99.9% of demand to handle floating point imprecision
        return total_capacity >= (0.999 * demand)

    # def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
    #     """
    #     Calculate fitness score with primary focus on demand fulfillment,
    #     then carbon emissions, then efficiency
    #     """
    #     # First check: is the solution valid?
    #     if not self.is_valid_solution(solution, size_distance):
    #         # Calculate deficit to guide evolution towards valid solutions
    #         deficit = self.demand_deficit(solution, size_distance)
    #         # Negative score proportional to deficit - helps genetic algorithm converge better
    #         return -1000000 * deficit
        
    #     # Solution is valid, so calculate emissions
    #     emissions = self.calculate_emissions(solution, size_distance)
        
    #     # If emissions are infinite (demand not met), this shouldn't happen but handle it
    #     if emissions == float('inf'):
    #         return float('-inf')
        
    #     # Inverse relationship: lower emissions = higher fitness
    #     emissions_score = 1000000 / (emissions + 1)
        
    #     # Add a small component for efficiency (fewer vehicles is better)
    #     vehicles_count = sum(solution.values())
    #     max_vehicles = self.max_vehicles_by_group[size_distance]
    #     if vehicles_count > 0:
    #         efficiency_score = max_vehicles / vehicles_count
    #     else:
    #         efficiency_score = 0
        
    #     # Calculate diversity score (mix of vehicle types is sometimes better for robustness)
    #     vehicle_types_used = sum(1 for v in solution.values() if v > 0)
    #     diversity_factor = vehicle_types_used / len(solution) if len(solution) > 0 else 0
            
    #     # Return combined score with emphasis on emissions
    #     return emissions_score * 0.9 + efficiency_score * 0.07 + diversity_factor * 0.03

    def fitness_function(self, solution: Dict, size_distance: Tuple) -> float:
        """
        Calculate fitness score with primary focus on demand fulfillment,
        then carbon emissions, then efficiency, incorporating TOPSIS score.
        """
        if not self.is_valid_solution(solution, size_distance):
            deficit = self.demand_deficit(solution, size_distance)
            return -1000000 * deficit
        
        emissions = self.calculate_emissions(solution, size_distance)
        if emissions == float('inf'):
            return float('-inf')
        
        emissions_score = 1000000 / (emissions + 1)
        
        vehicles = self.vehicles_by_size_distance[size_distance]
        weighted_topsis = 0
        for vehicle in vehicles:
            num_vehicles = solution[vehicle['vehicle_type']]
            weighted_topsis += num_vehicles * vehicle['topsis_score']
        
        vehicles_count = sum(solution.values())
        max_vehicles = self.max_vehicles_by_group[size_distance]
        efficiency_score = max_vehicles / vehicles_count if vehicles_count > 0 else 0
        
        # vehicle_types_used = sum(1 for v in solution.values() if v > 0)
        # diversity_factor = vehicle_types_used / len(solution) if len(solution) > 0 else 0
        
        return weighted_topsis+ emissions_score+ efficiency_score


    def generate_initial_population(self, size_distance: Tuple, population_size: int = 50) -> List[Dict]:
        """Generate diverse initial population with guaranteed demand fulfillment"""
        population = []
        vehicles = self.vehicles_by_size_distance[size_distance]
        max_vehicles = self.max_vehicles_by_group[size_distance]
        demand = vehicles[0]['demand']
        
        # Get all vehicle types
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        
        # Create solutions with diversity - but ensure all meet demand
        attempts = 0
        max_attempts = population_size * 10  # Limit attempts to avoid infinite loops
        
        # Include greedy solutions in the initial population for quick convergence
        # 1. Sort vehicles by emissions (low to high)
        sorted_vehicles = sorted(vehicles, key=lambda v: v['carbon_emissions_per_km'])
        greedy_solution = {v_type: 0 for v_type in vehicle_types}
        
        remaining_demand = demand
        for vehicle in sorted_vehicles:
            vehicle_type = vehicle['vehicle_type']
            while remaining_demand > 0 and sum(greedy_solution.values()) < max_vehicles:
                greedy_solution[vehicle_type] += 1
                remaining_demand -= vehicle['yearly_range']
        
        if self.is_valid_solution(greedy_solution, size_distance):
            population.append(greedy_solution)
        
        # 2. Sort by range (high to low) for efficiency
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

    def crossover(self, parent1: Dict, parent2: Dict, size_distance: Tuple) -> Tuple[Dict, Dict]:
        """Perform crossover between two parent solutions with guaranteed demand fulfillment"""
        attempts = 0
        max_attempts = 20
        vehicles = self.vehicles_by_size_distance[size_distance]
        demand = vehicles[0]['demand']
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        
        while attempts < max_attempts:
            # Use two-point crossover for better diversity
            vehicle_types = list(parent1.keys())
            
            if len(vehicle_types) < 3:
                # For small number of types, use single point crossover
                crossover_point = random.randint(1, len(vehicle_types) - 1)
                
                child1 = {}
                child2 = {}
                
                for i, vehicle_type in enumerate(vehicle_types):
                    if i < crossover_point:
                        child1[vehicle_type] = parent1[vehicle_type]
                        child2[vehicle_type] = parent2[vehicle_type]
                    else:
                        child1[vehicle_type] = parent2[vehicle_type]
                        child2[vehicle_type] = parent1[vehicle_type]
            else:
                # For more types, use two-point crossover
                points = sorted(random.sample(range(1, len(vehicle_types)), 2))
                
                child1 = {}
                child2 = {}
                
                for i, vehicle_type in enumerate(vehicle_types):
                    if i < points[0] or i >= points[1]:
                        child1[vehicle_type] = parent1[vehicle_type]
                        child2[vehicle_type] = parent2[vehicle_type]
                    else:
                        child1[vehicle_type] = parent2[vehicle_type]
                        child2[vehicle_type] = parent1[vehicle_type]
            
            # Ensure demand is met for both children
            child1_capacity = sum(child1[vt] * vehicle_ranges[vt] for vt in vehicle_types)
            child2_capacity = sum(child2[vt] * vehicle_ranges[vt] for vt in vehicle_types)
            
            # If both meet demand and are valid, return them
            valid1 = self.is_valid_solution(child1, size_distance)
            valid2 = self.is_valid_solution(child2, size_distance)
            
            if valid1 and valid2:
                return child1, child2
            
            # If only one is valid, repair the other
            if valid1 and not valid2:
                child2 = self._repair_solution(child2, size_distance)
                if self.is_valid_solution(child2, size_distance):
                    return child1, child2
            elif valid2 and not valid1:
                child1 = self._repair_solution(child1, size_distance)
                if self.is_valid_solution(child1, size_distance):
                    return child1, child2
            else:
                # Both invalid, repair both
                child1 = self._repair_solution(child1, size_distance)
                child2 = self._repair_solution(child2, size_distance)
                if self.is_valid_solution(child1, size_distance) and self.is_valid_solution(child2, size_distance):
                    return child1, child2
                    
            attempts += 1
        
        # If failed to create valid children, use the parents if they're valid
        if self.is_valid_solution(parent1, size_distance) and self.is_valid_solution(parent2, size_distance):
            return parent1.copy(), parent2.copy()
        
        # If one parent is invalid, return two copies of the valid one
        if self.is_valid_solution(parent1, size_distance):
            return parent1.copy(), parent1.copy()
        if self.is_valid_solution(parent2, size_distance):
            return parent2.copy(), parent2.copy()
        
        # If both parents are invalid (shouldn't happen), create a basic valid solution
        basic_solution = self._create_basic_valid_solution(size_distance)
        return basic_solution, basic_solution
    
    def _create_basic_valid_solution(self, size_distance: Tuple) -> Dict:
        """Create a simple valid solution that meets demand"""
        vehicles = self.vehicles_by_size_distance[size_distance]
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        demand = vehicles[0]['demand']
        
        # Sort vehicles by emissions (low to high)
        sorted_vehicles = sorted(vehicles, key=lambda v: v['carbon_emissions_per_km'])
        
        solution = {v_type: 0 for v_type in vehicle_types}
        remaining_demand = demand
        
        # Add vehicles until demand is met
        for vehicle in sorted_vehicles:
            vehicle_type = vehicle['vehicle_type']
            while remaining_demand > 0:
                solution[vehicle_type] += 1
                remaining_demand -= vehicle['yearly_range']
                if remaining_demand <= 0:
                    break
            if remaining_demand <= 0:
                break
        
        return solution
    
    def _repair_solution(self, solution: Dict, size_distance: Tuple) -> Dict:
        """Repair an invalid solution to ensure it meets demand requirements"""
        vehicles = self.vehicles_by_size_distance[size_distance]
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        demand = vehicles[0]['demand']
        max_vehicles = self.max_vehicles_by_group[size_distance]
        
        # Make a copy to avoid modifying the original
        repaired = solution.copy()
        
        # Calculate current capacity
        total_capacity = sum(repaired[vt] * vehicle_ranges[vt] for vt in vehicle_types)
        total_vehicles = sum(repaired.values())
        
        # If we exceed max vehicles, reduce until within limits
        if total_vehicles > max_vehicles:
            # Sort vehicle types by efficiency (range per vehicle)
            efficiency_ranking = sorted(vehicle_types, 
                                      key=lambda vt: vehicle_ranges[vt], 
                                      reverse=True)
            
            # Reduce vehicles starting with least efficient types
            for vt in reversed(efficiency_ranking):
                while total_vehicles > max_vehicles and repaired[vt] > 0:
                    repaired[vt] -= 1
                    total_vehicles -= 1
                    total_capacity -= vehicle_ranges[vt]
        
        # If demand is not met, add vehicles until it is
        if total_capacity < demand:
            # Sort by emissions efficiency (lower emissions first)
            emissions_ranking = sorted(vehicles, 
                                     key=lambda v: v['carbon_emissions_per_km'])
            
            # First try adding lowest emission vehicles
            for vehicle in emissions_ranking:
                vt = vehicle['vehicle_type']
                while total_capacity < demand and total_vehicles < max_vehicles:
                    repaired[vt] += 1
                    total_vehicles += 1
                    total_capacity += vehicle_ranges[vt]
                
                if total_capacity >= demand:
                    break
            
            # If still not meeting demand and at max vehicles, swap less efficient vehicles
            # for more efficient ones
            if total_capacity < demand and total_vehicles >= max_vehicles:
                # Sort by range (highest first)
                range_ranking = sorted(vehicle_types, 
                                     key=lambda vt: vehicle_ranges[vt], 
                                     reverse=True)
                
                # Try replacing less efficient vehicles with more efficient ones
                for high_range_vt in range_ranking:
                    for low_range_vt in reversed(range_ranking):
                        if high_range_vt == low_range_vt:
                            continue
                        
                        # Only swap if it would increase capacity
                        if vehicle_ranges[high_range_vt] > vehicle_ranges[low_range_vt] and repaired[low_range_vt] > 0:
                            repaired[low_range_vt] -= 1
                            repaired[high_range_vt] += 1
                            
                            # Recalculate capacity
                            total_capacity = sum(repaired[vt] * vehicle_ranges[vt] for vt in vehicle_types)
                            
                            if total_capacity >= demand:
                                break
                    
                    if total_capacity >= demand:
                        break
        
        return repaired

    def mutate(self, solution: Dict, size_distance: Tuple, mutation_rate: float = 0.2) -> Dict:
        """Mutate a solution with focus on emissions reduction while maintaining demand fulfillment"""
        vehicles = self.vehicles_by_size_distance[size_distance]
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        vehicle_ranges = {v['vehicle_type']: v['yearly_range'] for v in vehicles}
        
        # Sort vehicles by carbon emissions (lowest first)
        sorted_vehicles = sorted(vehicles, key=lambda v: v['carbon_emissions_per_km'])
        
        # Try multiple mutation strategies
        attempts = 0
        max_attempts = 20
        
        while attempts < max_attempts:
            attempts += 1
            mutated = solution.copy()
            mutation_happened = False
            
            # Strategy 1: Random adjustment - increase or decrease random vehicles
            for vt in vehicle_types:
                if random.random() < mutation_rate:
                    mutation_happened = True
                    change = random.choice([-1, 1])
                    if change == -1 and mutated[vt] > 0:
                        mutated[vt] -= 1
                    elif change == 1:
                        mutated[vt] += 1
            
            # Strategy 2: Emission reduction - swap high emission for low emission
            if random.random() < 0.4:  # 40% chance
                # Find a vehicle with non-zero allocation
                used_types = [vt for vt in vehicle_types if mutated[vt] > 0]
                if used_types:
                    # Sort by emissions
                    used_types_sorted = sorted(used_types, 
                                             key=lambda vt: next(v['carbon_emissions_per_km'] for v in vehicles if v['vehicle_type'] == vt))
                    
                    # Try to reduce a high-emission vehicle
                    if len(used_types_sorted) > 1:
                        high_emission_vt = used_types_sorted[-1]
                        low_emission_vt = used_types_sorted[0]
                        
                        # Only if reducing doesn't make solution invalid
                        temp = mutated.copy()
                        temp[high_emission_vt] -= 1
                        temp[low_emission_vt] += 1
                        
                        if self.is_valid_solution(temp, size_distance):
                            mutated = temp
                            mutation_happened = True
            
            # Strategy 3: Vehicle reduction - if possible, reduce total vehicles
            if random.random() < 0.3:  # 30% chance
                # Sort by range (highest first)
                range_ranking = sorted(vehicle_types, 
                                     key=lambda vt: vehicle_ranges[vt], 
                                     reverse=True)
                
                # Try to replace two low-range vehicles with one high-range vehicle
                for high_range_vt in range_ranking:
                    for low_range_vt in reversed(range_ranking):
                        if high_range_vt == low_range_vt or mutated[low_range_vt] < 2:
                            continue
                        
                        temp = mutated.copy()
                        temp[low_range_vt] -= 2
                        temp[high_range_vt] += 1
                        
                        if self.is_valid_solution(temp, size_distance):
                            mutated = temp
                            mutation_happened = True
                            break
                    
                    if mutation_happened:
                        break
            
            # If no mutation happened, force a simple change
            if not mutation_happened:
                vt = random.choice(vehicle_types)
                temp = mutated.copy()
                if random.random() < 0.5 and temp[vt] > 0:
                    temp[vt] -= 1
                else:
                    temp[vt] += 1
                
                if self.is_valid_solution(temp, size_distance):
                    mutated = temp
                    mutation_happened = True
            
            # Check if valid
            if self.is_valid_solution(mutated, size_distance):
                return mutated
            
            # Try to repair if invalid
            repaired = self._repair_solution(mutated, size_distance)
            if self.is_valid_solution(repaired, size_distance):
                return repaired
        
        # If all attempts fail, return original solution or a repaired version of it
        repaired_original = self._repair_solution(solution, size_distance)
        if self.is_valid_solution(repaired_original, size_distance):
            return repaired_original
        
        # Last resort: create a basic valid solution
        return self._create_basic_valid_solution(size_distance)

    def optimize(self, size_distance: Tuple, generations: int = 250) -> Dict:
        """Run genetic algorithm to find optimal fleet combination"""
        # Generate diverse initial population
        population_size = 150
        population = self.generate_initial_population(size_distance, population_size)
        
        best_solution = None
        best_fitness = float('-inf')
        no_improvement_count = 0
        
        # Track best solutions for comparison
        emissions_by_generation = []
        
        for gen in range(generations):
            # Calculate fitness for entire population
            fitness_scores = [(solution, self.fitness_function(solution, size_distance))
                            for solution in population]
            
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Check if we have a new best solution
            if fitness_scores[0][1] > best_fitness:
                best_solution = fitness_scores[0][0]
                best_fitness = fitness_scores[0][1]
                no_improvement_count = 0
                
                # Calculate and save emissions for this generation
                best_emissions = self.calculate_emissions(best_solution, size_distance)
                emissions_by_generation.append(best_emissions)
            else:
                no_improvement_count += 1
            
            # Early stopping if no improvement for many generations
            if no_improvement_count >= 50:
                break
            
            # Select parents (use tournament selection)
            parents = []
            tournament_size = max(3, len(population) // 20)  # Dynamic tournament size
            for _ in range(len(population)):
                tournament = random.sample(fitness_scores, tournament_size)
                tournament.sort(key=lambda x: x[1], reverse=True)
                parents.append(tournament[0][0])
            
            # Create next generation
            next_generation = []
            
            # Elitism: keep top solutions
            elite_count = max(2, len(population) // 10)
            next_generation.extend([score[0] for score in fitness_scores[:elite_count]])
            
            # Fill the rest through crossover and mutation
            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(parents, 2)
                child1, child2 = self.crossover(parent1, parent2, size_distance)
                
                # Apply mutation with varying rates based on generation
                # Higher mutation early, lower mutation later
                mutation_rate = 0.3 * (1 - min(1.0, gen / (generations * 0.7)))
                
                child1 = self.mutate(child1, size_distance, mutation_rate)
                child2 = self.mutate(child2, size_distance, mutation_rate)
                
                next_generation.append(child1)
                if len(next_generation) < population_size:
                    next_generation.append(child2)
            
            population = next_generation
        
        # Validate that best solution meets demand
        if best_solution and not self.is_valid_solution(best_solution, size_distance):
            best_solution = self._repair_solution(best_solution, size_distance)
            
        return best_solution

    def get_optimized_results(self) -> pd.DataFrame:
        """Run optimization and return results"""
        results = []
        total_carbon_emissions = 0
        
        for size_distance in self.vehicles_by_size_distance.keys():
            print(f"Optimizing for Size: {size_distance[0]}, Distance: {size_distance[1]}...")
            best_solution = self.optimize(size_distance)
            max_vehicles = self.max_vehicles_by_group[size_distance]
            
            # Validate solution meets demand
            vehicles = self.vehicles_by_size_distance[size_distance] 
            demand = vehicles[0]['demand']
            total_capacity = sum(best_solution[v['vehicle_type']] * v['yearly_range'] for v in vehicles)
            
            if total_capacity < demand:
                print(f"Warning: Solution does not meet demand for {size_distance}. Repairing...")
                best_solution = self._repair_solution(best_solution, size_distance)
                total_capacity = sum(best_solution[v['vehicle_type']] * v['yearly_range'] for v in vehicles)
            
            demand_fulfillment = self.calculate_demand_fulfillment(total_capacity, demand)
            size_distance_emissions = 0
            
            # Sort vehicles by emissions to allocate demand to lowest emission vehicles first
            sorted_vehicles = sorted(vehicles, key=lambda v: v['carbon_emissions_per_km'])
            remaining_demand = demand
            
            # Calculate emissions by allocating demand optimally
            for vehicle in sorted_vehicles:
                vehicle_type = vehicle['vehicle_type']
                num_vehicles = best_solution[vehicle_type]
                
                if num_vehicles > 0:
                    # Calculate how much this vehicle type can cover
                    vehicle_capacity = num_vehicles * vehicle['yearly_range']
                    assigned_demand = min(vehicle_capacity, remaining_demand)
                    remaining_demand -= assigned_demand
                    
                    # If no more demand to assign, vehicle is unused
                    if assigned_demand <= 0:
                        continue
                    
                    # Calculate emissions
                    emissions = vehicle['carbon_emissions_per_km'] * assigned_demand
                    size_distance_emissions += emissions
                    
                    # Calculate utilization for this vehicle type
                    utilization = self.calculate_utilization(
                        assigned_demand,
                        num_vehicles,
                        vehicle['yearly_range']
                    )
                    
                    Allocation = vehicle.get('Allocation')
                    Size = vehicle.get('Size')
                    Distance_demand = vehicle.get('Distance_demand')

                    results.append({
                        # "Allocation": f"Size {size_distance[0]}, Distance {size_distance[1]}",
                        "Allocation": Allocation,
                        "Size":Size,
                        "Distance":Distance_demand,
                        "Vehicle": vehicle_type,
                        "Fuel": vehicle['fuel'],
                        "no_of_vehicles": num_vehicles,
                        "Max Vehicles": max_vehicles,
                        "Demand": demand,
                        "Assigned Demand": round(assigned_demand, 2),
                        "Yearly Range": vehicle['yearly_range'],
                        "Utilization": round(utilization, 2),
                        "Demand_Fulfillment": round(demand_fulfillment, 2),
                        "Carbon Emissions": round(emissions, 2),
                        "Emissions Per KM": round(vehicle['carbon_emissions_per_km'], 4)
                    })
            
            total_carbon_emissions += size_distance_emissions
            
            # Verify all demand is allocated
            if abs(remaining_demand) > 0.01:  # Allow small floating-point error
                print(f"Warning: {remaining_demand:.2f} km of demand not allocated for {size_distance}")

        print(f"\nTotal Carbon Emissions: {total_carbon_emissions:.2f}")
        return pd.DataFrame(results), total_carbon_emissions


input_folder = "topsis_result/"
output_folder = "optimized_fleet_results_carbon/"


def process_all_years():
    """Processes all available yearly data files and stores results."""
    yearly_emissions = []  # List to store total emissions per year

    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            year = file.split("_")[-1].split(".")[0]  # Extract year from filename
            csv_path = os.path.join(input_folder, file)

            print(f"\nProcessing year: {year}")
            results_df, total_emissions = main(csv_path)  # Unpack both return values

            # Save results for the year
            output_file = os.path.join(output_folder, f"optimized_fleet_allocation_carbon_{year}.csv")
            results_df.to_csv(output_file, index=False)
            print(f"Results saved for {year} at: {output_file}")

            # Store total emissions for this year
            yearly_emissions.append({"Year": year, "Total Carbon Emissions": total_emissions})

    # Save yearly emissions summary
    emissions_df = pd.DataFrame(yearly_emissions)
    emissions_summary_file = os.path.join(output_folder, "yearly_total_carbon_emissions.csv")
    emissions_df.to_csv(emissions_summary_file, index=False)
    print(f"\nYearly total carbon emissions saved at: {emissions_summary_file}")

def main(csv_path: str):
    """Main function to run the optimization"""
    print("\nRunning optimization with pure carbon emissions minimization...")
    data_df = load_and_preprocess_data(csv_path)
    optimizer = FleetOptimizer(data_df)
    optimized_results, total_emissions = optimizer.get_optimized_results()
    print("\nOptimized Fleet Allocation:")
    print(optimized_results)
    return optimized_results, total_emissions


if __name__ == "__main__":
    process_all_years()
