WEATHER_INFO = {
    "Berlin": {"weather": "mostly sunny", "temperature": 7, "unit": "celsius"},
    "Paris": {"weather": "mostly cloudy", "temperature": 8, "unit": "celsius"},
    "Rome": {"weather": "sunny", "temperature": 14, "unit": "celsius"},
    "Madrid": {"weather": "sunny", "temperature": 10, "unit": "celsius"},
    "London": {"weather": "cloudy", "temperature": 9, "unit": "celsius"},
}


def get_current_weather(location: str):
    if location in WEATHER_INFO:
        return WEATHER_INFO[location]

    else:
        return {"weather": "unkwown", "temperature": "unkwown", "unit": "unkwown"}
