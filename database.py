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

