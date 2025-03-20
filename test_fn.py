from demand import VehicleAllocation
from pprint import pprint
def main():
    va = VehicleAllocation()
    df = va.allocate_vehicles(2023)
    pprint(df)

if __name__ == "__main__":
    main()