import os
import requests

from dotenv import load_dotenv


load_dotenv()


def find_recipe_by_ingredients(
    ingredients: str, number: int = 2, ranking: int = 1, ignore_pantry: bool = True
):
    api_key = os.getenv("SPOONACULAR_API_KEY")

    url = "https://api.spoonacular.com/recipes/findByIngredients"

    r = requests.get(
        url,
        {
            "ingredients": ingredients,
            "number": number,
            "ranking": ranking,
            "ignorePantry": ignore_pantry,
            "apiKey": api_key,
        },
    )

    data = r.json()

    result = [
        {
            k: v
            for k, v in recipe.items()
            if k not in ["missedIngredients", "unusedIngredients"]
        }
        for recipe in data
    ]

    return result
