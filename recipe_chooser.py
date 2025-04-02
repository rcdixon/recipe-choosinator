from tabulate import tabulate
import pandas as pd
from random import sample
from InquirerLib import prompt
import os
from math import isnan
# from InquirerPy.validator import EmptyInputValidator

def isNaN(num):
    return num != num

potential_choosers = ["Rob", "Bob"]

recipe_datatable = pd.read_csv("/home/rankrc/dev/recipe-choosinator/recipes.csv")
random_five_recipes = recipe_datatable.sample(n=5)

os.system('clear')
number_of_recipes_question = {
    "type": "number",
    "message": "How many recipes do you want to choose?",
    "name": "number_of_rounds",
    "min_allowed": 1,
    "default": 0
}
number_of_rounds = int(prompt(number_of_recipes_question)["number_of_rounds"])

all_chosen_recipes = pd.DataFrame(columns=recipe_datatable.columns)
os.system('clear')


for round_num in range(number_of_rounds):
    first_chooser = sample(potential_choosers, 1)[0]
    second_chooser = sample([chooser for chooser in potential_choosers if chooser != first_chooser], 1)[0]
    random_five_recipes = random_recipes = recipe_datatable.sample(n=5)
    random_recipe_display = {}

    for row_number in range(len(random_five_recipes)):
        random_recipe_display[
            f'- {random_five_recipes.iloc[row_number]["name"]} ({random_five_recipes.iloc[row_number]["meal_category"]})'
        ] = random_five_recipes[random_five_recipes["name"] == random_five_recipes.iloc[row_number]["name"]]

    first_recipe_question = {
        "type": "checkbox",
        "message": f"Here are five recipes. {first_chooser}, pick two:",
        "choices": random_recipe_display.keys(),
        "validate": lambda result: len(result) == 2,
        "instruction": "(use space bar to select)",
        "invalid_message": "Must choose 2 recipes",
        "name": "chosen_recipes"
    }

    first_round_recipes = prompt(first_recipe_question)["chosen_recipes"]
    os.system('clear')

    final_recipe_question = {
        "type": "list",
        "message": f"{second_chooser}, pick one of those recipes:",
        "choices": first_round_recipes,
        "multiselect": False,
        "name": "chosen_recipe"
    }

    final_recipe = prompt(final_recipe_question)["chosen_recipe"]
    os.system('clear')
    all_chosen_recipes = pd.concat([all_chosen_recipes, random_recipe_display[final_recipe]])

    print(f'{final_recipe} added to final list')

os.system('clear')
print("Here is your final list of recipes:\n")

recipes_formatted = (all_chosen_recipes[['name', 'source_location', 'recipe_notes']]
     .rename(columns={'name': 'Name', 'source_location': 'Source', 'recipe_notes': 'Notes'})
     .fillna(''))

print(tabulate(recipes_formatted, headers='keys', tablefmt='rounded_grid', showindex=False))
