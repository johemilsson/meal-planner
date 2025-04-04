import os
import yaml
import pytest

from meal_planner.recipe import Recipe


recipe_list = []
for root, _, files in os.walk(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "recipies",
    )):

    recipe_list.extend([os.path.join(root, file) for file in files if file.endswith(".yml")])



@pytest.mark.parametrize("recipe_file", recipe_list)
def test_load_recipies_title(recipe_file):
    """
    Test if the recipe loads correctly.
    """
    recipe = Recipe()
    recipe.load(recipe_file)

    # Check if the recipe has a title
    assert recipe.title is not None

    # # Check if the recipe has a list of ingredients
    # assert isinstance(recipe.ingredients, dict)

    # # Check if the recipe has a list of instructions
    # assert isinstance(recipe.instructions, dict)

    # # Check if the recipe has a time and servings
    # assert isinstance(recipe.time, dict)
    # assert isinstance(recipe.servings, int)

    # # Check if the recipe has a list of tags
    # assert isinstance(recipe.source, str)