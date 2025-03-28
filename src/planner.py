"""
Planner class to manage recipes and upload them to TickTick.
"""
import os
import random
import datetime

from recipe import Recipe
from ticktick_api import get_client

class Planner:
    def __init__(self):
        self.client = None
        self.weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            ]
        self.recipies = self._get_recipies()


    def _get_recipies(self):
        recipies_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "recipies",
        )
        
        recipies = {}

        for weekday in self.weekdays:
            weekday_dir = os.path.join(recipies_dir, weekday)
            recipies[weekday] = [os.path.join(weekday_dir, recipe) for recipe in os.listdir(weekday_dir) if recipe.endswith(".yml")]
        
        return recipies

    def _get_client(self):
        if not self.client:
            self.client = get_client()

    def sample_recipies(self):
        chosen_recipies = {}
        for weekday in self.recipies:
            recipe_file = random.choice(self.recipies[weekday])
            recipe = Recipe()
            recipe.load(recipe_file)
            chosen_recipies[weekday] = recipe.to_dict()

        return chosen_recipies

    # def get_ingredients(self, recipies):
    #     ingredients = set()
    #     for recipe in recipies:
    #         recipe_class = Recipe()
    #         recipe_path = os.path.join(
    #             os.path.dirname(__file__),
    #             os.pardir,
    #             "recipies",
    #             recipe
    #         )
    #         recipe_class.load(recipe_path)
    #         ingredients.update(recipe_class.get_ingredients()) # TODO: Sum amount for each ingredient

    #     return ingredients

    # def upload_ingredients(self, ingredients):
    #     self._get_client()
    #     tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    #     start_time = tomorrow.replace(hour=17, minute=0)
    #     end_time = tomorrow.replace(hour=22, minute=0)

    #     main_task = self.client.task.builder(
    #         title=f"Shopping list",
    #         startDate=start_time,
    #         dueDate=end_time,
    #     )
    #     created_main_task = self.client.task.create(main_task)
    #     for ingredient in ingredients:
    #         sub_task = self.client.task.builder(title=ingredient)
    #         created_sub_task = self.client.task.create(sub_task)
    #         self.client.task.make_subtask(created_sub_task, parent=created_main_task["id"])

    # def upload_recipies(self, recipies):
    #     day = datetime.datetime.now()
    #     self._get_client()
    #     dinners = self.client.get_by_fields(name="Dinners")
    #     for recipe in recipies:
    #         recipe_class = Recipe()
    #         recipe_path = os.path.join(
    #             os.path.dirname(__file__),
    #             os.pardir,
    #             "recipies",
    #             recipe
    #         )
    #         recipe_class.load(recipe_path)
    #         markdown = recipe_class.to_md()

    #         day += datetime.timedelta(days=1)
    #         start_time = day.replace(hour=16, minute=30)
    #         end_time = day.replace(hour=17, minute=30)

    #         task = self.client.task.builder(
    #             title=recipe_class.title,
    #             startDate=start_time,
    #             dueDate=end_time,
    #             content=markdown
    #         )

    #         created_task = self.client.task.create(task)
    #         self.client.task.move(created_task, dinners["id"])


    # def create_pdfs(self, recipies):
    #     created_pdfs = []
    #     for recipe in recipies:
    #         recipe_class = Recipe()
    #         recipe_path = os.path.join(
    #             os.path.dirname(__file__),
    #             os.pardir,
    #             "recipies",
    #             recipe
    #         )
    #         recipe_class.load(recipe_path)
    #         pdf_name = os.path.splitext(recipe)[0] + ".pdf"
    #         pdf_path = recipe_class.to_pdf(pdf_name)
    #         created_pdfs.append(pdf_path)

    #     return created_pdfs


if __name__ == "__main__":
    planner = Planner()
    my_recipies = planner.sample_recipies()
    # ingredients = planner.get_ingredients(my_recipies)
    print("Recipies:")
    for weekday in my_recipies:
        print(f"{weekday}: {my_recipies[weekday]['title']}")
    

