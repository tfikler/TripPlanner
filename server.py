from gpt import get_top_destinations, get_airports_for_destinations, get_daily_plan, generate_image_for_the_trip
from serp_api import departure_flights, get_hotel_in_destination, return_flights

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    start_date: str
    end_date: str
    total_budget: str
    trip_type: str


class DailyPlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    total_budget: str
    airline: str
    departure_time: str
    flight_price: float
    hotel_price: float


class GenerateImageRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    daily_plan: str


@app.post("/get_trips")
def get_trips(request: TripRequest):
    destinations_list = get_top_destinations(request.start_date, request.end_date, request.total_budget, request.trip_type)
    hotels_list = []
    flights_list = []
    return_flights_list = []
    airports_corresponding_to_destinations = get_airports_for_destinations(destinations_list)
    print(destinations_list)

    for airport, destination in zip(airports_corresponding_to_destinations, destinations_list):
        cheapest_flight = departure_flights(request.start_date, request.end_date, airport)
        print('cheapest_flight', cheapest_flight)
        flights_list.append(cheapest_flight)
        if cheapest_flight is None:
            break
        budget_post_flight = int(request.total_budget) - cheapest_flight['price']
        print('budget_post_flight', budget_post_flight)
        expensive_hotel = get_hotel_in_destination(request.start_date, request.end_date, destination, budget_post_flight)
        print('expensive_hotel', expensive_hotel)
        hotels_list.append(expensive_hotel)

    print("destinations_list", destinations_list)
    print("hotels_list", hotels_list)
    if None in hotels_list or None in flights_list:
        trips = []
    else:
        trips = [{'destination': dest, 'hotel': hotel['name'], 'flight_price': flight['price'], 'airline': flight['airline'], 'departure_time': flight['departure_time'], 'hotel_price': hotel['price']} for dest, hotel, flight in zip(destinations_list, hotels_list, flights_list)]
    # trips = [
    #     {
    #         "destination": "Maldives",
    #         "hotel": "The Nautilus Maldives",
    #         "flight_price": 1000,
    #         "airline": "El Al",
    #         "departure_time": "2024-12-27 08:00",
    #         "hotel_price": "1000$"
    #
    #     },
    #     {
    #         "destination": "Hawaii",
    #         "hotel": "ESPACIO The Jewel of Waikiki",
    #         "flight_price": 2000,
    #         "airline": "El Al",
    #         "departure_time": "2024-12-27 08:00",
    #         "hotel_price": "1000$"
    #     },
    #     {
    #         "destination": "Bora Bora",
    #         "hotel": "Four Seasons Resort Bora Bora",
    #         "flight_price": 3000,
    #         "airline": "El Al",
    #         "departure_time": "2024-12-27 08:00",
    #         "hotel_price": "1000"
    #     },
    #     {
    #         "destination": "Bahamas",
    #         "hotel": "Rock House Hotel and Restaurant",
    #         "flight_price": 4000,
    #         "airline": "El Al",
    #         "departure_time": "2024-12-27 08:00",
    #         "hotel_price": "1000"
    #     },
    #     {
    #         "destination": "Fiji",
    #         "hotel": "Vacala Bay Resort",
    #         "flight_price": 5000,
    #         "airline": "El Al",
    #         "departure_time": "2024-12-27 08:00",
    #         "hotel_price": "1000"
    #     }
    # ]
    print(f'trips before return: {trips}')
    return trips


@app.post("/daily_plan")
def daily_plan(request: DailyPlanRequest):
    daily_planning = get_daily_plan(request.start_date, request.end_date, request.total_budget, request.destination, request.airline, request.departure_time, request.flight_price, request.hotel_price)
    return daily_planning


@app.post("/generate_image")
def generate_image(request: GenerateImageRequest):
    image_url = generate_image_for_the_trip(request.destination, request.start_date, request.end_date, request.daily_plan)
    return image_url

# def get_user_inputs():
#     start_date = input("Enter the start date (YYYY-MM-DD): ")
#     end_date = input("Enter the end date (YYYY-MM-DD): ")
#     total_budget = input("Enter the total budget: ")
#     trip_type = input("Enter the trip type (ski/beach/city): ")
#     return start_date, end_date, total_budget, trip_type


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
    import uvicorn
    uvicorn.run(app, port=8000)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
