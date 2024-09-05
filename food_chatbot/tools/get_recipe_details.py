import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from haystack import Pipeline
from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)

from ..components import retriever


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
):
    api_key = os.getenv("SPOONACULAR_API_KEY")

    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

    r = requests.get(
        url,
        {
            "includeNutrition": include_nutrition,
            "addWinePairing": add_wine_pairing,
            "addTasteData": add_taste_data,
            "apiKey": api_key,
        },
    )

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
        response = requests.get(recipe_url)
    except requests.RequestException:
        return f"Problem with the url: {recipe_url}"

    soup = BeautifulSoup(response.content, "html.parser")

    result["page_content"] = soup.get_text(strip=True)

    return result
