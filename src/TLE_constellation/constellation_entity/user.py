'''

Author: yunanhou

Date : 2023/12/14

Function : This file defines the user terminal class, the source endpoint and destination endpoint that need to be
           specified in communication, and these endpoints are the instantiation objects of this class. User terminals
           are all located on the surface of the earth, and the longitude and latitude must be passed in when
           instantiating this class.

'''

class user:
    def __init__(self, longitude, latitude, user_name=None):
        self.user_name = user_name  # the name of user
        self.longitude = longitude  # the longitude of user
        self.latitude = latitude  # the latitude of user