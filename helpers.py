def file(file):
    f = open(file)
    
    return f.read()

def fix_ingredients(ingredients):
    ingredients = ingredients.translate(str.maketrans({
        ',': ' ', '*': ' ', ':': ' ', ';': ' ', '\\': ' ', '/': ' ', '|': ' ', '(': ' ', ')': ' '
        }))
    return ingredients.split()


def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def str_to_list(string):
    li = []
    for word in string:
        li.append(word.lower())
        
    return li

def find_str_in_title(all_recipes, string):
    
    recipes = [recipe for recipe in all_recipes if string in recipe['title'].lower()]
    
    return recipes

def find_ingerdient_in_ingredients(all_recipes, ingredients_string):
    
    list_ingredients = [x.strip().lower() for x in fix_ingredients(ingredients_string)]
    set_ingredients = set(list_ingredients)
    recipes = []
    
    for recipe in all_recipes:
        
        rec_string =  " ".join(recipe['ingredients']).lower()
        recipe_ingredients = fix_ingredients(rec_string)
        set_recipe_ingredients = set(recipe_ingredients)
        
        if set_ingredients.issubset(set_recipe_ingredients):
            recipes.append(recipe)
    
    return recipes
