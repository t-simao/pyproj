""" User API """

from flask import request, Response, Blueprint
import json
from database import users_collection
from helpers import fix_id


users = Blueprint('users',
                  __name__,
                  url_prefix='/api/users'
                  )


@users.route('/all', methods=['GET'])
def get_users():
    
    all_users = users_collection.find({})
    response = Response(
        response=json.dumps([fix_id(user) for user in all_users]),
        status=200,
        mimetype="application/json"
        )
    
    return response

@users.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.json
    username = data.get('username', None)
    password = data.get('password', None)
    
    user = users_collection.find_one({"username": username})
    if user:
        res = {"message": "User already exists"}
        status = 400
    else:
        user = users_collection.insert_one({"username": username, "password": password})
        res = {"message": "User registered"}
        status = 200
        
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    return response

@users.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.json
    username = data.get('username', None)
    password = data.get('password', None)
    
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        res = fix_id(user)
        status = 200
    else:
        res = {"message": "Wrong username/password, try again!"}
        status = 400
    
    response = Response(
        response=json.dumps(res),
        status=status,
        mimetype="application/json"
        )
    return response
