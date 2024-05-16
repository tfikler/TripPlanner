from serpapi import GoogleSearch


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