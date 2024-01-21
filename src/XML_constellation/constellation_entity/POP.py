'''

Author : yunanhou

Date : 2023/11/07

Function : This file defines the POP point class. The POP point is an entrance and exit that must be passed through
           before the satellite transmits the signal to the ground station GS before accessing the ground Internet.

'''

class POP:
    def __init__(self , longitude, latitude , POP_name=None):
        self.POP_name = POP_name # the name of POP
        self.longitude = longitude # the longitude of POP
        self.latitude = latitude # the latitude of POP

