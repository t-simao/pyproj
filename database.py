from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from helpers import file

uri = file('db.txt')
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    print(client.admin.command('ping'))
    db = client["App"]
    users_collection = db['Users']
    recipes_collection = db["Recipe"]
except Exception as e:
    print(e)

def update():
    update = recipes_collection.update_many({}, {"$set": {"added_favorite": []}})
    
    print(update.modified_count, "Documents update.")
    
# update()