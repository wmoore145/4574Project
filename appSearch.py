# Search through appointments on a given day
# return the best order of appointments to go in
from itertools import permutations
from collections import OrderedDict
import json as simplejson
import urllib
from bson.objectid import ObjectId

def getTravelTime(origin_lat,origin_long,final_lat,final_long):
    origin = origin_lat,origin_long
    finaldest = final_lat,final_long
    api_key = 'AIzaSyC1-0yfh2ekEdBNcM1VVrxK4w-BtCAxEPM'#remove after testing
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false&key={2}".format(str(origin),str(finaldest),api_key)
    result= simplejson.load(urllib.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    return driving_time # returns  # hours # min or #min

# search function given all the appointments, the buisneses needed, the start time, and current route
# this is based off an AI Project I did
# I realised after I was mostly done It can be simplified much more
# I will simplify it later down the road when we are sure this is what we want
# Originaly I was using a breadth first search but since there wont be that many appoinments
# Exhaustive seaching through every possibility is viable
'''def nextApt(allApps, needed, starttime, route):
    print("called")
    print(starttime)
    newRoute = route
    queue = []
    for biz in needed:
        if biz not in route.keys():
            queue.append(biz)

    while len(queue) != 0:

        currentBiz = queue.pop(0)

        for app in allApps.get(currentBiz):
            print("failed?")
            print(starttime)
            if (app[1] >= starttime):
                print("here: ")
                print(app[1])
                print(app[2])
                print(starttime)
                newRoute[currentBiz] = [app[1], app[0]]
                nextApt(allApps, needed, app[2], newRoute)
                break
        print("broke?")
        print(starttime)
        if (len(route) == len(needed)):
            return route'''
        

def search(biz, window):
    print("Entered succesful")
    route = OrderedDict() #using an ordered dictionary for the route
    best_route = OrderedDict() # best route to take
    bestEnd = 10000     #high best end time so it only gets smaller, should be after appointmets stop
    allApps = []
    #allApps = {}

    query = window.col.find({"apointee": "NONE"})

    
    for appointment in query:
        allApps.append([appointment["business"], float(appointment["start_time"]), float(appointment["end_time"]), str(appointment["_id"])])
        #if appointment["business"] not in allApps.keys():
        #    allApps[appointment["business"]] = []
        #allApps[appointment["business"]].append([str(appointment["_id"]), int(appointment["start_time"]), int(appointment["end_time"])])

    
    
    allLists = permutations(allApps)  # finds all possible combinations of appointments
    final_order = []
    for order in allLists:
        starttime = float(window.searchStartEntry.text())
        endtime = float(window.searchEndEntry.text())
        current_order = []
        for item in order:
            if item[0] in biz and item[1] >= starttime and item[2] <= endtime and item not in current_order:
                current_order.append(item)
                starttime = item[2]

        #travel_time_possible = True
        #for item_loc in range(len(current_order)):
        #    if item_loc + 1 >= len(current_order):
        #        break
        #    business_coords_query =  window.mongo_client["appointment_user_data"]["user_data"].find_one({"username": current_order[item_loc][0]})#finds business item
        #    end_long = business_coords_query["long"]
        #    end_lat = business_coords_query["lat"]
        #    private_coords_query =  window.mongo_client["appointment_user_data"]["user_data"].find_one({"username": window.client.username_text})#finds user item
        #    start_long = private_coords_query["long"]
        #    start_lat = private_coords_query["lat"]
        #    travel_time = getTravelTime(start_lat, start_long, end_lat, end_long)
        #    if travel_time > current_order[item_loc][2] - current_order[item_loc+1][1]:
        #        travel_time_possible = False
        #if not travel_time_possible:
        #    continue

        if len(current_order) > len(final_order) or len(current_order) == 0:
            final_order = current_order
            continue
        if current_order[-1][2] - current_order[0][1] < final_order[-1][2] - final_order[0][1]:
            final_order = current_order
        
    #print(final_order)
    return final_order
                
    #allLists = permutations(biz)  # finds all possible combinations of appointment orders
    #for order in list(allLists):
    #    nextApt(allApps, order, 0, route)
    #    endtime = list(route.values())[-1]
    #    if(endtime[0] < bestEnd):
    #        best_route = route
    #        bestEnd = endtime[0]



    #print(best_route)

    #converts the ordered dictionary to a string
    #return best_route


