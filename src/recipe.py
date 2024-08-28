import os

import yaml

class Recipe:
    def __init__(self):
        self.name: str = None
        self.ingredients: set = None
        self.instructions: list = None


    def load(self, src):
        with open(src, 'r') as fid:
            dct = yaml.safe_load(fid)

        self.name = dct["name"]
        self.ingredients = dct["ingredients"]
        self.instructions = dct["instructions"]

    def get_ingredients(self):
        ingredients_list = set()
        for dct in self.ingredients:
            ingredients_list.add(list(dct.keys())[0])

        return ingredients_list


    def save(self, filename: str, directory=None):
        save_dct = {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

        if directory is None:
            directory = os.getcwd()

        with open(os.path.join(directory, filename), "w") as fid:
            yaml.safe_dump(save_dct, fid)

if __name__ == "__main__":
    recipe = Recipe()
    recipe.load("/home/johannes/Projects/Python/meal-planner/src/recipies/test.yml")
    ingredients = recipe.get_ingredients()
