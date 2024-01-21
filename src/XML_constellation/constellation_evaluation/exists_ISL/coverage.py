'''

Author : yunanhou

Date : 2023/10/18

Function : calculate the coverage of a certain layer of shell in the constellation

Calculation method: Divide the longitude of the earth's surface every 10° and the latitude every 10°, thus obtaining
                    18*36 fragments. Each fragment represents a certain area of the earth's surface.

'''

import math
import h5py
import numpy as np


# The Tile class is a class used to represent a certain area on the earth's surface. The area is represented by
# four latitude and longitude coordinates.
class Tile:
    def __init__(self, longitude_start, longitude_end, latitude_start, latitude_end):
        self.longitude_start = longitude_start
        self.longitude_end = longitude_end
        self.latitude_start = latitude_start
        self.latitude_end = latitude_end
        self.population = 0 # the population in the area
        self.satellites = 0 # the number of satellites visible in the area




# Function : Determine whether the circular area observed by the satellite overlaps with a square tile. Returns True
#            if there is overlap, False if there is no overlap.
# Parameters:
# tile : an instantiated object of the Tile class
# sat_longitude and sat_latitude represent the longitude and latitude of the satellite subsatellite point respectively
# central_angle : the central angle of the satellite
def judge_tile_sat(tile , sat_longitude , sat_latitude , central_angle):
    flag_latitude = False
    flag_longitude = False
    if sat_latitude > 0 and sat_latitude + central_angle > 90 :
        latitude_upper_boundary = 90
        latitude_lower_boundary = min(sat_latitude - central_angle , 180 - central_angle - sat_latitude)
        if ( tile.latitude_start >= latitude_lower_boundary and tile.latitude_start <= latitude_upper_boundary ) or \
                (tile.latitude_end >= latitude_lower_boundary and tile.latitude_end <= latitude_upper_boundary) :
            flag_latitude = True
    elif sat_latitude < 0 and sat_latitude - central_angle < -90 :
        latitude_upper_boundary = max(sat_latitude + central_angle , central_angle - sat_latitude - 180)
        latitude_lower_boundary = -90
        if ( tile.latitude_start >= latitude_lower_boundary and tile.latitude_start <= latitude_upper_boundary ) or \
                (tile.latitude_end >= latitude_lower_boundary and tile.latitude_end <= latitude_upper_boundary) :
            flag_latitude = True
    else:
        latitude_upper_boundary = sat_latitude + central_angle
        latitude_lower_boundary = sat_latitude - central_angle
        if ( tile.latitude_start >= latitude_lower_boundary and tile.latitude_start <= latitude_upper_boundary ) or \
                (tile.latitude_end >= latitude_lower_boundary and tile.latitude_end <= latitude_upper_boundary) :
            flag_latitude = True

    if (sat_longitude > 0 and sat_longitude - central_angle < 0) or (sat_longitude < 0 and sat_longitude + central_angle > 0) :
        longitude_upper_boundary = sat_longitude + central_angle
        longitude_mid_boundary = 0
        longitude_lower_boundary = sat_longitude - central_angle
        if (tile.longitude_start >= longitude_lower_boundary and tile.longitude_start <= longitude_mid_boundary) or \
                (tile.longitude_end >= longitude_lower_boundary and tile.longitude_end <= longitude_mid_boundary) :
            flag_longitude = True
        if (tile.longitude_start >= longitude_mid_boundary and tile.longitude_start <= longitude_upper_boundary) or \
                (tile.longitude_end >= longitude_mid_boundary and tile.longitude_end <= longitude_upper_boundary) :
            flag_longitude = True
    elif sat_longitude > 0 and sat_longitude + central_angle > 180 :
        longitude_boundary_1 = sat_longitude - central_angle
        longitude_boundary_2 = 180
        longitude_boundary_3 = central_angle + sat_longitude - 360
        longitude_boundary_4 = -180
        if (tile.longitude_start >= longitude_boundary_1 and tile.longitude_start <= longitude_boundary_2) or \
                (tile.longitude_end >= longitude_boundary_1 and tile.longitude_end <= longitude_boundary_2) :
            flag_longitude = True
        if (tile.longitude_start >= longitude_boundary_4 and tile.longitude_start <= longitude_boundary_3) or \
                (tile.longitude_end >= longitude_boundary_4 and tile.longitude_end <= longitude_boundary_3) :
            flag_longitude = True
    elif sat_longitude < 0 and sat_longitude - central_angle < -180 :
        longitude_boundary_1 = sat_longitude + central_angle
        longitude_boundary_2 = -180
        longitude_boundary_3 = 360 - central_angle + sat_longitude
        longitude_boundary_4 = 180
        if (tile.longitude_start >= longitude_boundary_2 and tile.longitude_start <= longitude_boundary_1) or \
                (tile.longitude_end >= longitude_boundary_2 and tile.longitude_end <= longitude_boundary_1) :
            flag_longitude = True
        if (tile.longitude_start >= longitude_boundary_3 and tile.longitude_start <= longitude_boundary_4) or \
                (tile.longitude_end >= longitude_boundary_3 and tile.longitude_end <= longitude_boundary_4) :
            flag_longitude = True
    else :
        longitude_upper_boundary = sat_longitude + central_angle
        longitude_lower_boundary = sat_longitude - central_angle
        if (tile.longitude_start >= longitude_lower_boundary and tile.longitude_start <= longitude_upper_boundary) or \
                (tile.longitude_end >= longitude_lower_boundary and tile.longitude_end <= longitude_upper_boundary) :
            flag_longitude = True


    return flag_latitude and flag_longitude


# Parameters:
# constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
# dT : how often a timeslot is recorded
# sh : a shell class object, representing a shell in the constellation
# tile_size : the size of the square block on the earth's surface. For example, the default is to cut every 10°,
#             that is, each block occupies 10° longitude and 10° latitude.
# maximum_depression is the maximum depression angle of the satellite, and minimum_elevation is the minimum elevation
# angle of the ground observation point. The units of these two parameters are degrees (°).
def coverage(constellation_name , dT , sh ,tile_size=10 , maximum_depression = 56.5 , minimum_elevation = 25):
    Tiles = []
    for lon in range(-180, 180 , tile_size):
        for lat in range(-90 , 90 , tile_size):
            tile = Tile(lon , lon+tile_size , lat , lat+tile_size)
            Tiles.append(tile)
    central_angle = 180 - 2 * (maximum_depression + minimum_elevation) # satellite center angle
    coverage_per_timeslot = [] # list type, used to store the sh coverage of each timeslot
    file_path = "data/XML_constellation/" + constellation_name + ".h5"  # h5 file path and name
    # loop to calculate the coverage of each timeslot
    for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
        # read the satellite position of the shell layer of the constellation constellation at time t
        with h5py.File(file_path, 'r') as file:
            # access the existing first-level subgroup position group
            position_group = file['position']
            # access the existing secondary subgroup 'shell'+str(count) subgroup
            current_shell_group = position_group[sh.shell_name]
            # read the data set
            position = np.array(current_shell_group['timeslot' + str(t)]).tolist()
            position = [element.decode('utf-8') for row in position for element in row]
            position = [position[i:i + 3] for i in range(0, len(position), 3)]
            position = [[float(element) for element in row] for row in position]
        # a list object indicates which tiles can be covered by the entire constellation shell under timeslot t.
        # The list stores Tile class objects.
        tiles_t = []
        for sat in position:
            sat_longitude = sat[0] # the longitude of sat
            sat_latitude = sat[1] # the latitude of sat
            for tile in Tiles :
                if judge_tile_sat(tile , sat_longitude , sat_latitude , central_angle) :
                    tiles_t.append(tile)
        tiles_t = set(tiles_t) # set a set collection and remove duplicate elements
        coverage_per_timeslot.append(1.0*len(tiles_t)/len(Tiles))

    return coverage_per_timeslot





# Function : calculate the number of satellites visible per million people by latitude and longitude
# Parameters:
# constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
# dT : how often a timeslot is recorded
# sh : a shell class object, representing a shell in the constellation
# tile_size : the size of the square block on the earth's surface. For example, the default is to cut every 10°, that
#             is, each block occupies 10° longitude and 10° latitude.
# maximum_depression is the maximum depression angle of the satellite, and minimum_elevation is the minimum elevation
# angle of the ground observation point. The units of these two parameters are degrees (°).
def coverage_aggregated_by_latitude_and_longitude(constellation_name , dT , sh ,tile_size=10 , maximum_depression =
                                                    56.5 , minimum_elevation = 25):
    central_angle = 180 - 2 * (maximum_depression + minimum_elevation)  # satellite center angle
    satellite_in_latitude = [0 for i in range(int(180 / tile_size))]
    satellite_in_longitude = [0 for i in range(int(360 / tile_size))]
    file_path = "data/XML_constellation/" + constellation_name + ".h5"  # h5 file path and name
    for time in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
        # read the satellite position of the shell layer of the constellation constellation at time
        with h5py.File(file_path, 'r') as file:
            # access the existing first-level subgroup position group
            position_group = file['position']
            # access the existing secondary subgroup 'shell'+str(count) subgroup
            current_shell_group = position_group[sh.shell_name]
            # read the data set
            position = np.array(current_shell_group['timeslot' + str(time)]).tolist()
            position = [element.decode('utf-8') for row in position for element in row]
            position = [position[i:i + 3] for i in range(0, len(position), 3)]
            position = [[float(element) for element in row] for row in position]
        for satellite_no in range(sh.number_of_satellites):
            latitude = position[satellite_no][1]
            latitude_lower_boundary = int(math.floor((latitude - central_angle / 2) / tile_size))
            latitude_upper_boundary = int(math.floor((latitude + central_angle / 2) / tile_size))
            if latitude_lower_boundary < -int(180 / tile_size / 2):
                latitude_lower_boundary = -int(180 / tile_size / 2)
            if latitude_upper_boundary > int(180 / tile_size / 2)-1:
                latitude_upper_boundary = int(180 / tile_size / 2)-1
            for k in range(latitude_lower_boundary, latitude_upper_boundary + 1):
                satellite_in_latitude[k + int(180 / tile_size / 2)] += 1

            longitude = position[satellite_no][0]
            longitude_lower_boundary = int(math.floor((longitude - central_angle / 2) / tile_size))
            longitude_upper_boundary = int(math.floor((longitude + central_angle / 2) / tile_size))
            if longitude_lower_boundary < -int(360 / tile_size / 2):
                longitude_lower_boundary = int(
                    math.floor((180 - (-180 - longitude + central_angle / 2)) / tile_size))
            if longitude_upper_boundary > int(360 / tile_size / 2)-1:
                longitude_upper_boundary = int(
                    math.floor((-180 + longitude + central_angle / 2 - 180) / tile_size))
            if longitude_lower_boundary > 0 and longitude_upper_boundary < 0:
                for k in range(longitude_lower_boundary, int(360 / tile_size / 2)):
                    satellite_in_longitude[k + int(360 / tile_size / 2)] += 1
                for k in range(-int(360 / tile_size / 2), longitude_upper_boundary + 1):
                    satellite_in_longitude[k + int(360 / tile_size / 2)] += 1
            else:
                for k in range(longitude_lower_boundary, longitude_upper_boundary + 1):
                    satellite_in_longitude[k + int(360 / tile_size / 2)] += 1

    # find the average of each timeslot
    satellite_in_latitude = [x / float((int)(sh.orbit_cycle / dT) + 1) for x in satellite_in_latitude]
    satellite_in_longitude = [x / float((int)(sh.orbit_cycle / dT) + 1) for x in satellite_in_longitude]

    return satellite_in_latitude , satellite_in_longitude

