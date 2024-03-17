'''

Author : yunanhou

Date : 2023/08/25

Function : This script defines the constellation configuration information function, including constellation name,
           number of shells, number of satellites, number of orbits, inclination, orbit altitude, etc. The function of
           this function is to read the data of the config/constellation_generation/<constellation_name>.xml
           configuration file

'''
import os
import h5py
import src.XML_constellation.constellation_entity.shell as shell
import src.constellation_generation.by_XML.orbit_configuration as orbit_configuration
import xml.etree.ElementTree as ET
import src.XML_constellation.constellation_entity.constellation as CONSTELLATION


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



# Parameters:
# dT : the timeslot, and the timeslot t is calculated from 1
# constellation_name : the name of the constellation to be generated, used to read the xml configuration file
def constellation_configuration(dT , constellation_name):
    # the path to the constellation configuration information file .xml file
    xml_file_path = "config/XML_constellation/" + constellation_name + ".xml"
    # read constellation configuration information
    constellation_configuration_information = read_xml_file(xml_file_path)
    # convert string to int type
    number_of_shells = int(constellation_configuration_information['constellation']['number_of_shells'])
    shells = []
    # ensure the data/XML_constellation/ directory exists
    data_directory = "data/XML_constellation/"
    # This will create the directory if it does not exist
    os.makedirs(data_directory, exist_ok=True)
    # determine whether the .h5 file of the delay and satellite position data of the current constellation exists. If
    # it exists, delete the file and create an empty .h5 file. If it does not exist, directly create an empty .h5 file.
    file_path = "data/XML_constellation/" + constellation_name + ".h5"
    if os.path.exists(file_path):
        # if the .h5 file exists, delete the file
        os.remove(file_path)
    # create new empty .h5 file
    with h5py.File(file_path, 'w') as file:
        # create position group
        position = file.create_group('position')
        # create multiple shell subgroups within the position group. For example, the shell1 subgroup represents the
        # first layer of shells, the shell2 subgroup represents the second layer of shells, etc.
        for count in range(1, number_of_shells + 1, 1):
            position.create_group('shell' + str(count))
    for count in range(1 , number_of_shells+1 , 1):
        altitude = int(constellation_configuration_information['constellation']['shell'+str(count)]['altitude'])
        orbit_cycle = int(constellation_configuration_information['constellation']['shell'+str(count)]['orbit_cycle'])
        inclination = float(constellation_configuration_information['constellation']['shell'+str(count)]['inclination'])
        phase_shift = int(constellation_configuration_information['constellation']['shell'+str(count)]['phase_shift'])
        number_of_orbit = int(constellation_configuration_information['constellation']['shell'+str(count)]['number_of_orbit'])
        number_of_satellite_per_orbit = int(constellation_configuration_information['constellation']['shell'+str(count)]
                                            ['number_of_satellite_per_orbit'])
        shell_name = "shell" + str(count)
        sh = shell.shell(altitude=altitude, number_of_satellites=number_of_orbit * number_of_satellite_per_orbit,
                         number_of_orbits=number_of_orbit, inclination=inclination, orbit_cycle=orbit_cycle,
                         number_of_satellite_per_orbit=number_of_satellite_per_orbit, phase_shift=phase_shift, shell_name = shell_name)
        # the basic properties of the sh layer have been configured. Now the track of the sh layer is generated.
        orbit_configuration.orbit_configuration(sh, dT)
        # all orbits and satellites in the sh layer have been configured. Now set the number of each satellite.
        # the number starts from 1.
        # the total number of satellites contained in the sh layer shell
        number_of_satellites_in_sh = sh.number_of_satellites
        # the total number of tracks contained in the sh layer shell
        number_of_orbits_in_sh = sh.number_of_orbits
        # in the sh layer shell, the number of satellites contained in each orbit
        number_of_satellites_per_orbit = (int)(
            number_of_satellites_in_sh / number_of_orbits_in_sh)
        # number each satellite in the sh layer, that is, modify the id attribute of the satellite object
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):
            # traverse the satellites in each orbit, satellite_index starts from 1
            for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):
                satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # get satellite object
                # set the ID number of the current satellite
                satellite.id = (orbit_index - 1) * number_of_satellites_per_orbit + satellite_index
        # add the current shell layer sh to the constellation
        shells.append(sh)
        # write the longitude, latitude, altitude and other location information of all satellites in the current
        # shell layer sh into a file and save it
        for tt in range(1 , (int)(sh.orbit_cycle / dT)+2 , 1):
            # this list is used to store the position information of all satellites in the current shell. It is a
            # two-dimensional list. Each element is a one-dimensional list. Each one-dimensional list contains three
            # elements, which respectively represent the longitude, latitude and altitude of a satellite.
            satellite_position = []
            for orbit in sh.orbits:
                for sat in orbit.satellites:
                    satellite_position.append([str(sat.longitude[tt-1]) , str(sat.latitude[tt-1]) , str(sat.altitude[tt-1])])
            with h5py.File(file_path, 'a') as file:
                # access the existing first-level subgroup position group
                position = file['position']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = position['shell' + str(count)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(tt) , data = satellite_position)
    # all shells, orbits, and satellites have been initialized, and the target constellation is generated and returned.
    target_constellation = CONSTELLATION.constellation(constellation_name=constellation_name, number_of_shells=
                                number_of_shells, shells=shells)
    return target_constellation

