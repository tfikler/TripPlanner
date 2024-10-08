from openai import OpenAI
client = OpenAI(api_key="sk-proj-LyFh8uJ9L105OpQqAgPPT3BlbkFJABdGfuYHtbMSCOezr0vd")


def get_top_destinations(start_date, end_date, total_budget, trip_type):
    fomarting = ("Japan\n"
              "Italy\n"
              "France\n"
              "Spain\n"
              "Greece\n")
    prompt = (f"Get the top 5 destinations for a {trip_type} trip from {start_date} to {end_date} "
              f"with a total budget of {total_budget} give only the destination in separate lines without line numbers in this format {fomarting}")
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


def get_daily_plan(destination, start_date, end_date, total_budget, airline, departure_time, flight_price, hotel_price):
    daily_plan_object = {
        "destination": "Whistler, British Columbia",
        "flight_price": 500,
        "hotel_price": 500,
        "budget": 1234,
        "dates": {
            "start": "2024-05-19",
            "end": "2024-05-23"
        },
        "dailyPlan": [
            {
                "date": "2024-05-19",
                "activities": [
                    "Depart from home city using the flight details provided at time provided",
                    "Arrive in Whistler",
                    "Check into accommodation",
                    "Explore Whistler Village"
                ],
                "expenses": 200
            },
            {
                "date": "2024-05-20",
                "activities": [
                    "Skiing/Snowboarding at Whistler Blackcomb",
                    "Lunch on the slopes",
                    "Relax at a spa",
                    "Dinner at a local restaurant"
                ],
                "expenses": 300
            },
            {
                "date": "2024-05-21",
                "activities": [
                    "Hiking or biking in Whistler Mountain",
                    "Visit the Squamish Lil'wat Cultural Centre",
                    "Dinner at a mountain lodge"
                ],
                "expenses": 250
            },
            {
                "date": "2024-05-22",
                "activities": [
                    "Whistler ziplining tour",
                    "Shopping at Whistler's boutique stores",
                    "Dinner at a local pub"
                ],
                "expenses": 200
            },
            {
                "date": "2024-05-23",
                "activities": [
                    "Check out of accommodation",
                    "Souvenir shopping",
                    "Depart from Whistler"
                ],
                "expenses": 100
            }
        ]
    }
    print(total_budget, destination, airline, departure_time, start_date, end_date)
    prompt = (f"Build a daily plan for a trip to {total_budget} from {destination} using flight {airline} on {departure_time} until {start_date} with a total budget of {end_date} with flight price of {flight_price} and hotel price of {hotel_price}"
              f"give it as object like this {daily_plan_object} so i can use it later in my react app - response only with the daily plan object."
              f"Make it valid so i can do JSON.parse on it.")
    print(prompt)
    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
            {"role": "system", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    daily_plan = response.choices[0].message.content
    print(daily_plan)
    return daily_plan


def generate_image_for_the_trip(destination, start_date, end_date, daily_plan):
    prompt = f"Generate an image for a trip to {destination} from {start_date} to {end_date} according to the following daily plan activities: {daily_plan}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url
