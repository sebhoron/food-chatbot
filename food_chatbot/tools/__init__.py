from .rag_pipeline_func import rag_pipeline_func
from .get_weather import get_weather

tools = [
    {
        "type": "function",
        "function": {
            "name": "rag_pipeline_func",
            "description": "Get information about where people live",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to use in the search. Infer this from the user's message. It should be a question or a statement",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather data for the specified location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country abbreviation, e.g. London,UK",
                    },
                    "units": {
                        "type": "string",
                        "description": "The units that will be used when returning weather data, e.g. 'us' for imperial/fahrenheit or 'metric' for metric/celsius",
                        "enum": ["us", "metric", "uk", "base"],
                    },
                },
                "required": ["location", "units"],
            },
        },
    },
]
