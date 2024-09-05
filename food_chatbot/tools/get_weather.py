"""Module providing a function to get weather for specified location."""

import os
import requests

from dotenv import load_dotenv


load_dotenv()


def get_weather(location: str, units: str = "metric"):
    key = os.getenv("VISUAL_CROSSING_WEATHER_API_KEY")

    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

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
