import math  # Use math library to access math modules that we need to calculate nutritional info
import requests

app_id = "9b205e26"
app_key = "39cb576341b00bcc867f9ebb96a860be"


def print_list(choices_dict):
    for key, value in choices_dict.items():
        print(f'{key}){value}')


def meal_plan():
    mealType_choice = {1: "breakfast", 2: "lunch", 3: "dinner", 4: "snack", 5: "any"}
    print_list(mealType_choice)
    ask_mealType_no = (input(f"Enter a number for meal type: "))
    mealType1 = mealType_choice[int(ask_mealType_no)]
    return mealType1


def diet_plan():
    dietlabels_choice = {1: "kosher", 2: "vegetarian", 3: "vegan", 4: "gluten-free", 5: "dairy-free", 6: "pescatarian",7: "Mediterranean"}
    print_list(dietlabels_choice)
    ask_dietlabels_no = input("Enter a number for diet label: ")
    dietlabels1 = dietlabels_choice[int(ask_dietlabels_no)]
    return dietlabels1


def recipe_search():
    user_choice = input('Enter 1 OR 2 ingredients separated by a comma: ')
    ingredients = user_choice.split(" ", )
    while True:
        mealtypelist_one = ["breakfast", "lunch", "dinner", "snack"]
        mealType = meal_plan()
        if mealType in mealtypelist_one:
            diet = input("Do you follow a specific diet?: yes / no ")
            diet_options = "yes"
            diet_options2 = "no"
            if diet in diet_options:
                dietlabels = diet_plan()
                results = requests.get(
                    f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients}&app_id={app_id}&app_key={app_key}&health={dietlabels}&mealType={mealType}")
                data = results.json()
                return data['hits']
            elif diet in diet_options2:
                results = requests.get(
                    f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients}&app_id={app_id}&app_key={app_key}&mealType={mealType}")
                data = results.json()
                return data['hits']
        else:
            diet = input("Do you follow a specific diet?: yes / no ")
            diet_options = "yes"
            diet_options2 = "no"
            if diet in diet_options:
                dietlabels = diet_plan()
                results = requests.get(
                    f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients}&app_id={app_id}&app_key={app_key}&health={dietlabels}")
                data = results.json()
                return data['hits']
            elif diet in diet_options2:
                results = requests.get(
                    f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredients}&app_id={app_id}&app_key={app_key}")
                data = results.json()
                return data['hits']


def run():
    results = recipe_search()
    for result in results:  # retrieve url, ingredients, no/ of servings, nutrition & label for every object in hits

        recipe_info = result["recipe"]
        recipe_name = recipe_info["label"].title()
        recipe_link = recipe_info["url"]
        recipe_ingredients = recipe_info["ingredientLines"]
        recipe_yield = recipe_info["yield"]
        calories_yield = str(math.ceil((recipe_info["calories"]) / recipe_yield))  # calories per yield
        recipe_fat = recipe_info["totalNutrients"]["FAT"]  # retrieve&store nutritional info per recipe as dict
        recipe_protein = recipe_info["totalNutrients"]["PROCNT"]  # code for protein
        recipe_carbohydrates = recipe_info["totalNutrients"]["CHOCDF"]  # nutritional code for carbs
        recipe = result['recipe']
        list(range(10))
        # 1st print recipes + info. limit to 10 recipes
        print("\n")
        print(recipe['label'])
        print("\nThis recipe is suitable for: {}".format(recipe['healthLabels']))
        print("It contains {} calories.".format(int(recipe['calories'])))
        print(recipe['url'])
        print("Ingredients: \n{}".format(recipe['ingredientLines']) + '\n')

        # then write recipe and some nutritional infor to text file
        recipe_file = open('recipe_info.txt', "a")
        recipe_file.write(recipe_name.upper() + "\n")
        recipe_file.write(recipe_link + "\n")
        recipe_file.write("Ingredients:" + "\n")

        for elements in recipe_ingredients:
            recipe_file.write(elements + "\n")
        recipe_file.write("\n")
        recipe_file.write("Nutritional Information:" + "\n")
        recipe_file.write("Number of servings: " + str(int(recipe_yield)) + "\n")
        recipe_file.write("Calories per serving: " + calories_yield + "\n")
        recipe_file.write('')

        # used math.ceil() method to round values up to the nearest integer, figured floats may confuse our 'dumb' user
        recipe_file.write(recipe_fat["label"] + " per serving: " + str(
            math.ceil((recipe_fat["quantity"]) / (result["recipe"]["yield"]))) + recipe_fat["unit"] + "\n")
        recipe_file.write(recipe_carbohydrates["label"] + " per serving: " + str(
            math.ceil((recipe_carbohydrates["quantity"]) / (result["recipe"]["yield"]))) + recipe_carbohydrates["unit"] + "\n")
        recipe_file.write(recipe_protein["label"] + " per serving: " + str(
            math.ceil((recipe_protein["quantity"]) / (result["recipe"]["yield"]))) + recipe_protein["unit"] + "\n" * 4)

        recipe_file.close()  # file will close and not get affected by lines below

    # finally ask user if they would like to search for another ingredient, if yes the prog prints, writes & asks again.
    search_again = input('\nWould you like to find recipes for another ingredient? yes/no\n').lower()
    if search_again.lower() == 'yes':
        run()
    elif search_again.lower() == 'no':  # if no prog exits with a thank-you note
        print('\n the recipes above have been saved to a downloadable file. \n''We have included some nutritional information too! ')
        print('Thanks for visiting Coffee&Class!')
        exit()


# HOW TO ORDER RESULTS BY COOKING TIME

print('Welcome to Coffee&Class Recipe Search Engine \n''We will choose some recipes based on an ingredient of your choice\n''and your dietary needs')
open("recipe_info.txt", 'w').close()

run()