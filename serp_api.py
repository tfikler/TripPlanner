from serpapi import GoogleSearch

# TODO:
#   1. Adjust the max_price budget depending on the left amount after flight and divide by the nights
#   2. Check if we want to deal with the flight back to TLV

iri_api_key = "0a67b2d50f48210578fee708cbbaf99aaaacb765c59414c86ad6bafbcdd3be9b"

def adjust_min_budget(total_budget):
    min_budget = 0
    if 5000 < total_budget < 10000:
        min_budget = total_budget // 10
    if total_budget < 5000:
        min_budget = 500
    if total_budget > 10000:
        min_budget = 1000
    return min_budget


def get_hotel_in_destination(start_date, end_date, destination, total_budget):
    min_budget = adjust_min_budget(int(total_budget))
    params = {
        "api_key": iri_api_key,
        "engine": "google_hotels",
        "q": destination,
        "hl": "en",
        "gl": "us",
        "check_in_date": start_date,
        "check_out_date": end_date,
        "currency": "USD",
        "sort_by": "3",
        "max_price": total_budget,
        "min_price": min_budget,
        "next_page_token": ""
    }

    search1 = GoogleSearch(params)
    response = search1.get_json()
    next_page_token = response.get('serpapi_pagination', None)
    if next_page_token:
        params['next_page_token'] = next_page_token['next_page_token']
        print(f'Next page token: {params["next_page_token"]} second page search')

    search = GoogleSearch(params)
    response = search.get_json()
    next_page_token = response.get('serpapi_pagination', None)
    if next_page_token:
        params['next_page_token'] = next_page_token['next_page_token']
        print(f'Next page token: {params["next_page_token"]} third page search')
        search = GoogleSearch(params)
        response = search.get_json()

    try:
        properties = response.get('properties', [])
        if properties:
            most_expensive_hotel = max(properties, key=lambda x: x['rate_per_night']['extracted_lowest'])
            return {
                'name': most_expensive_hotel['name'],
                'price': most_expensive_hotel['total_rate']['lowest'],
                'rating': most_expensive_hotel.get('overall_rating', 'N/A'),
                'address': most_expensive_hotel.get('gps_coordinates', 'N/A'),
                'link': most_expensive_hotel.get('link', 'N/A')
            }
    except KeyError:
        return None


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
        "api_key": iri_api_key
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