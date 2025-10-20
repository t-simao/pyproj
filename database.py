from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from test import file



def get_collection():
    uri = file()
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        print(client.admin.command('ping'))
        db = client["App"]
        users = db["Users"]
        return users
    except Exception as e:
        print(e)
    
# users = get_collection()
