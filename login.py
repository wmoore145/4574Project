from pymongo import MongoClient

def login(username, password):
    mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
    col = mongo_client["appointment_user_data"]["user_data"]#database user_data and collection user_data
    query = col.find_one({"username": username, "password": password})
    if query is None:
        return False
    return True


def register(username, password, type):
    mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
    col = mongo_client["appointment_user_data"]["user_data"]#database user_data and collection user_data
    query = col.find_one({"username": username})
    if query is not None:
        return False #username already taken
    col.insert_one({"username": username, "password": password, "type": type})
    return True
    
