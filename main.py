import pprint

### Example usage of formulas class

from utilities.calculations import formulas
formulas = formulas()

vehicle_details = formulas.vehciles_purchased_in_year(
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
    ('BEV_S1_2023', 'BEV', 'S1', 2023, 187000, 102000, 50000, 10),
    ('Diesel_S2_2023', 'Diesel', 'S2', 2020, 104000, 106000, 60000, 5),
    ('LNG_S3_2023', 'LNG', 'S3', 2023, 151136, 73000, 45000, 8)
]
total_fleet_insurance_cost = formulas.yearly_insurace_cost(current_fleet_details, 2025)
print('\noutput of total_fleet_insurance_cost:')
pprint.pprint(total_fleet_insurance_cost)