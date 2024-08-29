"""
1. Get all recipies from directory
2. Assign recipe to each day of the week
3. Consolidate all ingredients
4. Upload ingredients to google keep (using gkeepapi)
5. Print pdf with recipies and day

import random

random.sample(list, n) # Select n unique items from list
"""
import os

class Planner:
    def __init__(self):
        self.recipies = self._get_recipies()

    @staticmethod
    def _get_recipies():
        recipies_dir = os.path.join(
            os.path.dirname(__file__),
            "recipies",
        )
        recipies = [
            recipe for recipe in os.listdir(recipies_dir) if recipe.endswith(".yml")
        ]

        return recipies

if __name__ == "__main__":
    planner = Planner()