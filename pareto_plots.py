import matplotlib.pyplot as plt
import numpy as np

def plot_pareto_front(pareto_solutions):
    costs = []
    emissions = []

    for solution, cost, emission in pareto_solutions:
        costs.append(cost)
        emissions.append(emission)
    
    costs = np.array(costs)
    emissions = np.array(emissions)
    
    # Sort by cost to draw the Pareto front
    sorted_indices = np.argsort(costs)
    costs = costs[sorted_indices]
    emissions = emissions[sorted_indices]

    plt.figure(figsize=(10, 6))
    plt.scatter(costs, emissions, color='blue', label='Solutions')
    plt.plot(costs, emissions, color='red', label='Pareto Front')
    plt.xlabel('Total Cost ($)')
    plt.ylabel('Total Emissions (kg CO₂)')
    plt.title('Pareto Front for Fleet Optimization')
    plt.legend()
    plt.grid()
    plt.show()

# Example usage:
# Suppose `pareto_solutions` is obtained from the optimizer
# optimizer = MultiObjectiveFleetOptimizer(data)
# pareto_solutions = optimizer.pareto_rank(population, size_distance)
# plot_pareto_front(pareto_solutions)

# Let me know if you’d like me to integrate this directly into your existing code!
