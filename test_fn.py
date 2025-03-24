from main_tradeoff_topsis import optimization
from pprint import pprint
def main():
    cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year = 0.5, 0.5, 50, 100, 5, 2023, 2038
    optimization(cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year)

if __name__ == "__main__":
    main()