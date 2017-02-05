#edited 20:32
        

class Intercom(object):
    
    def __init__(self, tag, location):
        self.tag = tag
        self.location = location


class Location(object):

    def __init__(self, floor, wing, room):
        self.__floor = floor
        self.__wing = wing
        self.__room = room

    def change_floor(self, new_floor):
        self.__floor = new_floor
    
    def change_wing(self, new_wing):
        self.__floor = new_wing

    def change_room(self, new_room):
        self.__floor = new_room

    def get_floor(self):
        return self.__floor

    def get_room(self):
        return self.__room

    def get_wing(self):
        return self.__wing
    




        
##function to call. Takes: "You should go " + result
def parse_intent(intention, intercom):
    intent = intention.lower().replace('_',' ')
    
    if intent == "eating":
        return "starve."

    elif intent == "studying":
        return nearest_library(intercom)

    else:
        return "nowhere."
    


def nearest_library(intercom):
    if intercom.location.get_floor() == 1:
        return "to near room A123."
    else:
        return "nowhere since there are no other floors for now."

def nearest_cafeteria(intercom):

##def nearest_bathroom(intercom):
##    if intercom.get_floor() == "1"
##        return "to near room A123."
