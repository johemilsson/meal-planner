"""
Planner class to manage recipes and upload them to TickTick.
"""
import os
import random
import datetime

from recipe import Recipe
from ticktick_api import get_client
from meal_planner import BASIC_INGREDIENTS_FILE

class Planner:
    def __init__(self, start_day=None, debug=False):
        if debug:
            self.client = None
        else:
            self.client = get_client()
        
        if start_day is None:
            self.start_day = datetime.datetime.now()
        else:
            self.start_day = start_day

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
        recipies_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                "recipies",
            )
        )
        
        recipies = []
        for i in range(len(self.weekdays)):
            weekday_dir = os.path.join(recipies_dir, str(i))
            recipies.append(
                [os.path.join(weekday_dir, recipe) for recipe in os.listdir(weekday_dir) if recipe.endswith(".yml")]
                )
                
        
        return recipies

    def sample_recipies(self):
        chosen_recipies = []
        for i in range(len(self.weekdays)):
            recipe_file = random.choice(self.recipies[i])
            chosen_recipies.append(recipe_file)

        return chosen_recipies
    
    def specify_recipies(self):
        """
        Specify the recipes to be used for the week.
        """
        chosen_recipies = []
        for i in range(len(self.weekdays)):
            print(f"Choose a recipe for {self.weekdays[i]}:")
            for j, recipe in enumerate(self.recipies[i]):
                print(f"{j}: {recipe}")
            recipe_index = int(input(f"Choose a recipe for {self.weekdays[i]}: "))
            print(f"You chose {self.recipies[i][recipe_index]} for {self.weekdays[i]}")
            recipe_file = self.recipies[i][recipe_index]
            chosen_recipies.append(recipe_file)

        return chosen_recipies

    def get_ingredients(self, recipies):
        ingredients = set()
        for recipe in recipies:
            recipe_class = Recipe()
            recipe_class.load(recipe)
            ingredients.update(recipe_class.get_ingredients()) # TODO: Sum amount for each ingredient

        with open(BASIC_INGREDIENTS_FILE, "r") as f:
            for ingredient in f:
                ingredient = ingredient.strip()
                if ingredient in ingredients:
                    ingredients.remove(ingredient)

        return ingredients

    def upload_ingredients(self, ingredients):
        day = self.start_day
        start_time = day.replace(hour=17, minute=0)
        end_time = day.replace(hour=22, minute=0)

        task_list = self.client.get_by_fields(name="Shopping")
        
        for ingredient in ingredients:
            task = self.client.task.builder(
                title=ingredient,
                startDate=start_time,
                dueDate=end_time,
            )

            created_task = self.client.task.create(task)
            self.client.task.move(created_task, task_list["id"])

    def upload_recipies(self, recipies):
        day = self.start_day 
        dinners = self.client.get_by_fields(name="Dinners")
        for src in recipies:
            recipe = Recipe()
            recipe.load(src)

            start_time = day.replace(hour=16, minute=30)
            end_time = day.replace(hour=17, minute=30)

            task = self.client.task.builder(
                title=recipe.title,
                startDate=start_time,
                dueDate=end_time,
                content=recipe.source,
            )

            created_task = self.client.task.create(task)
            self.client.task.move(created_task, dinners["id"])
            day += datetime.timedelta(days=1)


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
    start_day = datetime.datetime.now() + datetime.timedelta(days=1)    
    planner = Planner(start_day=start_day)
    my_recipies = planner.sample_recipies()
    ingredients = planner.get_ingredients(my_recipies)
    #my_recipies = planner.specify_recipies()
    print(my_recipies)
    print(ingredients)
    planner.upload_recipies(my_recipies)
    planner.upload_ingredients(ingredients)
