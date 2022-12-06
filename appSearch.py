# appSearch.py
# ECE4574 FA22 Appointment Scheduler Nov. 28, 2022
# Sam Stewart, William Moore
# Search through appointments on a given day, returns the best order of appointments to go in
from itertools import permutations
import json as simplejson
import urllib.request

#Returns travel time in hours
def getTravelTime(origin_lat,origin_long,final_lat,final_long):
    origin = origin_lat,origin_long
    finaldest = final_lat,final_long
    api_key = 'AIzaSyC1-0yfh2ekEdBNcM1VVrxK4w-BtCAxEPM'#remove after testing
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false&key={2}".format(str(origin),str(finaldest),api_key)
    with urllib.request.urlopen(url) as opened:
        result= simplejson.load(opened)
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    return (float(driving_time)/float(360)) # returns hours  # Returns Value in seconds. for minutes divide driving_time by 60

#Searches database for appointment configurations in the business
def search(biz, window):
    allApps = []

    query = window.col.find({"apointee": "NONE"})

    for appointment in query:
        allApps.append([appointment["business"], float(appointment["start_time"]), float(appointment["end_time"]), str(appointment["_id"])])


    allLists = permutations(allApps)  # finds all possible combinations of appointments
    final_order = []
    for order in allLists:
        starttime = float(window.searchStartEntry.text())
        endtime = float(window.searchEndEntry.text())
        current_order = []
        for item in order:
            already_listed_business = False
            for listed_item in current_order:
                if item[0] == listed_item[0]:#if business in current item already in booked items
                    already_listed_business = True
            if item[0] in biz and item[1] >= starttime and item[2] <= endtime and not already_listed_business:
                current_order.append(item)
                starttime = item[2]

        #Below is the commented out travel time functionality
        #is commented out because we were approaching the free trial limit 

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
        #    if "NA" == end_long or "NA" == end_lat or "NA" == start_long or "NA" == start_lat:
        #        continue
        #    travel_time = getTravelTime(start_lat, start_long, end_lat, end_long)
        #    if travel_time > current_order[item_loc][2] - current_order[item_loc+1][1]:
        #        travel_time_possible = False
        #if not travel_time_possible:
        #    continue

        if len(current_order) > len(final_order) or len(current_order) == 0:#checks if current order has more appointments than 'best' order
            final_order = current_order
            continue
        if (len(current_order) == len(final_order)) and (current_order[-1][2] - current_order[0][1] < final_order[-1][2] - final_order[0][1]):#checks if current order takes less time than 'best' order
            final_order = current_order
        
    return final_order
                


