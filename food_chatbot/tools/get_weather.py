"""Module providing a function to get weather for specified location."""

import os
import requests

from dotenv import load_dotenv


load_dotenv()


def get_weather(location: str, units: str = "metric") -> dict:
    """Function to retrieve weather information on a specific city.

    Args:
        location (str): _description_
        units (str, optional): _description_. Defaults to "metric".

    Returns:
        dict: _description_
    """
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
        timeout=10,
    )

    data = r.json()

    return data["currentConditions"]
