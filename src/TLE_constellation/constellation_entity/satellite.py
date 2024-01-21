'''

Author : yunanhou

Date : 2023/12/01

Function : This file defines the satellite class for Constellation

'''


class satellite:
    def __init__(self , tle_json , tle_2le):
        # TLE in json format. This property is a dict object that holds various fields in JSON format
        self.tle_json = tle_json
        # TLE in 2le format. This property is a tuple object that contains two elements, each of which is a string
        # representing tle data in 2le format
        self.tle_2le = tle_2le
        # cospar_id of current satellite
        self.cospar_id = self.tle_json["OBJECT_ID"][:8]
        # shell class variables are used to represent the shell to which the current satellite belongs
        self.shell = None
        # orbit class variables are used to represent the orbit to which the current satellite belongs
        self.orbit = None
        # longitude (degree), because the satellite is constantly moving, there are many longitudes. Use the list type
        # to store all the longitudes of the satellite.
        self.longitude = []
        # latitude (degree), because the satellite is constantly moving, there are many latitudes. Use the list type
        # to store all the latitudes of the satellite.
        self.latitude = []
        # altitude (km), because the altitude is constantly moving, there are many altitudes. Use the list type
        # to store all the altitudes of the satellite.
        self.altitude = []
        # list type attribute, which stores the current satellite and which satellites have established ISL, stores
        # the ISL object
        self.ISL = []
        # the id number of the satellite
        self.id = -1