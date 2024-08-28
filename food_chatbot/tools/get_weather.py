import os
import requests

from dotenv import load_dotenv


load_dotenv()


def get_weather(location: str, units: str = "metric"):
    key = os.getenv("WEATHER_API")

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    r = requests.get(
        url,
        {
            "location": location,
            "key": key,
            "unitGroup": units,
            "include": "current",
        },
    )

    data = r.json()

    return data["currentConditions"]
