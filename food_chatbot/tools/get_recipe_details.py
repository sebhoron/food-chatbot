"""Module defining get_recipe tool"""

import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from haystack import Pipeline
from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)

from food_chatbot.components import retriever


load_dotenv()

document_store = MongoDBAtlasDocumentStore(
    database_name="recipe_details",
    collection_name="food_chatbot",
    vector_search_index="embedding_index",
)

recipe_details_pip = Pipeline()
recipe_details_pip.add_component("retriever", retriever)


def get_recipe_details(
    recipe_id: int,
    include_nutrition: bool = False,
    add_wine_pairing: bool = False,
    add_taste_data: bool = False,
) -> dict:
    """Function to get recipe details.

    Args:
        recipe_id (int): Id of the recipe
        include_nutrition (bool, optional): Include nutrition data ps. Defaults to False.
        add_wine_pairing (bool, optional): Add a wine pairing to the recipe. Defaults to False.
        add_taste_data (bool, optional): Add taste data to the recipe. Defaults to False.

    Returns:
        dict: _description_
    """
    api_key = os.getenv("SPOONACULAR_API_KEY")

    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

    try:
        r = requests.get(
            url,
            {
                "includeNutrition": include_nutrition,
                "addWinePairing": add_wine_pairing,
                "addTasteData": add_taste_data,
                "apiKey": api_key,
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        print("Timed out")

    data = r.json()

    result = {
        k: v
        for k, v in data.items()
        if k
        in [
            "title",
            "image",
            "servings",
            "readyInMinutes",
            "pricePerServing",
            "cheap",
            "summary",
            "winePairing",
        ]
    }

    recipe_url = data["sourceUrl"]

    try:
        response = requests.get(recipe_url, timeout=10)
    except requests.RequestException:
        return f"Problem with the url: {recipe_url}"

    soup = BeautifulSoup(response.content, "html.parser")

    result["page_content"] = soup.get_text(strip=True)

    return result
