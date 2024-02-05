'''

Author : yunanhou

Date : 2023/08/24

Function : This file defines the satellite class satellite, which is the base class for all satellites in this project.
           Determining the satellite's position in orbit requires parameters such as longitude, latitude, distance from
           the earth's surface, true periapsis angle, etc.

'''

class satellite:
    def __init__(self , nu , orbit , true_satellite):
        # longitude (degree), because the satellite is constantly moving, there are many longitudes. Use the list type
        # to store all the longitudes of the satellite.
        self.longitude = []
        # latitude (degree), because the satellite is constantly moving, there are many latitudes. Use the list type
        # to store all the latitudes of the satellite.
        self.latitude = []
        # altitude (km), because the altitude is constantly moving, there are many altitudes. Use the list type
        # to store all the altitudes of the satellite.
        self.altitude = []
        # the current orbit of the satellite
        self.orbit = orbit
        # list type attribute, which stores the current satellite and which satellites have established ISL, stores
        # the ISL object
        self.ISL = []
        # True periapsis angle is a parameter that describes the position of an object in orbit. It represents the
        # angle of the object's position in orbit relative to the perigee. For different times, the value of the true
        # periapsis angle keeps changing as the object moves in its orbit.
        self.nu = nu
        # the id number of the satellite, which is the number of the satellite in the shell where it is located. If the
        # constellation has multiple shells, the id of each satellite is the number of the shell in which it is located.
        # Each shell is numbered starting from 1. The ID number is initially -1, and the user does not need to specify
        # it manually.
        self.id = -1
        # real satellite object created with sgp4 and skyfield models
        self.true_satellite = true_satellite
