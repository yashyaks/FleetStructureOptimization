import time
from main_tradeoff_topsis import optimization

def main():
    cost_weight, carbon_emissions_weight = 0.5, 0.5
    generations, population_size = 50, 100
    prev_years, min_year, max_year = 7, 2023, 2038

    start_time = time.time()  # Start timing
    optimization(cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year)
    end_time = time.time()  # End timing

    print(f"Optimization function execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
