""" Recipe API """

from flask import request, Response, Blueprint
import json
from database import recipes_collection
from helpers import fix_id, find_str_in_title, find_ingerdient_in_ingredients, fix_ingredients


recipes = Blueprint('recipes',
                  __name__,
                  url_prefix='/api/recipes'
                  )

@recipes.route('/all', methods=['GET'])
def get_all_recipes():
    
    all_recipes = [fix_id(recipe) for recipe in recipes_collection.find({"public": True})]
    if all_recipes:
        res = all_recipes
        status = 200
    else:
        res = {"message": "No recipes found"}
        status = 400
        
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    
    return response

@recipes.route('/add', methods=['POST'])
def add_recipe():
    data = request.json
    title = data.get('title', None)
    category = data.get('category', None)
    servings = data.get('servings', None)
    ingredients = data.get('ingredients', None)
    instructions = data.get('instructions', None)
    username = data.get('username', None)
    
    if not title or not category or not servings or not ingredients or not instructions or not username:
        res = {"message": "Missing credential"}
        status = 400
    else:
        id_num = recipes_collection.count_documents({})
        recipe = {
            "title": title,
            "ingredients": ingredients,
            "servings": servings,
            "instructions": instructions,
            "id": id_num,
            "added_favorite": [],
            "category": category,
            "creator": username,
            "public": True
            }
        insert_recipe = recipes_collection.insert_one(recipe)
        if insert_recipe.acknowledged:
            res = {"message": "Recipe created"}
            status = 200
        else:
            res = {"message": "Failed to create"}
            status = 200
            
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    return response


@recipes.route('/', methods=['GET'], strict_slashes=False)
def get_recipes():
    title = request.args.get('title', None)
    ingredients = request.args.get('ingredients', None)
    category = request.args.get('category', None)
    username = request.json.get('username', None)
    all_recipies = [fix_id(recipe) for recipe in recipes_collection.find({"public": True})]
    
    if category and title:
        recipe_cat = [fix_id(recipe) for recipe in recipes_collection.find({"category": category, "public": True })]
        res = find_str_in_title(recipe_cat, title.lower())
        status = 200
    elif category and ingredients:
        recipe_cat = [fix_id(recipe) for recipe in recipes_collection.find({"category": category, "public": True })]
        res = find_ingerdient_in_ingredients(recipe_cat, ingredients)
        status = 200
    elif username:
        res = [fix_id(recipe) for recipe in recipes_collection.find({"creator": username })]
        status = 200
    elif category:
        res = [fix_id(recipe) for recipe in recipes_collection.find({"category": category, "public": True })]
        status = 200
    elif title:
        res = find_str_in_title(all_recipies, title.lower())
        status = 200
    elif ingredients:
        res = find_ingerdient_in_ingredients(all_recipies, ingredients)
        status = 200
    else:
        res = {"message": "No recipes found"}
        status = 400
        
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    return response

@recipes.route('/<int:id_num>', methods=['GET'])
def get_recipe_by_id(id_num):
    recipe = recipes_collection.find_one({'id': id_num, "public": True})
    
    if recipe:
        res = fix_id(recipe)
        status = 200
    else:
        res = {"message": "No recipe found"}
        status = 400
    
    response = Response(
        response = json.dumps(res),
        status = status,
        mimetype="application/json"
        )
    
    return response

@recipes.route('/add-favorite/<int:id_num>', methods=['POST'])
def add_recipe_in_favorite(id_num):
    data = request.json
    username = data.get('username', None)
    
    if not username :
        res = {"message": "Missing user"}
        status = 400
    else:
        update_recipe = recipes_collection.update_one(
            {"id": id_num, "public": True},
            {"$addToSet": {"added_favorite": username}}
            )
        
        if update_recipe.matched_count == 0:
            res = {"message": "No recipe found"}
            status = 400
        elif update_recipe.modified_count == 0:
            res = {"message": "Already favorite"}
            status = 200
        else:
            res = {"message": "Favorite added"}
            status = 400
            
    response = Response(
        response = json.dumps(res),
        status = status,
        mimetype = "application/json"
        )
    
    return response

@recipes.route("/favorites", methods=['GET'])
def get_favorites_by_user():
    data = request.json
    username = data.get('username', None)
    
    if not username:
        res = {"message": "Missing user"}
        status = 400
    else:
        recipes = recipes_collection.find({'added_favorite': username})
        if recipes:
            res = [fix_id(recipe) for recipe in recipes]
            status = 200
        else:
            res = {"message": "No favorite recipes found"}
            status = 400
    
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    return response

@recipes.route("/rm-favorite/<int:id_num>", methods=['POST'])
def remove_from_favorites(id_num):
    data = request.json
    username = data.get('username', None)
    
    if not username :
        res = {"message": "Missing user"}
        status = 400
    else:
        update_recipe = recipes_collection.update_one(
            {"id": id_num},
            {"$pull": {"added_favorite": username}}
            )
        
        if update_recipe.matched_count == 0:
            res = {"message": "No recipe found"}
            status = 400
        elif update_recipe.modified_count == 0:
            res = {"message": "Not a favorite"}
            status = 200
        else:
            res = {"message": "favorite removed"}
            status = 400
            
    response = Response(
        response = json.dumps(res),
        status = status,
        mimetype = "application/json"
        )
    
    return response
    
    
