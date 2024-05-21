from gpt import get_top_destinations, get_airports_for_destinations, get_daily_plan, generate_image_for_the_trip
from serp_api import departure_flights, get_hotel_in_destination, return_flights


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
    trip_type = "ski"
    destinations_list = get_top_destinations(start_date, end_date, total_budget, trip_type)
    hotels_list = []
    flights_list = []
    return_flights_list = []
    total_budget_int = int(total_budget)
    airports_corresponding_to_destinations = get_airports_for_destinations(destinations_list)
    
    for airport, destination in zip(airports_corresponding_to_destinations, destinations_list):
        cheapest_flight = departure_flights(start_date, end_date, airport)
        flights_list.append(cheapest_flight)
        print(f'Cheapest flight to {destination} is {cheapest_flight}')
        
        cheapest_return_flight = return_flights(start_date, end_date, airport,cheapest_flight["departure_token"])
        return_flights_list.append(cheapest_return_flight)
        
        print(f'Cheapest return flight from {destination} is {cheapest_return_flight}')
        
        budget_post_flight = total_budget_int - cheapest_flight["price"]
        expensive_hotel = get_hotel_in_destination(start_date, end_date, destination, budget_post_flight)
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
