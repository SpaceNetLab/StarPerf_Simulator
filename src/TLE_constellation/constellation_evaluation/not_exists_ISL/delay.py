'''

Author: yunanhou

Date : 2023/12/16

Function : Calculate the communication delay between two ground users in bent-pipe mode


Implementation method: When the bent-pipe mode communicates between two terminals (denoted as terminal A and terminal
                       B), the process is: terminal A → satellite 1 → ground station A → POP point 1 → terminal B, or
                       terminal B → Satellite 2 → Ground station B → POP point 2 → Terminal A. Therefore, if you want
                       to calculate the delay between terminal A and terminal B in bent-pipe mode, you can calculate
                       the delay between terminal A → satellite 1 → ground station A → POP point 1 → POP point 2 →
                       ground station B → satellite 2 → terminal B , use this delay time to represent the bent-pipe
                       delay between terminal A and terminal B. Among them, when calculating the delay between POP
                       point 1 → POP point 2, it is expressed by dividing the great circle distance on the earth's
                       surface by a certain speed.

'''
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt
import numpy as np
import math
import src.TLE_constellation.constellation_entity.ground_station as GS
import src.TLE_constellation.constellation_entity.POP as POP_POINT


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



# Function : given the longitude and latitude of two points on the earth's surface, calculate the distance between the
#            two points (the calculation result takes into account the curvature of the earth, that is, the great circle
#            distance between the two points), and the unit of the return value is kilometers.
def distance_two_terrestrial_point(point1 , point2):
    longitude1 = point1.longitude
    latitude1 = point1.latitude
    longitude2 = point2.longitude
    latitude2 = point2.latitude
    # convert latitude and longitude to radians
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2),
                                                              float(latitude2)])
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371.0*1000 # the average radius of the earth is 6371km
    # convert the result to kilometers with three decimal places.
    distance=np.round(distance/1000,3)
    return distance



# Function : calculate the distance between the user and a satellite (the calculation result takes into account the
#            curvature of the earth), the unit of the return value is kilometers
def distance_between_satellite_and_user(groundstation , satellite , t):
    longitude1 = groundstation.longitude
    latitude1 = groundstation.latitude
    longitude2 = satellite.longitude[t-1]
    latitude2 = satellite.latitude[t-1]
    # convert latitude and longitude to radians
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1),
                                                              float(longitude2), float(latitude2)])
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371.0*1000 # the average radius of the earth is 6371km
    # convert the result to kilometers with three decimal places.
    distance=np.round(distance/1000,3)
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



# Function : Strategy 1 for users to choose which satellite above their heads to connect to: users always
#            connect to the satellite closest to them
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
    for satellite in sh.satellites:
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
    # after the above for loop ends, the variable nearest_satellite_to_source represents the satellite closest to
    # the source, and the variable nearest_satellite_to_target represents the satellite closest to the target
    return nearest_satellite_to_source , nearest_satellite_to_target



# Function : Strategy 1 for satellites in the sky to choose which ground station to establish a connection with: the
#            satellite forwards to the ground station closest to the user within its visible range
# Parameters:
# minimum_elevation : the minimum elevation angle of the ground observation point, and the parameter unit is degrees (°)
# Return value : a ground_station class object. Of course, if there is no GS within the current visible range of the
#                satellite, this function will return None.
def satellite_connect_groundstation_policy1(user , satellite , GSs , t , minimum_elevation):
    # convert the longitude, latitude, and altitude coordinates of the satellite satellite at time t into
    # three-dimensional Cartesian coordinates
    sat_x,sat_y,sat_z = latilong_to_descartes(satellite , "satellite" , t)
    # traverse GSs and find a GS closest to the user among the ground stations visible to the satellite.
    nearest_GS_to_user = None # the base station closest to the user
    GS_to_user_distance = float('inf') # the distance from the nearest base station to the user
    for gs in GSs:
        # convert the latitude and longitude coordinates of the ground station gs into
        # three-dimensional Cartesian coordinates
        gs_x,gs_y,gs_z = latilong_to_descartes(gs , "GS")
        # determine whether the satellite satellite is visible to the ground station gs at time t.
        # If visible, further calculate its distance from the user.
        if judgePointToSatellite(sat_x , sat_y , sat_z , gs_x , gs_y , gs_z , minimum_elevation):
            distance_between_user_and_GS = distance_two_terrestrial_point(user , gs)
            if distance_between_user_and_GS < GS_to_user_distance:
                GS_to_user_distance = distance_between_user_and_GS
                nearest_GS_to_user = gs
    return nearest_GS_to_user





# Parameters:
# source is the source of communication, and target is the destination of communication. Both the two parameters
# are user class objects.
# dT : how often to record a timeslot
# sh : a shell class object, representing a shell in the constellation
# ground_station_file: the data file of the satellite constellation ground base station GS (given in
#                      the form of path + file name)
# POP_file: satellite constellation ground POP point data file (given in the form of path + file name)
# α : the great circle distance coefficient between the source and target points. That is, since the actual
#     communication distance may not be the calculated exact distance, the calculated distance from the source to the
#     target is multiplied by a distance coefficient α to serve as the source. The final bent-pipe communication
#     distance to the target
# β : the communication speed between source and target. The speed of light in vacuum is c, but the speed of
#     communication between source and target may not be c. Therefore, the speed of light c multiplied by the speed
#     coefficient β represents the final communication speed from source to target. speed
# maximum_depression : the maximum depression angle of the satellite, and minimum_elevation is the minimum elevation
#                      angle of the ground observation point. The units of these two parameters are degrees (°).
def delay(source , target , dT , sh , ground_station_file , POP_file , α = 1.1 , β = 1.0 , minimum_elevation = 25):
    # read ground base station data
    ground_station = read_xml_file(ground_station_file)
    # generate GS
    GSs = []
    for gs_count in range(1, len(ground_station['GSs']) + 1, 1):
        gs = GS.ground_station(longitude=float(ground_station['GSs']['GS' + str(gs_count)]['Longitude']),
                               latitude=float(ground_station['GSs']['GS' + str(gs_count)]['Latitude']),
                               description=ground_station['GSs']['GS' + str(gs_count)]['Description'],
                               frequency=ground_station['GSs']['GS' + str(gs_count)]['Frequency'],
                               antenna_count=int(ground_station['GSs']['GS' + str(gs_count)]['Antenna_Count']),
                               uplink_GHz=float(ground_station['GSs']['GS' + str(gs_count)]['Uplink_Ghz']),
                               downlink_GHz=float(ground_station['GSs']['GS' + str(gs_count)]['Downlink_Ghz']))
        GSs.append(gs)
    # read ground POP point data
    POP = read_xml_file(POP_file)
    # generate POP
    POPs = []
    for pop_count in range(1, len(POP['POPs']) + 1, 1):
        pop = POP_POINT.POP(longitude=float(POP['POPs']['POP' + str(pop_count)]['Longitude']),
                            latitude=float(POP['POPs']['POP' + str(pop_count)]['Latitude']),
                            POP_name=POP['POPs']['POP' + str(pop_count)]['Name'])
        POPs.append(pop)
    # List type, used to store the delay time from source to target in bent-pipe mode in each timeslot, unit: seconds
    minimum_delay_time = []
    for t in range(1, (int)(sh.orbit_cycle / dT) + 3, 1):
        # find the source satellite and target satellite
        satellite_to_source, satellite_to_target = user_connect_satelite_policy1(source, target, sh, t)
        # find the GS closest to the source among all GS within the visible range of the satellite satellite_to_source
        nearest_GS_to_source = satellite_connect_groundstation_policy1(source, satellite_to_source, GSs, t,
                                                                       minimum_elevation)
        # if there is no GS within the visible range of the source satellite in the current timeslot,
        # it means communication is impossible.
        if nearest_GS_to_source is None:
            minimum_delay_time.append(float('inf'))
            continue
        # find the GS closest to target among all GS within the visible range of satellite satellite_to_target
        nearest_GS_to_target = satellite_connect_groundstation_policy1(target, satellite_to_target, GSs, t,
                                                                       minimum_elevation)
        # if there is no GS within the visible range of the target satellite in the current timeslot,
        # it means communication is impossible.
        if nearest_GS_to_target is None:
            minimum_delay_time.append(float('inf'))
            continue
        # find the POP point closest to the base station nearest_GS_to_source,
        # find the POP point closest to the base station nearest_GS_to_target
        nearest_POP_to_sourceGS = None
        POP_to_sourceGS_distance = float('inf')
        nearest_POP_to_targetGS = None
        POP_to_targetGS_distance = float('inf')
        for pop in POPs:
            distance_between_pop_and_sourceGS = distance_two_terrestrial_point(pop, nearest_GS_to_source)
            if distance_between_pop_and_sourceGS < POP_to_sourceGS_distance:
                POP_to_sourceGS_distance = distance_between_pop_and_sourceGS
                nearest_POP_to_sourceGS = pop
            distance_between_pop_and_targetGS = distance_two_terrestrial_point(pop, nearest_GS_to_target)
            if distance_between_pop_and_targetGS < POP_to_targetGS_distance:
                POP_to_targetGS_distance = distance_between_pop_and_targetGS
                nearest_POP_to_targetGS = pop

        # at this point, nearest_POP_to_sourceGS represents the POP point closest to the source base station,
        # and nearest_POP_to_targetGS represents the POP point closest to the target base station.

        # To calculate the delay between source and target, you need to calculate the delay between
        # nearest_GS_to_source → nearest_POP_to_sourceGS → nearest_POP_to_targetGS → nearest_GS_to_target.
        # Among them, the delays of nearest_GS_to_source → nearest_POP_to_sourceGS and nearest_POP_to_targetGS →
        # nearest_GS_to_target can be calculated directly based on the longitude and latitude coordinates.
        # The delay of nearest_POP_to_sourceGS → nearest_POP_to_targetGS is calculated using the distance of the
        # great circle of the earth.

        # calculate the distance in the three-dimensional Cartesian coordinate system between source and satellite
        # satellite_to_source, unit: km
        source_x, source_y, source_z = latilong_to_descartes(source, "User")
        sourcesatellite_x, sourcesatellite_y, sourcesatellite_z = latilong_to_descartes(satellite_to_source,
                                                                                        "satellite", t)
        distance_between_source_and_sourcesatellite = math.sqrt(
            (source_x - sourcesatellite_x) ** 2 + (source_y - sourcesatellite_y) ** 2
            + (source_z - sourcesatellite_z) ** 2) / 1000.0
        # calculate the distance in the three-dimensional Cartesian coordinate system between the satellite
        # satellite_to_source and the ground station nearest_GS_to_source, unit: km
        sourceGS_x, sourceGS_y, sourceGS_z = latilong_to_descartes(nearest_GS_to_source, "GS")
        distance_between_sourcesatellite_and_sourceGS = math.sqrt(
            (sourceGS_x - sourcesatellite_x) ** 2 + (sourceGS_y - sourcesatellite_y) ** 2
            + (sourceGS_z - sourcesatellite_z) ** 2) / 1000.0
        # calculate the distance between nearest_GS_to_source → nearest_POP_to_sourceGS, unit: km
        distance_between_sourceGS_and_sourceGSPOP = distance_two_terrestrial_point(nearest_GS_to_source,
                                                                                   nearest_POP_to_sourceGS)
        # calculate the distance between nearest_POP_to_sourceGS → nearest_POP_to_targetGS, unit: km
        distance_between_sourceGSPOP_and_targetGSPOP = distance_two_terrestrial_point(nearest_POP_to_sourceGS,
                                                                                      nearest_POP_to_targetGS)
        # calculate the distance between nearest_POP_to_targetGS → nearest_GS_to_target, unit: km
        distance_between_targetGS_and_targetGSPOP = distance_two_terrestrial_point(nearest_GS_to_target,
                                                                                   nearest_POP_to_targetGS)
        # calculate the distance in the three-dimensional Cartesian coordinate system between nearest_GS_to_target
        # and satellite_to_target, unit: km
        targetGS_x, targetGS_y, targetGS_z = latilong_to_descartes(nearest_GS_to_target, "GS")
        targetsatellite_x, targetsatellite_y, targetsatellite_z = latilong_to_descartes(satellite_to_target,
                                                                                        "satellite", t)
        distance_between_targetGS_and_targetsatellite = math.sqrt(
            (targetGS_x - targetsatellite_x) ** 2 + (targetGS_y - targetsatellite_y) ** 2
            + (targetGS_z - targetsatellite_z) ** 2) / 1000.0
        # calculate the distance between satellite_to_target and target
        target_x, target_y, target_z = latilong_to_descartes(target, "User")
        distance_between_targetsatellite_and_target = math.sqrt(
            (target_x - targetsatellite_x) ** 2 + (target_y - targetsatellite_y) ** 2
            + (target_z - targetsatellite_z) ** 2) / 1000.0
        # adding the above 7 distances together is the bent-pipe communication distance between source → target.
        distance_between_source_and_target = distance_between_source_and_sourcesatellite + \
                                             distance_between_sourcesatellite_and_sourceGS + \
                                             distance_between_sourceGS_and_sourceGSPOP + \
                                             distance_between_sourceGSPOP_and_targetGSPOP + \
                                             distance_between_targetGS_and_targetGSPOP + \
                                             distance_between_targetGS_and_targetsatellite + \
                                             distance_between_targetsatellite_and_target
        # since the actual communication distance may not be the exact distance_between_source_and_target,
        # distance_between_source_and_target is multiplied by a distance coefficient α to serve as the
        # final distance between source and target, unit: km
        distance_between_source_and_target = distance_between_source_and_target * α
        # communication speed between source and target, unit: kilometers/second, where 300000.0 is the speed of
        # light in vacuum, that is, 300,000 kilometers/second
        speed_between_source_and_target = 300000.0 * β
        # calculate the delay time between source and target, unit: seconds
        delay_between_source_and_target = distance_between_source_and_target / speed_between_source_and_target
        # the one-way delay calculated above is usually calculated as the round-trip time, which is the rtt value,
        # so it needs to be multiplied by 2.
        minimum_delay_time.append(delay_between_source_and_target * 2)

    return minimum_delay_time
