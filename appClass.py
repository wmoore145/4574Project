
class AppointmentSlot:
    def __init__(self, starttime, endtime, book=False,n = None):
        self.start = starttime
        self.end = endtime
        self.booked = book
        self.name = n

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


