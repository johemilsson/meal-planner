import os
import yaml

from src import ROOT_DIR
from src.pdf_generator import create_recipe_pdf

class Recipe:
    def __init__(self):
        self.title: str = None
        self.ingredients: set = None
        self.instructions: list = None
        self.time = None
        self.servings: int = None
        self.source: str = None


    def load(self, src):
        with open(src, 'r') as fid:
            dct = yaml.safe_load(fid)

        self.title = dct["title"]
        self.ingredients = dct["ingredients"]
        self.instructions = dct["instructions"]
        self.time = dct["time"]
        self.servings = dct["servings"]
        self.source = dct["source"]

    def get_ingredients(self):
        ingredients_list = set()
        for item in self.ingredients.values():
            for dct in item:
                ingredients_list.add(list(dct.keys())[0])

        if "Vatten" in ingredients_list:
            ingredients_list.remove("Vatten") # TODO: Create a separate list of unneeded ingredients

        return ingredients_list

    def to_pdf(self, filename):
        pdfs_dir = os.path.join(ROOT_DIR, "pdfs")
        os.makedirs(pdfs_dir, exist_ok=True)
        filepath = os.path.join(pdfs_dir, filename)
        create_recipe_pdf(
            self.title,
            self.ingredients,
            self.instructions,
            self.time,
            self.servings,
            filepath
        )

        return filepath

    def save(self, filename: str, directory=None):
        save_dct = {
            "name": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

        if directory is None:
            directory = os.getcwd()

        with open(os.path.join(directory, filename), "w") as fid:
            yaml.safe_dump(save_dct, fid)

if __name__ == "__main__":
    recipe = Recipe()
    recipe.load("/home/johannes/Projects/Python/meal-planner/recipies/korv_stroganoff.yml")
    ingredients = recipe.get_ingredients()
    recipe.to_pdf("test.pdf")
