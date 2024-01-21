'''

Author : yunanhou

Date : 2023/11/30

Function : Find the shell to which the satellite belongs based on TLE data in json format

Specific idea: Read the "COSPAR_ID" field in the constellation's satellite launch batch (such as Starink's satellite
               launch batch, "config/TLE_constellation/Starlink/launches.xml"), and then compare it with the
               "OBJECT_ID" in the json format TLE data Fields are associated to determine which shell a satellite
               belongs to, because the shell the satellite is in is related to the batch it is launched from, and the
               satellite launch batch is identified by a unique "OBJECT_ID" field.

'''
import xml.etree.ElementTree as ET
import h5py
from datetime import datetime
import numpy as np
import json
import src.TLE_constellation.constellation_entity.launch as LAUNCH
import src.TLE_constellation.constellation_entity.satellite as SATELLITE
import src.TLE_constellation.constellation_entity.shell as SHELL



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


# Parameter :
# constellation_name : the name of constellation , such as "Starlink"
# Return Value :
# this function returns a collection of shell objects that have established corresponding relationships
def satellite_to_shell_mapping(constellation_name):
    # constellation launches information file
    constellation_launches_file = "config/TLE_constellation/" + constellation_name + \
                                  "/launches.xml"
    # read constellation launches information
    constellation_launches_information = read_xml_file(constellation_launches_file)
    # the following launches list is used to store launch class objects generated based on satellite launch batch data
    # read from xml
    launches = []
    for cospar_id_count in range(1 , len(constellation_launches_information['Launches'])+1 , 1):
        launch = LAUNCH.launch(
            str(constellation_launches_information['Launches']['Launch' + str(cospar_id_count)]['COSPAR_ID']) ,
            float(constellation_launches_information['Launches']['Launch' + str(cospar_id_count)]['Altitude']),
            float(constellation_launches_information['Launches']['Launch' + str(cospar_id_count)]['Inclination']))
        launches.append(launch)

    launch_altitude_inclination = []
    for launch in launches:
        launch_altitude_inclination.append((launch.altitude , launch.inclination))

    # use set to remove duplicate shells
    launch_altitude_inclination = list(set(launch_altitude_inclination))

    shells = []
    count=1
    for lai in launch_altitude_inclination:
        shells.append(SHELL.shell(lai[0] , lai[1] , "shell" + str(count)))
        count = count + 1


    # TLE data file
    constellation_json_TLE_file = "config/TLE_constellation/" + constellation_name + "/tle.h5"
    with h5py.File(constellation_json_TLE_file, 'a') as file:
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y%m%d')
        TLE_group = file[formatted_date]
        TLE_2LE = np.array(TLE_group[formatted_date + '-2LE']).tolist()
        TLE_2LE = [item.decode('utf-8') for item in TLE_2LE]
        # use zip to form a tuple of two adjacent elements
        TLE_2LE = list(zip(TLE_2LE[0::2], TLE_2LE[1::2]))
        TLE_JSON = np.array(TLE_group[formatted_date + '-json']).tolist()
        TLE_JSON = [item.decode('utf-8') for item in TLE_JSON]
        # convert string to JSON object
        TLE_JSON = [json.loads(item) for item in TLE_JSON]


    satellites = []
    for index in range(len(TLE_2LE)):
        satellite = SATELLITE.satellite(tle_json = TLE_JSON[index] , tle_2le = TLE_2LE[index])
        satellites.append(satellite)


    # determine the launch object of the satellite based on the first 8 bits of the "OBJECT_ID" field in the satellite
    # TLE data, and then determine the shell to which the satellite belongs based on the "altitude" and "inclination"
    # of the launch object
    for sat in satellites:
        sat_cospar_id = sat.cospar_id
        target_altitude = None
        target_inclination = None
        for laun in launches:
            if laun.cospar_id == sat_cospar_id:
                target_altitude = laun.altitude
                target_inclination = laun.inclination
                break
        for sh in shells:
            if target_altitude == sh.altitude and target_inclination == sh.inclination:
                sh.satellites.append(sat)
                sat.shell = sh
                break


    # calculate the orbit cycle of every shell
    for shell in shells:
        orbit_period = float('-inf')
        for satellite in shell.satellites:
            orbit_period = max(orbit_period, 1 / satellite.tle_json["MEAN_MOTION"] * 24 * 60 * 60)
        shell.orbit_cycle = int(orbit_period)


    # at this point in the code execution, the relationship between the satellite and the shell has been mapped
    # now return to shells
    return shells

