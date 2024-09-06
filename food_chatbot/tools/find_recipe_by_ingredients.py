"""Module to call API to retrieve recipes that use specified ingredients"""

import os
import requests

from dotenv import load_dotenv


load_dotenv()


def find_recipe_by_ingredients(
    ingredients: str, number: int = 2, ranking: int = 1, ignore_pantry: bool = True
) -> list:
    """Function to find recipes by ingredients.

    Args:
        ingredients (str): List of ingredients to be used in a recipe.
        number (int, optional): _description_. Defaults to 2.
        ranking (int, optional): _description_. Defaults to 1.
        ignore_pantry (bool, optional): _description_. Defaults to True.

    Returns:
        list: _description_
    """
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
        timeout=10,
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
