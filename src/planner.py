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
import random
import datetime

from src.recipe import Recipe
from src.ticktick_api import get_client

class Planner:
    def __init__(self):
        self.recipies = self._get_recipies()
        self.client = None


    @staticmethod
    def _get_recipies():
        recipies_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "recipies",
        )
        recipies = [
            recipe for recipe in os.listdir(recipies_dir) if recipe.endswith(".yml")
        ]

        # Remove the template recipe
        recipies.remove("template.yml")

        return recipies

    def _get_client(self):
        if not self.client:
            self.client = get_client()

    def sample_recipies(self, number_of_days):
        chosen_recipies = random.sample(self.recipies, number_of_days)

        return chosen_recipies

    def get_ingredients(self, recipies):
        ingredients = set()
        for recipe in recipies:
            recipe_class = Recipe()
            recipe_path = os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                "recipies",
                recipe
            )
            recipe_class.load(recipe_path)
            ingredients.update(recipe_class.get_ingredients()) # TODO: Sum amount for each ingredient

        return ingredients

    def upload_ingredients(self, ingredients):
        self._get_client()
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        start_time = tomorrow.replace(hour=17, minute=0)
        end_time = tomorrow.replace(hour=22, minute=0)

        main_task = self.client.task.builder(
            title=f"Shopping list",
            startDate=start_time,
            dueDate=end_time,
        )
        created_main_task = self.client.task.create(main_task)
        for ingredient in ingredients:
            sub_task = self.client.task.builder(title=ingredient)
            created_sub_task = self.client.task.create(sub_task)
            self.client.task.make_subtask(created_sub_task, parent=created_main_task["id"])

    def upload_recipies(self, recipies):
        day = datetime.datetime.now()
        self._get_client()
        dinners = self.client.get_by_fields(name="Dinners")
        for recipe in recipies:
            recipe_class = Recipe()
            recipe_path = os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                "recipies",
                recipe
            )
            recipe_class.load(recipe_path)
            markdown = recipe_class.to_md()

            day += datetime.timedelta(days=1)
            start_time = day.replace(hour=16, minute=30)
            end_time = day.replace(hour=17, minute=30)

            task = self.client.task.builder(
                title=recipe_class.title,
                startDate=start_time,
                dueDate=end_time,
                content=markdown
            )

            created_task = self.client.task.create(task)
            self.client.task.move(created_task, dinners["id"])


    def create_pdfs(self, recipies):
        created_pdfs = []
        for recipe in recipies:
            recipe_class = Recipe()
            recipe_path = os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                "recipies",
                recipe
            )
            recipe_class.load(recipe_path)
            pdf_name = os.path.splitext(recipe)[0] + ".pdf"
            pdf_path = recipe_class.to_pdf(pdf_name)
            created_pdfs.append(pdf_path)

        return created_pdfs




if __name__ == "__main__":
    planner = Planner()
    my_recipies = planner.sample_recipies(5)
    ingredients = planner.get_ingredients(my_recipies)
    planner.upload_ingredients(ingredients)
    planner.upload_recipies(my_recipies)
    # pdfs = planner.create_pdfs(my_recipies)

