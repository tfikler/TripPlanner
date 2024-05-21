from serpapi import GoogleSearch

# TODO:
#   1. Adjust the max_price budget depending on the left amount after flight and divide by the nights
#   2. Check if we want to deal with the flight back to TLV

iri_api_key = "6f65010aaf06a3011f862d0c37dc8f1d8632ac19fc22c6b54981a859d0fa75c9"

def adjust_min_budget(total_budget):
    min_budget = 0
    if 5000 < total_budget < 10000:
        min_budget = total_budget // 10
    if total_budget < 5000:
        min_budget = 500
    if total_budget > 10000:
        min_budget = 1000
    return min_budget


def get_hotel_in_destination(start_date, end_date, destination, budget_post_flight):
    min_budget = adjust_min_budget(int(budget_post_flight))
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
        "max_price": budget_post_flight,
        "min_price": min_budget,
        "next_page_token": ""
    }

    search1 = GoogleSearch(params)
    response = search1.get_json()
    # next_page_token1 = response.get('serpapi_pagination', None)
    # if next_page_token1:
    #     params['next_page_token'] = next_page_token1['next_page_token']
    #     print(f'Next page token: {params["next_page_token"]} second page search')
    #
    # search = GoogleSearch(params)
    # response = search.get_json()
    # next_page_token2 = response.get('serpapi_pagination', None)
    # if next_page_token2:
    #     params['next_page_token'] = next_page_token2['next_page_token']
    #     print(f'Next page token: {params["next_page_token"]} third page search')
    #     search = GoogleSearch(params)
    #     response = search.get_json()

    print(f'hotel response: {response} on destination {destination}')
    try:
        properties = response.get('properties', [])
        if properties:
            most_expensive_hotel = max(properties, key=lambda x: x['rate_per_night']['extracted_lowest'])
            return {
                'name': most_expensive_hotel['name'],
                'price': most_expensive_hotel['total_rate']['lowest'],
            }
    except Exception as e:
        print(f'Error in get_hotel_in_destination: {e}')
        return None


def departure_flights(outbound_date, return_date, airport_code):
    print(airport_code)
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
    print(f'departure flights response: {response} in code {airport_code}')
    try:
        best_flights = response.get('best_flights', [])
        if best_flights:
            cheapest_flight = min(best_flights, key=lambda x: x['price'])
            print(f'cheapest_flight according to airport code: {airport_code} is {cheapest_flight}')
            return {
                'price': cheapest_flight['price'],
            }
        else:
            print(f'best_flights is empty, trying other_flights')
            best_flight = response['other_flights'][0]['price']
            return {
                'price': best_flight,
            }
    except Exception as e:
        print(f'Error in departure_flights: {e}')
        return None


def return_flights(outbound_date, return_date, airport_code, departure_token):
    params = {
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": "TLV",
        "arrival_id": airport_code,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "api_key": "f4173a9c84a401366b706d95b33b4e1633cf3ecff0e24fd9db964897763a15f0",
        "departure_token": departure_token
    }

    search = GoogleSearch(params)
    response = search.get_json()
    print(f'return flights response: {response} end here')
    try:
        return response['other_flights'][0]['flights'][0]['departure_airport']['name']
    except KeyError:
        return None