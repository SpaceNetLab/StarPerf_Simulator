'''

Author : yunanhou

Date : 2023/11/08

Function : Calculate the communication bandwidth between two ground users in bent-pipe mode

Implementation method: When the bent-pipe mode communicates between two ends (denoted as end A and end B), end A selects
                       a satellite in the sky as a relay (denoted as satellite 1) according to a certain strategy, and
                       end B selects a satellite in the sky as a relay according to a certain strategy. The strategy
                       selects a satellite in the sky as the relay (denoted as satellite 2). Assume that there are n
                       GSs within the visible range of satellite 1, and the bandwidth of each GS is P; there are m GSs
                       within the visible range of satellite 2, and the bandwidth of each GS is for P. Therefore, the
                       bandwidth of satellite 1 → satellite 2 can be expressed as n*P, and the bandwidth of satellite 2
                       → satellite 1 can be expressed as m*P.Since the communication is bidirectional, the communication
                       bandwidth between A and B is min{n*P,m*P}. The above calculation is performed for each timeslot
                       within the satellite orbit period. Finally, the average of all timeslot values can be used as the
                       bent-pipe bandwidth for communication between A and B.

'''
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt
import src.XML_constellation.constellation_entity.ground_station as GS
import xml.etree.ElementTree as ET

# Read xml document
def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

# Read xml document
def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: xml_to_dict(root)}


# Calculate the distance between the user and a satellite (the calculation result takes into account the curvature of
# the earth), the unit of the return value is kilometers
def distance_between_satellite_and_user(groundstation , satellite , t):
    longitude1 = groundstation.longitude
    latitude1 = groundstation.latitude
    longitude2 = satellite.longitude[t-1]
    latitude2 = satellite.latitude[t-1]
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2),
                                                              float(latitude2)]) # Convert latitude and longitude to radians
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371.0*1000 # the average radius of the earth is 6371km
    distance=np.round(distance/1000,3)  # convert the result to kilometers with three decimal places.
    return distance


# Function : convert the latitude and longitude coordinates of ground GS/POP points/user terminals/satellites into
#            three-dimensional Cartesian coordinates
# Parameters:
# transformed_object : the GS class object/satellite class object that needs to be converted
# object_type : the type of the parameter transformed_object. The type of object_type is a string. The value of the
#               string is "GS" or "satellite" or "POP" or "User".
# t : the timeslot number, starting from 1. Among them, when object_type is "GS", this parameter is invalid. When
#     object_type is "satellite", this parameter represents the tth timeslot of the satellite.
# Return value : the x, y, and z coordinates of the converted GS, and xyz are all in meters.
def latilong_to_descartes(transformed_object , object_type , t=None):
    a = 6371000.0
    e2 = 0.00669438002290
    if object_type == "satellite":
        longitude = math.radians(transformed_object.longitude[t - 1])
        latitude = math.radians(transformed_object.latitude[t - 1])
        fac1 = 1 - e2 * math.sin(latitude) * math.sin(latitude)
        N = a / math.sqrt(fac1)
        # the unit of satellite height above the ground is meters
        h = transformed_object.altitude[t - 1] * 1000
        X = (N + h) * math.cos(latitude) * math.cos(longitude)
        Y = (N + h) * math.cos(latitude) * math.sin(longitude)
        Z = (N * (1 - e2) + h) * math.sin(latitude)
        return X, Y, Z
    else:
        longitude = math.radians(transformed_object.longitude)
        latitude = math.radians(transformed_object.latitude)
        fac1 = 1 - e2 * math.sin(latitude) * math.sin(latitude)
        N = a / math.sqrt(fac1)
        h = 0  # GS height from the ground, unit is meters
        X = (N + h) * math.cos(latitude) * math.cos(longitude)
        Y = (N + h) * math.cos(latitude) * math.sin(longitude)
        Z = (N * (1 - e2) + h) * math.sin(latitude)
        return X, Y, Z



# Function : given a point on land (user, POP or GS, etc.) and the coordinates of a satellite in the three-dimensional
#            Cartesian system, determine whether the point on land can see the satellite.
# Parameters:
# sat_x, sat_y, sat_z : respectively represent the xyz coordinates of the satellite in the three-dimensional Cartesian
#                       coordinate system
# point_x, point_y, point_z : respectively represent the xyz coordinates of points on land in the three-dimensional
#                             Cartesian coordinate system
# minimum_elevation : the minimum elevation angle at which a point on land can see the satellite
# Return value : Returning True means it can be seen, False means it can't be seen.
# Basic idea: Calculate the vector from the ground point to the satellite and the vector from the ground point to the
#             center of the earth respectively, and then calculate the angle between the two vectors. If the angle is
#             greater than or equal to (90°+minimum_elevation), it means it is visible, otherwise it means it is
#             invisible.
def judgePointToSatellite(sat_x , sat_y , sat_z , point_x , point_y , point_z , minimum_elevation):
    A = 1.0 * point_x * (point_x - sat_x) + point_y * (point_y - sat_y) + point_z * (point_z - sat_z)
    B = 1.0 * math.sqrt(point_x * point_x + point_y * point_y + point_z * point_z)
    C = 1.0 * math.sqrt(math.pow(sat_x - point_x, 2) + math.pow(sat_y - point_y, 2) + math.pow(sat_z - point_z, 2))
    angle = math.degrees(math.acos(A / (B * C))) # find angles and convert radians to degrees
    if angle < 90 + minimum_elevation or math.fabs(angle - 90 - minimum_elevation) <= 1e-6:
        return False
    else:
        return True




# Strategy 1 for users to choose which satellite above their heads to connect to: users always connect to the satellite
# closest to them
def user_connect_satelite_policy1(source , target , sh , t):
    # find the satellites closest to the source and target
    # the satellite closest to the source ground station
    nearest_satellite_to_source = None
    # initialize the nearest distance to the source base station to be infinite
    satellite_to_source_distance = float('inf')
    # the satellite closest to the target ground station
    nearest_satellite_to_target = None
    # initialize the nearest distance to the target base station to be infinite
    satellite_to_target_distance = float('inf')
    # traverse each satellite in the sh layer shell
    for orbit in sh.orbits:
        for satellite in orbit.satellites:
            # calculate the distance between the currently traversed satellite and the source
            dis1 = distance_between_satellite_and_user(source, satellite, t)
            # calculate the distance between the currently traversed satellite and the target
            dis2 = distance_between_satellite_and_user(target, satellite, t)
            if dis1 < satellite_to_source_distance:
                satellite_to_source_distance = dis1
                nearest_satellite_to_source = satellite
            if dis2 < satellite_to_target_distance:
                satellite_to_target_distance = dis2
                nearest_satellite_to_target = satellite
    # after the above for loop ends, the variable nearest_satellite_to_source represents the satellite closest to the
    # source, and the variable nearest_satellite_to_target represents the satellite closest to the target.
    return nearest_satellite_to_source , nearest_satellite_to_target



# Function : find all GSs within visible range of a satellite
# Parameters:
# minimum_elevation : the minimum elevation angle of the ground observation point, and the parameter unit is degrees (°)
# Return value : a list object, each element of which is a ground_station class object. Of course, if there is no GS
#                within the visible range of the current satellite, this function will return an empty list.
def satellite_visible_all_GSs(satellite , GSs , t , minimum_elevation):
    # convert the longitude, latitude, and altitude coordinates of the satellite satellite at time t into
    # three-dimensional Cartesian coordinates
    sat_x,sat_y,sat_z = latilong_to_descartes(satellite , "satellite" , t)
    all_visible_GSs = []
    for gs in GSs:
        # convert the latitude and longitude coordinates of the ground station gs into
        # three-dimensional Cartesian coordinates
        gs_x,gs_y,gs_z = latilong_to_descartes(gs , "GS")
        # determine whether the satellite satellite and the ground station gs are visible at time t.
        # If visible, add the current gs to all_visible_GSs.
        if judgePointToSatellite(sat_x , sat_y , sat_z , gs_x , gs_y , gs_z , minimum_elevation):
            all_visible_GSs.append(gs)
    return all_visible_GSs





# Function : calculate the bandwidth between two communication endpoints in bent-pipe mode
# Parameters:
# source is the source of communication, and target is the destination of communication. Both parameters
# are user class objects.
# dT : how often to record a timeslot
# sh : a shell class object, representing a shell in the constellation
# ground_station_file: the data file of the satellite constellation ground base station GS (given in
#                      the form of path + file name)
# minimum_elevation is the minimum
# elevation angle of the ground observation point. The unit of this parameter is degrees (°).
# GS_capacity : the GS capacity of each ground station, such as 10 Gbps, etc.
def bandwidth(source , target , dT , sh , ground_station_file , minimum_elevation = 25 , GS_capacity = 5.0):
    # read ground base station data
    ground_station = read_xml_file(ground_station_file)
    # generate GS
    GSs = []
    for gs_count in range(1 , len(ground_station['GSs'])+1 , 1):
        gs = GS.ground_station(longitude = float(ground_station['GSs']['GS'+str(gs_count)]['Longitude']) ,
                               latitude = float(ground_station['GSs']['GS'+str(gs_count)]['Latitude']) ,
                               description = ground_station['GSs']['GS'+str(gs_count)]['Description'] ,
                               frequency = ground_station['GSs']['GS'+str(gs_count)]['Frequency'] ,
                               antenna_count = int(ground_station['GSs']['GS'+str(gs_count)]['Antenna_Count']) ,
                               uplink_GHz = float(ground_station['GSs']['GS'+str(gs_count)]['Uplink_Ghz']) ,
                               downlink_GHz = float(ground_station['GSs']['GS'+str(gs_count)]['Downlink_Ghz']))
        GSs.append(gs)
    # list type, used to store the bandwidth from source to target in bent-pipe mode in each timeslot
    bandwidth_per_timeslot = []
    for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
        # find the source satellite and target satellite
        satellite_to_source, satellite_to_target = user_connect_satelite_policy1(source, target, sh, t)
        # find all GS within visible range of satellite satellite_to_source
        all_sourcesatellite_visible_GSs = satellite_visible_all_GSs(satellite_to_source, GSs, t, minimum_elevation)
        # find all GS within visible range of satellite satellite_to_target
        all_targetsatellite_visible_GSs = satellite_visible_all_GSs(satellite_to_target, GSs, t, minimum_elevation)
        # calculate the current timeslot bandwidth
        bandwidth_current_timeslot = GS_capacity * min(len(all_sourcesatellite_visible_GSs) ,
                                                       len(all_targetsatellite_visible_GSs))

        bandwidth_per_timeslot.append(bandwidth_current_timeslot)

    # calculate average bandwidth
    avg_bandwidth = sum(bandwidth_per_timeslot) / len(bandwidth_per_timeslot)
    return avg_bandwidth