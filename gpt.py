from openai import OpenAI
client = OpenAI(api_key="sk-proj-LyFh8uJ9L105OpQqAgPPT3BlbkFJABdGfuYHtbMSCOezr0vd")


def get_top_destinations(start_date, end_date, total_budget, trip_type):
    prompt = (f"Get the top 2 destinations for a {trip_type} trip from {start_date} to {end_date} "
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


def get_daily_plan(destination, start_date, end_date, total_budget):
    prompt = f"Build a daily plan for a trip to {destination} from {start_date} to {end_date} with a total budget of {total_budget}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ]
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
