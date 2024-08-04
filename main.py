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