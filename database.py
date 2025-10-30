import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from helpers import file

uri = os.environ.get("MONGODB_URI")
if not uri:
    uri = file('db.txt')
    

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    print(client.admin.command('ping'))
    db = client["App"]
    users_collection = db['Users']
    recipes_collection = db["Recipe"]
except Exception as e:
    print(e)
    
    users_collection = None
    recipes_collection = None

# print(recipes_collection.count_documents({}))
def update():
    update = recipes_collection.update_many(
        {},
        {"$set": {"public": True}}
        )
    
    print(update.modified_count, "Documents update.")
    
update()