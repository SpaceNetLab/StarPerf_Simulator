'''

Author : yunanhou

Date : 2023/11/08

Function : Calculate constellation coverage in bent-pipe mode

Implementation method: In bent-pipe mode, the coverage of the constellation is not only related to the satellite itself,
                       but also to the GS. If a user is in an area where a satellite can be seen overhead, but there is
                       no GS within the visible range of the satellite, then the area where the user is located is said
                       to be not covered by bent-pipe. Specifically, the coverage rate in bent-pipe mode can be
                       calculated as follows: First, divide the earth's surface into several tiles, for example, every
                       10° interval according to the longitude and latitude, so that you will get 18*36 tiles. Then
                       select a point (latitude and longitude) in each tile as the user's position, take the user as the
                       perspective, calculate all satellites visible to the user (note the set of these satellites as S)
                       , traverse all satellites in the S set, as long as If at least one satellite in the S set has a
                       GS in its visible field of view, the tile is considered to be covered. Perform this operation on
                       all tiles, and finally divide the number of covered tiles by the total number of tiles, which is
                       the coverage rate of the constellation under the current timeslot. Perform the above operation on
                       all timeslots to obtain the constellation coverage under each timeslot. Constellation coverage,
                       and finally average the value and return it as the final constellation coverage.

'''
import math
import src.XML_constellation.constellation_entity.ground_station as GS
import xml.etree.ElementTree as ET
import src.XML_constellation.constellation_entity.user as USER

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


# The Tile class is a class used to represent a certain area on the earth's surface. The area is represented by four
# latitude and longitude coordinates.
class Tile:
    def __init__(self, longitude_start, longitude_end, latitude_start, latitude_end):
        self.longitude_start = longitude_start
        self.longitude_end = longitude_end
        self.latitude_start = latitude_start
        self.latitude_end = latitude_end


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


# Function : given a longitude and latitude coordinate position on the earth's surface, find all the satellites that can
#            be seen at the position at time t, and return a list set composed of these satellites.
# Parameters:
# user : the user, which is a User class object
# t : the t-th timeslot
# sh : the shell of the constellation
# minimum_elevation : the minimum elevation angle of the ground observation point, in degrees
def user_visible_all_satellites(user , t , sh , minimum_elevation):
    # calculate the coordinates of the user in the three-dimensional Cartesian coordinate system
    user_x,user_y,user_z = latilong_to_descartes(user , "User")
    # define a list to represent the collection of all satellites that the user can see.
    user_visible_all_satellites_list = []
    # traverse all satellites in sh
    for orbit in sh.orbits:
        for satellite in orbit.satellites:
            # calculate the coordinates of the satellite satellite in the three-dimensional Cartesian
            # coordinate system at time t
            sat_x,sat_y,sat_z = latilong_to_descartes(satellite , "satellite" , t)
            # determine whether satellite and user are visible. If visible, add satellite to
            # user_visible_all_satellites_list
            if judgePointToSatellite(sat_x,sat_y,sat_z , user_x,user_y,user_z , minimum_elevation):
                user_visible_all_satellites_list.append(satellite)
    return user_visible_all_satellites_list



# Function : Determine whether among all the satellites in the satellites collection, there is at least one satellite
#            with at least 1 GS within its visible range. If so, return true, otherwise return false
# Parameters:
# satellites : the set of all satellites within the visible range of the user at time t
# t : the t-th timeslot
# GSs : a collection of ground base stations, each element of which is a ground_station class object
# minimum_elevation : the minimum elevation angle of the ground observation point, in degrees
def judge_user_coveraged(satellites , t , GSs , minimum_elevation):
    for sat in satellites:
        # calculate the coordinates of satellite sat in the three-dimensional Cartesian coordinate system
        sat_x, sat_y, sat_z = latilong_to_descartes(sat, "satellite", t)
        # traverse all base stations in GSs and use sat to determine whether they are visible one by one.
        for gs in GSs:
            # calculate the coordinates of base station gs in the three-dimensional Cartesian coordinate system
            gs_x,gs_y,gs_z = latilong_to_descartes(gs , "GS")
            # determine whether the satellite sat can see gs, if so, return true
            if judgePointToSatellite(sat_x, sat_y, sat_z , gs_x,gs_y,gs_z , minimum_elevation):
                return True
    return False



# Function : Calculate the coverage of the constellation in bent-pipe mode
# Parameters:
# dT : how often to record a timeslot
# sh : a shell class object, representing a shell in the constellation
# ground_station_file: the data file of the satellite constellation ground base station GS (given in the form
#                      of path + file name)
# minimum_elevation : the minimum elevation angle of the ground observation point, in degrees
# tile_size : the size of the square block on the earth's surface. For example, the default is to cut every 10°,
#             that is, each block occupies 10° longitude and 10° latitude.
def coverage(dT , sh , ground_station_file , minimum_elevation = 25 , tile_size=10):
    Tiles = []
    for lon in range(-180, 180, tile_size):
        for lat in range(-90, 90, tile_size):
            tile = Tile(lon, lon + tile_size, lat, lat + tile_size)
            Tiles.append(tile)
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
    # define a list to represent the constellation coverage of each timeslot
    coverage_rate_per_timeslot = []
    for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
        # define a list to represent the set of tiles that can be covered by the constellation at time t
        coveraged_tiles = []
        for tile in Tiles:
            # find a point in each tile to represent the user's location
            user_longitude = (tile.longitude_start + tile.longitude_end) / 2
            user_latitude = (tile.latitude_start + tile.latitude_end) / 2
            user = USER.user(user_longitude, user_latitude)
            # find all satellites visible to (user_longitude, user_latitude)
            user_visible_all_satellites_list = user_visible_all_satellites(user , t , sh , minimum_elevation)
            # If there is at least one satellite in the user_visible_all_satellites_list collection that has at
            # least one GS within its visible range, the current tile is covered
            if judge_user_coveraged(user_visible_all_satellites_list , t , GSs , minimum_elevation):
                coveraged_tiles.append(tile)
        # calculate the current timeslot constellation coverage
        coverage_rate_current_timeslot = 1.0 * len(coveraged_tiles) / len(Tiles)
        coverage_rate_per_timeslot.append(coverage_rate_current_timeslot)

    return coverage_rate_per_timeslot