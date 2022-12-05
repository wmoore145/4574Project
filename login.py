# login.py ECE4574 FA22 Appointment Scheduler Sam Stewart Nov. 28, 2022
# This handles login details/registration database communications
from pymongo import MongoClient
import json as simplejson
import urllib.request

#For distance calculations, takes address and returns coordinates in a list
def addr_to_coords(address):
    addr = address.replace(" ","%20")
    api_key = 'AIzaSyC1-0yfh2ekEdBNcM1VVrxK4w-BtCAxEPM'#remove after testing
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(addr,api_key)
    with urllib.request.urlopen(url) as opened:
        result= simplejson.load(opened)
    print(result)
    lat = result['results'][2]['location']['lat']
    lng = result['results'][2]['location']['lng']
    return [lat, lng] # returns lattitude and longitude

#Returns True if login is valid, and False if not
def login(username, password):
    mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
    col = mongo_client["appointment_user_data"]["user_data"]#database user_data and collection user_data
    query = col.find_one({"username": username, "password": password})
    if query is None:
        return False
    return True

#Returns True if registration happened, and False if not
def register(username, password, type, address):
    mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
    col = mongo_client["appointment_user_data"]["user_data"]#database user_data and collection user_data
    #if(address != 0):
    #    coords = addr_to_coords(address)
    query = col.find_one({"username": username})
    if query is not None:
        return False #username already taken
    #if(len(coords) != 2):
    #    col.insert_one({"username": username, "password": password, "type": type, "lat": "NA", "long": "NA"})
    #else:
    col.insert_one({"username": username, "password": password, "type": type, "lat": str(coords[0]), "long": str(coords[1])})
    return True
    
#Returns True if username is a business, and False if not
def isBusiness(username):
    mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
    col = mongo_client["appointment_user_data"]["user_data"]#database user_data and collection user_data
    query = col.find_one({"username": username, "type": "business"})
    if query is None:
        return False
    return True