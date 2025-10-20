""" DB API """

from flask import Flask, request, session, Response
from flask_cors import CORS
import json
from database import get_collection


app = Flask(__name__)
CORS(app)

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route('/api')
def index():
    return 'HEJ HEJ'

@app.route('/api/users', methods=['GET'])
def get_users():
    
    users = get_collection()
    all_users = users.find({})
    response = Response(
        response=json.dumps([fix_id(user) for user in all_users]),
        status=200,
        mimetype="application/json"
        )
    
    return response

@app.route('/api/register/', methods=['GET', 'POST'])
def register():
    username = request.args.get('username', None)
    password = request.args.get('password', None)
    
    users = get_collection()
    find_user = users.find_one({"username": username})
    if find_user:
        res = ['User exists']
    else:
        user = users.insert_one({"username": username, "password": password})
        res = ['Users registered']
        
    response = Response(
        response=json.dumps(res),
        status=200,
        mimetype="application/json"
        )
    return response

@app.route('/api/login/', methods=['GET', 'POST'])
def login():
    username = request.args.get('username', None)
    password = request.args.get('password', None)
    
    users = get_collection()
    find_user = users.find_one({"username": username, "password": password})
    if find_user:
        res = ["user logged in"]
    else:
        res = ["Wrong username/password"]
    
    response = Response(
        response=json.dumps(res),
        status=200,
        mimetype="application/json"
        )
    return response


if __name__ == "__main__":
    app.run(debug=True)