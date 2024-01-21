'''

Author: yunanhou

Date: 2023/12/10

Function : "n-nearest" connection mode, that is, a satellite establishes ISL with the n satellites closest to itself,
           and the n value is specified by the user.


When using this connection mode, since ISL has an effective distance range, it is possible to establish ISL only when
adjacent satellites are within this distance range.

To simplify matters, we assume that ISL will not be disconnected and rebuilt once established.

'''
import h5py
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt
import numpy as np
import src.TLE_constellation.constellation_entity.ISL as ISL_module

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

def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: xml_to_dict(root)}



# Function : Calculate the distance between two satellites (the calculation result takes into account the curvature
#            of the earth), the unit of the returned value is kilometers
def distance_two_satellites(satellite1 , satellite2 , t):
    longitude1 = satellite1.longitude[t-1]
    latitude1 = satellite1.latitude[t-1]
    longitude2 = satellite2.longitude[t-1]
    latitude2 = satellite2.latitude[t-1]
    # The altitude is the average altitude of the two satellites, in kilometers
    altitude = 1.0 * (satellite1.altitude[t-1] + satellite2.altitude[t-1]) / 2
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2), float(latitude2)]) # 经纬度转换成弧度
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    # The average radius of the earth is 6371km, and the satellite orbit altitude is 6371km.
    distance=2*asin(sqrt(a))*(6371.0+altitude)*1000
    # Convert the result to kilometers with three decimal places.
    distance=np.round(distance/1000,3)
    return distance


# Function : find all satellites in the current shell that are within the range of
#            [shortest_distance,longest_distance] from the current satellite and with less than n ISLs have been established
# Parameters:
# current_shell : a shell class object
# current_satellite : a satellite class object
# shortest_distance,longest_distance : ISL effective distance range
# n : the value of n in n-nearest mode
def find_satellites_in_the_shell_and_between_shortestdistance_and_longestdistance(current_shell , current_satellite ,
                                                                                  shortest_distance , longest_distance , n):
    satellites_in_shell_and_between_shortestdistance_and_longestdistance = []
    for satellite in current_shell.satellites:
        distance_between_satellite_and_currentsatellite = distance_two_satellites(current_satellite , satellite,1)
        if (longest_distance >= distance_between_satellite_and_currentsatellite >= shortest_distance and
                len(satellite.ISL) < n):
            satellites_in_shell_and_between_shortestdistance_and_longestdistance.append(satellite)
    return satellites_in_shell_and_between_shortestdistance_and_longestdistance


# Parameters:
# constellation : the constellation to establish n_nearest connection
# dT : the time interval
# n : each satellite can establish up to n ISLs
def n_nearest(constellation , dT , n):
    file_path = "data/TLE_constellation/" + constellation.constellation_name + ".h5"
    with h5py.File(file_path, 'a') as file:
        # get a list of root-level group names
        root_group_names = list(file.keys())
        # if the delay group is not in the root-level group of the file file, create a new root-level delay group.
        if 'delay' not in root_group_names:
            delay_group = file.create_group('delay')
            # create multiple shell subgroups within the delay group. For example, the shell1 subgroup represents the
            # first-level shell, the shell2 subgroup represents the second-level shell, etc.
            for count in range(1, constellation.number_of_shells + 1, 1):
                delay_group.create_group('shell' + str(count))


    # get ISL shortest distance and longest distance (unit : km)
    ISL_distance_range_file_path = \
        "src/TLE_constellation/constellation_connectivity/connectivity_plugin/ISL_distance_range.xml"
    ISL_distance_range = read_xml_file(ISL_distance_range_file_path)
    shortest_distance = float(ISL_distance_range["ISL_distance_range"]["shortest_distance"])
    longest_distance = float(ISL_distance_range["ISL_distance_range"]["longest_distance"])

    # traverse the shells and establish intra-layer ISL for each layer of shells.
    for shell_index, shell in enumerate(constellation.shells):
        for satellite in shell.satellites:
            if len(satellite.ISL) < n:
                # number of ISLs to be established
                number_of_need_create_ISL = n - len(satellite.ISL)
                # find all satellites in the current shell that are within the range of
                # [shortest_distance,longest_distance] from the current satellite and with less than n ISLs have
                # been established
                satellites_in_shell_and_between_shortestdistance_and_longestdistance = \
                find_satellites_in_the_shell_and_between_shortestdistance_and_longestdistance(shell,
                                                                satellite,shortest_distance , longest_distance , n)
                if len(satellites_in_shell_and_between_shortestdistance_and_longestdistance) >= number_of_need_create_ISL:
                    for index in range(number_of_need_create_ISL):
                        other_satellite = satellites_in_shell_and_between_shortestdistance_and_longestdistance[index]
                        isl = ISL_module.ISL(satellite1=satellite , satellite2=other_satellite)
                        isl_distance = [] # the distance attribute of the isl object
                        isl_delay = [] # delay attribute of isl object
                        # calculate the ISL delay and distance between satellites in each timeslot
                        for t in range(1 , (int)(shell.orbit_cycle / dT) + 3 , 1):
                            # calculate the distance between the two satellites
                            distance = distance_two_satellites(other_satellite , satellite , t)
                            isl_distance.append(distance)
                            # calculate the delay between the two satellites
                            delay = 1.0 * distance / 300000.0
                            isl_delay.append(delay)
                        isl.distance = isl_distance
                        isl.delay = isl_delay
                        satellite.ISL.append(isl)
                        other_satellite.ISL.append(isl)
                else:
                    for index in range(len(satellites_in_shell_and_between_shortestdistance_and_longestdistance)):
                        other_satellite = satellites_in_shell_and_between_shortestdistance_and_longestdistance[index]
                        isl = ISL_module.ISL(satellite1=satellite, satellite2=other_satellite)
                        isl_distance = []  # the distance attribute of the isl object
                        isl_delay = []  # delay attribute of isl object
                        # calculate the ISL delay and distance between satellites in each timeslot
                        for t in range(1, (int)(shell.orbit_cycle / dT) + 3, 1):
                            # calculate the distance between the two satellites
                            distance = distance_two_satellites(other_satellite, satellite, t)
                            isl_distance.append(distance)
                            # calculate the delay between the two satellites
                            delay = 1.0 * distance / 300000.0
                            isl_delay.append(delay)
                        isl.distance = isl_distance
                        isl.delay = isl_delay
                        satellite.ISL.append(isl)
                        other_satellite.ISL.append(isl)

        # save the delay matrix of this layer shell (sh) at each time t to a file
        for t in range(1, (int)(shell.orbit_cycle / dT) + 3, 1):
            # establish a delay matrix of points between satellites to store the delay time between any two satellites.
            # the unit is seconds. The rows and columns with the subscript 0 are left empty. Data is stored starting
            delay = [[0 for j in range(len(shell.satellites) + 1)] for i in range(len(shell.satellites) + 1)]# from row 1 and column 1.
            for satellite in shell.satellites:
                for isl in satellite.ISL:
                    sat1 = isl.satellite1
                    sat2 = isl.satellite2
                    if sat1 == satellite.id:
                        other_satellite = sat2
                    else:
                        other_satellite = sat1
                    delay[satellite.id][other_satellite] = isl.delay[t - 1]

            with h5py.File(file_path, 'a') as file:
                # access the existing first-level subgroup delay group
                delay_group = file['delay']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = delay_group['shell' + str(shell_index + 1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=delay)
