import requests
import json
from config.settings import OPENWEATHER_API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(cities):

    result = {}


    for city in cities:

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }


        response = requests.get(
            BASE_URL,
            params=params
        )


        if response.status_code != 200:
            result[city] = {
                "error": "Unable to fetch weather"
            }
            continue


        data = response.json()


        result[city] = {
            "temperature": f"{data['main']['temp']}°C",
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }


    return json.dumps(result)
