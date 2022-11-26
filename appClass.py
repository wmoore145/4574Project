import simplejson, urllib



class AppointmentSlot:
    def __init__(self, starttime, endtime, book=False,n = None, origin_lat = None, origin_long = None, final_lat = None, final_long = None):
        self.start = starttime
        self.end = endtime
        self.booked = book
        self.name = n
        self.origin = origin_lat,origin_long
        self.finaldest = final_lat,final_long

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end 
    
    def is_booked(self):
        return self.booked

    def get_name(self):
        return self.name
    
    def set_name(self, n):
        self.name = n

    #for canceling appointment
    def set_booked(self, b):
        self.booked = b
        
    def set_origin(origin_lat, origin_long):
        self.origin = origin_lat,origin_long
    
    def set_finalDestination(final_lat, final_long):
        self.finaldest = final_lat,final_long
    
    def get_travel_time():
        url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(self.origin),str(self.finaldest))
        result= simplejson.load(urllib.urlopen(url))
        driving_time = result['rows'][0]['elements'][0]['duration']['value']
        print(driving_time)


class CSlot(AppointmentSlot):
        pass

class BSlot(AppointmentSlot):
    def __init__(self, starttime, endtime, book=False,n = None, businessid = None):
        self.start = starttime
        self.end = endtime
        self.booked = book
        self.name = n
        self.bid = businessid
   
    def set_bid(self,id):
        self.bid = id

    def get_bid(self):
        return self.bid


