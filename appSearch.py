# Search through appointments on a given day
# return the best order of appointments to go in
from itertools import permutations
from collections import OrderedDict
import json as simplejson
import urllib

def getTravelTime(origin_lat,origin_long,final_lat,final_long):
    origin = origin_lat,origin_long
    finaldest = final_lat,final_long
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(self.origin),str(self.finaldest))
    result= simplejson.load(urllib.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    return driving_time # returns  # hours # min or #min

def getBusiness():
    business_names = []
    #get the names of all the businesses 
    #just return a list of all the businesses names
    return business_names

def getApps():
    
    #gets the appointments from the server
    #return a dictionary of all the appointments
    #see setupApps for the format it should return
    return {}

def setupApps():    #test database
    Aapp1 = [1, 2, False]   # [start time, end time, booked] booked = false means its open 
    Aapp2 = [2, 3, False]
    Aapp3 = [3, 4, False]
    Aapp4 = [4, 5, False]
    Aapp5 = [5, 6, False]
    A = [Aapp1, Aapp2, Aapp3, Aapp4, Aapp5] #list of appointments

    Bapp1 = [1, 2, False] 
    Bapp2 = [2, 3, True]
    Bapp3 = [3, 4, False]
    Bapp4 = [4, 5, False]
    Bapp5 = [5, 6, False]
    B = [Bapp1, Bapp2, Bapp3, Bapp4, Bapp5]

    Capp1 = [1, 2, False] 
    Capp2 = [2, 3, False]
    Capp3 = [3, 4, False]
    Capp4 = [4, 5, False]
    Capp5 = [5, 6, False]
    C = [Capp1, Capp2, Capp3, Capp4, Capp5]
    allApps = { #dictionary with the key being the appointment name, and the value being the list of appointmetns
        "A" : A,
        "B" : B,
        "C" : C,
    }
    return allApps


# search function given all the appointments, the buisneses needed, the start time, and current route
# this is based off an AI Project I did
# I realised after I was mostly done It can be simplified much more
# I will simplify it later down the road when we are sure this is what we want
# Originaly I was using a breadth first search but since there wont be that many appoinments
# Exhaustive seaching through every possibility is viable
def nextApt(allApps, needed, starttime, route):
    newRoute = route
    queue = []
    for biz in needed:
        if biz not in route.keys():
            queue.append(biz)

    while len(queue) != 0:

        currentBiz = queue.pop(0)

        for app in allApps.get(currentBiz):
            if ((app[0] >= starttime) and (app[2] == False)):
                newRoute[currentBiz] = app[0]
                nextApt(allApps, needed, app[1], newRoute)
                break

        if (len(route) == len(needed)):
            return route
        




def search(biz, col):
    print("Entered succesful")
    route = OrderedDict() #using an ordered dictionary for the route
    best_route = OrderedDict() # best route to take
    bestEnd = 10000     #high best end time so it only gets smaller, should be after appointmets stop
    allApps = {}

    query = col.find({})
    for appointment in query:
        occupied = True
        if appointment["apointee"] == "NONE":
            occupied = False
        if appointment["business"] not in allApps.keys():
            allApps[appointment["business"]] = []
        allApps[appointment["business"]].append([int(appointment["start_time"]), int(appointment["end_time"]), occupied])

    endtime = 0 
    
    allLists = permutations(biz)  # finds all possible combinations of appointment orders
    for order in list(allLists):
        nextApt(allApps, order, 0, route)
        endtime = list(route.values())[-1]
        if(endtime < bestEnd):
            best_route = route
            bestEnd = endtime


        route = {}

    #converts the ordered dictionary to a string
    return best_route


