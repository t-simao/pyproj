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
    
    all_recipes = [fix_id(recipe) for recipe in recipes_collection.find({})]
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

@recipes.route('/', methods=['GET'], strict_slashes=False)
def get_recipes():
    title = request.args.get('title', None)
    ingredients = request.args.get('ingredients', None)
    all_recipies = [fix_id(recipe) for recipe in recipes_collection.find({})]

    if title:
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

    recipe = recipes_collection.find_one({'id': id_num})
    
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
            {"id": id_num},
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
    
    
