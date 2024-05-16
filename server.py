from openai import OpenAI
import requests
from serpapi import GoogleSearch

client = OpenAI(api_key="sk-proj-LyFh8uJ9L105OpQqAgPPT3BlbkFJABdGfuYHtbMSCOezr0vd")
# client.api_key = "sk-proj-LyFh8uJ9L105OpQqAgPPT3BlbkFJABdGfuYHtbMSCOezr0vd"


def get_user_inputs():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    total_budget = input("Enter the total budget: ")
    trip_type = input("Enter the trip type (ski/beach/city): ")
    return start_date, end_date, total_budget, trip_type


def get_top_destinations(start_date, end_date, total_budget, trip_type):
    prompt = (f"Get the top 5 destinations for a {trip_type} trip from {start_date} to {end_date} "
              f"with a total budget of {total_budget} give only the destination in separate lines without line numbers")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    destinations = response.choices[0].message.content
    destinations = destinations.split("\n")
    return destinations


def get_airports_for_destinations(destinations_list):
    prompt = ("Get the nearest international airports corresponding to the following destinations that have incoming flights from TLV: "
             "") + ", ".join(destinations_list) + " give only the airport code in separate lines without line numbers"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    airports = response.choices[0].message.content
    airports = airports.split("\n")
    return airports


def get_flights_to_destination(outbound_date, return_date, airport_code):
    params = {
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": "TLV",
        "arrival_id": airport_code,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "api_key": "030c17e79dab106881442c7f93cdd621b97b907d2eb8501569ecf6a7faf9591a"
    }

    search = GoogleSearch(params)
    response = search.get_json()
    try:
        best_flights = response.get('best_flights', [])
        if best_flights:
            cheapest_flight = min(best_flights, key=lambda x: x['price'])
            return {
                'price': cheapest_flight['price'],
                'airline': cheapest_flight['flights'][0]['airline'],
                'departure_time': cheapest_flight['flights'][0]['departure_airport']['time'],
                'arrival_time': cheapest_flight['flights'][-1]['arrival_airport']['time'],
                'total_duration': cheapest_flight['total_duration'],
                'layovers': [layover['name'] for layover in cheapest_flight['layovers']]
            }
    except KeyError:
        return None


def main():
    # start_date, end_date, total_budget, trip_type = get_user_inputs()
    start_date = "2024-12-01"
    end_date = "2024-12-31"
    total_budget = "7000$"
    trip_type = "ski"
    destinations_list = get_top_destinations(start_date, end_date, total_budget, trip_type)
    airports_corresponding_to_destinations = get_airports_for_destinations(destinations_list)
    for airport, destinations_list in zip(airports_corresponding_to_destinations, destinations_list):
        cheapest_flight = get_flights_to_destination(start_date, end_date, airport)
        print(f'Cheapest flight to {destinations_list} is {cheapest_flight}')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
