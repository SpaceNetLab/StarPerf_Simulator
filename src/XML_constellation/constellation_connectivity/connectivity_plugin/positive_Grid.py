'''

Author : yunanhou

Date : 2023/08/24

Function : This script is used to simulate the constellation working in +Grid mode

Input : Satellite constellation without any ISL (i.e. each satellite is a node and there are no edges between nodes)

Output : A satellite constellation that has been connected according to the +Grid mode (that is, each satellite has 4
         ISLs to establish connections with two satellites in the same orbit and two satellites in adjacent orbits)


After the file is executed, ISLs have been established between the satellites in each shell in the incoming
constellation, and the delay time matrix between each satellite has also been written to the data/ folder.

'''
import h5py
from math import radians, cos, sin, asin, sqrt
import numpy as np
import src.XML_constellation.constellation_entity.ISL as ISL_module

# Function : Find the corresponding satellite according to the satellite's ID.
# Parameters:
# sh : a shell of a certain layer of the satellite constellation
# target_id : the ID number of the satellite to be found.
def search_satellite_by_id(sh , target_id):
    # the total number of satellites contained in the sh layer shell
    number_of_satellites_in_sh = sh.number_of_satellites
    # the total number of tracks contained in the sh layer shell
    number_of_orbits_in_sh = sh.number_of_orbits
    # in the sh layer shell, the number of satellites contained in each orbit
    number_of_satellites_per_orbit = (int)(number_of_satellites_in_sh / number_of_orbits_in_sh)
    # find the corresponding satellite according to the satellite id
    # traverse each orbit layer by layer, orbit_index starts from 1
    for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):
        # traverse the satellites in each orbit, satellite_index starts from 1
        for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):
            satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # get satellite object
            if satellite.id == target_id :
                return satellite


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



# Parameters:
# constellation : the constellation to establish +Grid connection
# dT : the time interval
def positive_Grid(constellation , dT):

    file_path = "data/XML_constellation/" + constellation.constellation_name + ".h5"
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

    # process the constellation layer by layer, processing each shell separately
    # sh is the shell object stored in constellation.shells, sh_index is the subscript of sh in constellation.shells
    for sh_index,sh in enumerate(constellation.shells):
        # the total number of satellites contained in the sh layer shell
        number_of_satellites_in_sh = sh.number_of_satellites
        # the total number of tracks contained in the sh layer shell
        number_of_orbits_in_sh = sh.number_of_orbits
        # in the sh layer shell, the number of satellites contained in each orbit
        number_of_satellites_per_orbit = (int)(number_of_satellites_in_sh / number_of_orbits_in_sh)

        # calculate distance and delay from one satellite to other satellites
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1,number_of_orbits_in_sh+1 , 1):
            # traverse the satellites in each orbit, satellite_index starts from 1
            for satellite_index in range(1 , number_of_satellites_per_orbit+1 , 1):
                # get the current satellite object
                cur_satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]
                # get the id of the current satellite
                cur_satellite_id = cur_satellite.id
                # get the id of the previous satellite of the current satellite
                up_satellite_id = -1
                if satellite_index != number_of_satellites_per_orbit:
                    up_satellite_id = cur_satellite_id+1
                else:
                    up_satellite_id = cur_satellite_id+1-satellite_index
                # find the corresponding satellite object up_satellite according to the id number up_satellite_id
                up_satellite = search_satellite_by_id(sh , up_satellite_id)
                # establish the ISL object between the two satellites cur_satellite and up_satellite
                isl_cur_up = ISL_module.ISL(satellite1=cur_satellite, satellite2=up_satellite)
                isl_cur_up_distance = [] # the distance attribute of the isl_cur_up object
                isl_cur_up_delay = [] # delay attribute of isl_cur_up object

                for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
                    # calculate the distance between the two satellites cur_satellite and up_satellite
                    distance_cur_up = distance_two_satellites(cur_satellite , up_satellite , t)
                    isl_cur_up_distance.append(distance_cur_up)
                    # calculate the delay between the two satellites cur_satellite and up_satellite
                    delay_cur_up = 1.0 * distance_cur_up / 300000.0
                    isl_cur_up_delay.append(delay_cur_up)
                isl_cur_up.distance = isl_cur_up_distance
                isl_cur_up.delay = isl_cur_up_delay
                cur_satellite.ISL.append(isl_cur_up)
                up_satellite.ISL.append(isl_cur_up)
                
                # get the id of the right satellite of the current satellite
                right_satellite_id = -1
                if orbit_index != number_of_orbits_in_sh:
                    right_satellite_id = orbit_index * number_of_satellites_per_orbit + satellite_index
                else:
                    if sh.inclination > 80 and sh.inclination < 100:
                        continue
                    else:
                        right_satellite_id = satellite_index
                # find the corresponding satellite object right_satellite according to the id number right_satellite_id
                right_satellite = search_satellite_by_id(sh, right_satellite_id)
                # establish an ISL object between the two satellites cur_satellite and right_satellite_id
                isl_cur_right = ISL_module.ISL(satellite1=cur_satellite, satellite2=right_satellite)
                isl_cur_right_distance = []  # the distance attribute of the isl_cur_right object
                isl_cur_right_delay = []  # delay attribute of isl_cur_right object
                # calculate the ISL delay and distance between satellites in each timeslot
                for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
                    # calculate the distance between the two satellites cur_satellite and right_satellite_id
                    distance_cur_right = distance_two_satellites(cur_satellite, right_satellite , t)
                    isl_cur_right_distance.append(distance_cur_right)
                    # calculate the delay between the two satellites cur_satellite and right_satellite_id
                    delay_cur_right = 1.0 * distance_cur_right / 300000.0
                    isl_cur_right_delay.append(delay_cur_right)

                isl_cur_right.distance = isl_cur_right_distance
                isl_cur_right.delay = isl_cur_right_delay
                # add the two ISLs between the current satellite and the previous satellite and the right satellite to
                # the satellite object
                cur_satellite.ISL.append(isl_cur_right)
                right_satellite.ISL.append(isl_cur_right)




        # save the delay matrix of this layer shell (sh) at each time t to a file
        for t in range(1, (int)(sh.orbit_cycle / dT) + 2, 1):
            # establish a delay matrix of points between satellites to store the delay time between any two satellites.
            # the unit is seconds. The rows and columns with the subscript 0 are left empty. Data is stored starting
            # from row 1 and column 1.
            delay = [[0 for j in range(number_of_satellites_in_sh + 1)] for i in range(number_of_satellites_in_sh + 1)]
            # traverse each orbit layer by layer, orbit_index starts from 1
            for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):
                # traverse the satellites in each orbit, satellite_index starts from 1
                for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):
                    # get the current satellite object
                    cur_satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]
                    for isls in cur_satellite.ISL:
                        sat1 = isls.satellite1
                        sat2 = isls.satellite2
                        if sat1 == cur_satellite.id:
                            other_satellite = sat2
                        else:
                            other_satellite = sat1
                        delay[cur_satellite.id][other_satellite] = isls.delay[t-1]

            with h5py.File(file_path, 'a') as file:
                # access the existing first-level subgroup delay group
                delay_group = file['delay']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = delay_group['shell' + str(sh_index+1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=delay)