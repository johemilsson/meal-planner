import os

import yaml

class Recipe:
    def __init__(self):
        self.name: str = None
        self.ingredients: set = None
        self.instructions: list = None

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
    recipe.name = "Test"
    recipe.ingredients = set([("Agg","5"), ("Mjol", "3dl"), ("Socker", "3dl")])
    recipe.instructions = ["Blanda", "Servera", "Njut"]
    recipe.save("test.yml")