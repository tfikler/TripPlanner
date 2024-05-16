from gpt import get_top_destinations, get_airports_for_destinations
from serp_api import get_flights_to_destination


def get_user_inputs():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    total_budget = input("Enter the total budget: ")
    trip_type = input("Enter the trip type (ski/beach/city): ")
    return start_date, end_date, total_budget, trip_type


def main():
    # start_date, end_date, total_budget, trip_type = get_user_inputs()
    start_date = "2024-12-01"
    end_date = "2024-12-31"
    total_budget = "7000$"
    trip_type = "beach"
    destinations_list = get_top_destinations(start_date, end_date, total_budget, trip_type)
    airports_corresponding_to_destinations = get_airports_for_destinations(destinations_list)
    for airport, destinations_list in zip(airports_corresponding_to_destinations, destinations_list):
        cheapest_flight = get_flights_to_destination(start_date, end_date, airport)
        print(f'Cheapest flight to {destinations_list} is {cheapest_flight}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
