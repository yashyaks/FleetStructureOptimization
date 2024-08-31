import pprint

### Example usage of formulas class

from utilities.costs import Costs
formulas = Costs()

vehicle_details = formulas.vehciles_that_can_be_purchased_in_year(
    year = '2023'
)
print('\noutput of vehciles_purchased_in_year:')
pprint.pprint(vehicle_details)

units_purchased = [
    ('BEV_S1_2023', 0),
    ('BEV_S2_2023', 0),
    ('BEV_S4_2023', 0),
    ('BEV_S3_2023', 0),
    ('Diesel_S1_2023', 0),
    ('Diesel_S2_2023', 0),
    ('Diesel_S4_2023', 0),
    ('Diesel_S3_2023', 1),
    ('LNG_S1_2023', 1),
    ('LNG_S2_2023', 0),
    ('LNG_S4_2023', 0),
    ('LNG_S3_2023', 0)
]
purchase_summary = formulas.cost_of_buying_vehicles_in_year(
    vehicle_details,
    units_purchased
)
print('\noutput of cost_of_buying_vehicles_in_year:')
pprint.pprint(purchase_summary)

cost_profile = formulas.cost_profiles(
    year_of_purchase = 2023,
    op_year = 2025
)
print('\noutput of cost_profiles:')
pprint.pprint(cost_profile)

current_fleet_details = [
    ('BEV_S1_2023', 'BEV', 'S1', 2023, 187000, 102000, 'D1', 10, 450, 'Electricity'),
    ('Diesel_S2_2023', 'Diesel', 'S2', 2020, 104000, 106000, 'D4', 5, 320, 'B20'),
    ('LNG_S3_2023', 'LNG', 'S3', 2023, 151136, 73000, 'D4', 8, 500, 'LNG')
]

total_fleet_insurance_cost = formulas.yearly_insurance_cost(current_fleet_details, 2025)
print('\noutput of total_fleet_insurance_cost:')
pprint.pprint(total_fleet_insurance_cost)

current_fleet_details = [
    ('BEV_S1_2023', 'BEV', 'S1', 2023, 187000, 102000, 'D1', 10, 450, 'Electricity'),
    ('Diesel_S2_2023', 'Diesel', 'S2', 2020, 104000, 106000, 'D4', 5, 320, 'B20'),
    ('LNG_S3_2023', 'LNG', 'S3', 2023, 151136, 73000, 'D4', 8, 500, 'LNG')
]

total_fleet_maintainence_cost = formulas.yearly_maintenance_cost(current_fleet_details, 2025)
print('\noutput of total_fleet_maintainence_cost:')
pprint.pprint(total_fleet_maintainence_cost)

current_vehicle_details = ('BEV_S1_2023', 'BEV', 'S1', 2023, 187000, 102000, 'D1', 10, 450, 'Electricity')
fuel_profile = formulas.fuel_profile(current_vehicle_details, 2038)
print('\noutput of fuel_profile:')
pprint.pprint(fuel_profile)

current_fleet_details = [
    ('BEV_S1_2023', 'BEV', 'S1', 2023, 187000, 102000, 'D1', 10, 450, 'Electricity', 0.8193),
    ('Diesel_S2_2023', 'Diesel', 'S2', 2020, 104000, 106000, 'D4', 5, 320, 'B20', 0.9635),
    ('LNG_S3_2023', 'LNG', 'S3', 2023, 151136, 73000, 'D4', 8, 500, 'LNG', 0.9868)
]
yearly_fuel_cost = formulas.yearly_fuel_cost(current_fleet_details, 2025)
print('\noutput of yearly_fuel_cost:')
pprint.pprint(yearly_fuel_cost)

fleet_for_resale = [
    ('BEV_S1_2023', 'BEV', 2023, 187000, 2),
    ('Diesel_S2_2023', 'Diesel', 2020, 104000,  1),
    ('LNG_S3_2023', 'LNG', 2023, 151136, 3)
]
total_recievables = formulas.recievables_from_sale_of_vehicle(fleet_for_resale, 2025)
print('\noutput of recievables_from_sale_of_vehicle:')
pprint.pprint(total_recievables)

total_cost = formulas.total_fleet_cost_for_current_op_year(vehicle_details, units_purchased, current_fleet_details, fleet_for_resale, 2025)
print('\noutput of total_fleet_cost_for_current_op_year:')
pprint.pprint(total_recievables)


### Example usage of CarbonEmissions class
from utilities.carbon_emmissions import CarbonEmissions
carbon_emissions = CarbonEmissions()

carbon_emissions_limit = carbon_emissions.carbon_emissions_limit(2025)
print('\noutput of carbon_emissions_limit:')
pprint.pprint(carbon_emissions_limit)

total_carbon_emissions = carbon_emissions.total_carbon_emmissions(current_fleet_details, 2025)
print('\noutput of total_carbon_emissions:')
pprint.pprint(total_carbon_emissions)