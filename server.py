from gpt import get_top_destinations, get_airports_for_destinations, get_daily_plan, generate_image_for_the_trip
from serp_api import get_flights_to_destination, get_hotel_in_destination


def get_user_inputs():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    total_budget = input("Enter the total budget: ")
    trip_type = input("Enter the trip type (ski/beach/city): ")
    return start_date, end_date, total_budget, trip_type


def get_user_desired_trip(destinations_list, hotels_list):
    for i, (destination, hotel) in enumerate(zip(destinations_list, hotels_list)):
        print(f'{i + 1}. {destination} - {hotel["name"]}')
    trip = input("Enter the trip number you would like: ")
    return destinations_list[int(trip) - 1], hotels_list[int(trip) - 1]


def main():
    # start_date, end_date, total_budget, trip_type = get_user_inputs()
    start_date = "2024-12-27"
    end_date = "2024-12-31"
    total_budget = "7000"
    trip_type = "beach"
    destinations_list = get_top_destinations(start_date, end_date, total_budget, trip_type)
    hotels_list = []
    flights_list = []
    airports_corresponding_to_destinations = get_airports_for_destinations(destinations_list)
    for airport, destination in zip(airports_corresponding_to_destinations, destinations_list):
        cheapest_flight = get_flights_to_destination(start_date, end_date, airport)
        flights_list.append(cheapest_flight)
        print(f'Cheapest flight to {destination} is {cheapest_flight}')
        expensive_hotel = get_hotel_in_destination(start_date, end_date, destination, total_budget)
        hotels_list.append(expensive_hotel)
        print(f'Most expensive hotel in {destination} is {expensive_hotel["name"]} with a price of {expensive_hotel["price"]}')
    chosen_destination, chosen_hotel = get_user_desired_trip(destinations_list, hotels_list)
    daily_plan = get_daily_plan(chosen_destination, start_date, end_date, total_budget)
    image_url = generate_image_for_the_trip(chosen_destination, start_date, end_date, daily_plan)
    print(image_url)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
