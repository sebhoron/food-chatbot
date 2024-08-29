import os
import requests

from dotenv import load_dotenv


load_dotenv()


def find_recipe_by_ingredients(
    ingredients: str, number: int = 2, ranking: int = 1, ignore_pantry: bool = True
):
    apiKey = os.getenv("FOOD_API")

    url = f"https://api.spoonacular.com/recipes/findByIngredients"

    r = requests.get(
        url,
        {
            "ingredients": ingredients,
            "number": number,
            "ranking": ranking,
            "ignore_pantry": ignore_pantry,
            "apiKey": apiKey,
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
