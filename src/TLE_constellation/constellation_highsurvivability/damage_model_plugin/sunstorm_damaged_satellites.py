'''

Author: yunanhou

Date : 2023/12/17

Function : This script is used to simulate the availability of the constellation (including delay, bandwidth, etc.)
           after a group of satellites are damaged due to a solar storm accident. Simulate the specific way in which
           the solar wind damages the constellation: randomly destroy a group of satellites in the original
           constellation. After the satellite is destroyed, it will A hole is left.

           Modification of position information: directly delete the lines that need to be deleted. After the
           modification, the number of lines in the file is less than the number of lines before modification.

'''
import random
import h5py
import numpy as np
import networkx as nx
import copy
import src.TLE_constellation.constellation_entity.satellite as SATELLITE
import src.TLE_constellation.constellation_entity.orbit as ORBIT
import src.TLE_constellation.constellation_entity.shell as SHELL
import src.TLE_constellation.constellation_entity.constellation as CONSTELLATION
import os



# Parameters:
# constellation : the constellation that needs to be destroyed by the solar storm and is a constellation class object.
# sh : the shell that needs to be destroyed by the solar storm and is a shell class object
# num_of_damaged_satellites : the number of randomly destroyed satellites. If the value is less than 1, it is the
#                             number of satellites destroyed as a percentage of the total number; if the value is
#                             greater than 1, it is the number of satellites that need to be destroyed.
# dT : how often a timeslot is recorded
# satrt_satellite_id : the id of the most central satellite in a group of satellites to be destroyed. If
#                      satrt_satellite_id is -1, it means that the id of the center satellite of the destroyed group is
#                      not specified, but a randomly generated one.
# Return Value : returns the constellation name after num_of_damaged_satellites satellites have been destroyed
def sunstorm_damaged_satellites(constellation , sh , num_of_damaged_satellites , dT , satrt_satellite_id):
    # if num_of_damaged_satellites is less than 1, it is the number of satellites destroyed as a percentage of the
    # total number; if num_of_damaged_satellites is greater than 1, it is the number of satellites that need to be
    # destroyed.
    if num_of_damaged_satellites < 1:
        num_of_damaged_satellites = (int)(len(sh.satellites) * num_of_damaged_satellites)
    if satrt_satellite_id == -1:
        # randomly generate a destroyed satellite. start_point_lower_bound and start_point_upper_bound represent the
        # lower limit and upper limit of the ID of a destroyed satellite respectively.
        satrt_satellite_id_lower_bound = 1
        satrt_satellite_id_upper_bound = len(sh.satellites)
        satrt_satellite_id = random.randint(satrt_satellite_id_lower_bound, satrt_satellite_id_upper_bound)
    # read the delay matrix of the shell layer of the constellation constellation
    file_path = "data/TLE_constellation/" + constellation.constellation_name + ".h5"  # h5 file path and name

    # read the delay matrix of the shell layer of the constellation constellation at time t
    with h5py.File(file_path, 'r') as file:
        # access the existing first-level subgroup delay group
        delay_group = file['delay']
        # access the existing secondary subgroup 'shell'+str(count) subgroup
        current_shell_group = delay_group[sh.shell_name]
        # read the data set
        delay = np.array(current_shell_group['timeslot' + str(1)]).tolist()
    # create an undirected graph object named G, which is empty at first, with no nodes and edges.
    G = nx.Graph()
    satellite_nodes = []
    for i in range(1, len(delay), 1):
        satellite_nodes.append(i)
    G.add_nodes_from(satellite_nodes)  # add nodes to an undirected graph

    satellite_edges = []
    for i in range(1, len(delay), 1):
        for j in range(i + 1, len(delay), 1):
            if delay[i][j] > 0:
                satellite_edges.append((i, j))
    G.add_edges_from(satellite_edges)  # add edges to undirected graph
    # BFS traversal starts from the starting node satrt_satellite_id
    bfs_tree = nx.bfs_tree(G, source=satrt_satellite_id)
    # extract the results of BFS traversal
    bfs_result = list(bfs_tree.nodes())
    # take the first num_of_damaged_satellites nodes from bfs_result as satellite nodes that need to be destroyed.
    # What is stored in damaged_satellites is actually the ID of the satellite that needs to be deleted.
    damaged_satellites = bfs_result[:num_of_damaged_satellites]

    # deep copy of original constellation
    constellation_copy_name = constellation.constellation_name + "_sunstorm_damaged"
    constellation_copy_number_of_shells = constellation.number_of_shells
    constellation_copy_shells = []
    for every_shell_index, every_shell in enumerate(constellation.shells):
        shell_copy_altitude = every_shell.altitude  # height
        shell_copy_inclination = every_shell.inclination  # inclination
        shell_copy_orbit_cycle = every_shell.orbit_cycle  # cycle
        shell_copy_shell_name = every_shell.shell_name  # shell name
        shell_copy_orbits = []
        for every_orbit in every_shell.orbits:
            orbit_copy_raan_lower_bound = every_orbit.raan_lower_bound
            orbit_copy_raan_upper_bound = every_orbit.raan_upper_bound
            orbit_copy_satellites = []
            for every_satellite in every_orbit.satellites:
                if (every_satellite.id in damaged_satellites) and (
                        ("shell" + str(every_shell_index + 1)) == sh.shell_name):
                    continue  # the currently traversed satellite needs to be destroyed, so do nothing.
                else:
                    satellite_copy_tle_json = copy.deepcopy(every_satellite.tle_json)
                    satellite_copy_tle_2le = copy.deepcopy(every_satellite.tle_2le)
                    satellite_copy_cospar_id = copy.deepcopy(every_satellite.cospar_id)
                    satellite_copy_longitude = copy.deepcopy(every_satellite.longitude)
                    satellite_copy_latitude = copy.deepcopy(every_satellite.latitude)
                    satellite_copy_altitude = copy.deepcopy(every_satellite.altitude)
                    satellite_copy_ISL = copy.deepcopy(every_satellite.ISL)
                    satellite_copy_id = every_satellite.id
                    satellite_copy = SATELLITE.satellite(tle_json=satellite_copy_tle_json,
                                                         tle_2le=satellite_copy_tle_2le)
                    satellite_copy.cospar_id = satellite_copy_cospar_id
                    satellite_copy.longitude = satellite_copy_longitude
                    satellite_copy.latitude = satellite_copy_latitude
                    satellite_copy.altitude = satellite_copy_altitude
                    satellite_copy.ISL = satellite_copy_ISL
                    satellite_copy.id = satellite_copy_id
                    orbit_copy_satellites.append(satellite_copy)
            if len(orbit_copy_satellites) == 0:
                continue
            else:
                orbit_copy = ORBIT.orbit(shell=None, raan_lower_bound=orbit_copy_raan_lower_bound,
                                         raan_upper_bound=orbit_copy_raan_upper_bound)
                orbit_copy.satellites = orbit_copy_satellites
                shell_copy_orbits.append(orbit_copy)

        if len(shell_copy_orbits) == 0:
            continue
        else:
            shell_copy = SHELL.shell(altitude=shell_copy_altitude, inclination=shell_copy_inclination,
                                     shell_name=shell_copy_shell_name)
            shell_copy.orbit_cycle = shell_copy_orbit_cycle
            shell_copy.orbits = shell_copy_orbits
        constellation_copy_shells.append(shell_copy)

    constellation_copy = CONSTELLATION.constellation(constellation_name=constellation_copy_name,
                                                     number_of_shells=constellation_copy_number_of_shells,
                                                     shells=constellation_copy_shells)

    for sh in constellation_copy.shells:
        all_satellites_in_sh = []
        for orbit in sh.orbits:
            orbit.shell = sh
            for sat in orbit.satellites:
                sat.shell = sh
                sat.orbit = orbit
            all_satellites_in_sh = all_satellites_in_sh + orbit.satellites
        sh.satellites = all_satellites_in_sh

    # add ISL connections to the satellites in the constellation_copy constellation. These added ISL connections are
    # the ISLs after deleting the damaged satellites from the original constellation.
    for every_shell in constellation_copy.shells:
        for sat in every_shell.satellites:
            for isl_index in range(len(sat.ISL) - 1, -1, -1):
                if (sat.ISL[isl_index].satellite1 in damaged_satellites) or (
                        sat.ISL[isl_index].satellite2 in damaged_satellites):
                    sat.ISL.pop(isl_index)

    # modify the satellite id in the constellation_copy constellation so that it increases continuously starting from 1
    for every_shell in constellation_copy.shells:
        satellite_new_id = 1
        oldid_dict_newid = {}
        for sat in every_shell.satellites:
            # satellite original id
            satellite_old_id = sat.id
            # satellite new id
            sat.id = satellite_new_id
            oldid_dict_newid[satellite_old_id] = satellite_new_id
            satellite_new_id = satellite_new_id + 1

        # the satellite ID has been modified, and the ID in ISL also needs to be modified.
        for sat in every_shell.satellites:
            for isl_index in range(len(sat.ISL) - 1, -1, -1):
                sat.ISL[isl_index].satellite1 = oldid_dict_newid[sat.ISL[isl_index].satellite1]
                sat.ISL[isl_index].satellite2 = oldid_dict_newid[sat.ISL[isl_index].satellite2]

    # determine whether the .h5 file of the delay and satellite position data of the current constellation exists.
    # If it exists, delete the file and create an empty .h5 file. If it does not exist, directly create an empty
    # .h5 file.
    copy_file_path = "data/TLE_constellation/" + constellation_copy_name + ".h5"
    if os.path.exists(copy_file_path):
        # if the .h5 file exists, delete the file
        os.remove(copy_file_path)
    # create new empty .h5 file
    with h5py.File(copy_file_path, 'w') as file:
        # create position group
        position = file.create_group('position')
        # create multiple shell subgroups within the position group. For example, the shell1 subgroup represents the
        # first layer of shells, the shell2 subgroup represents the second layer of shells, etc.
        for count in range(1, len(constellation.shells) + 1, 1):
            position.create_group('shell' + str(count))
        # create delay group
        delay = file.create_group('delay')
        # create multiple shell subgroups within the delay group. For example, the shell1 subgroup represents the
        # first-level shell, the shell2 subgroup represents the second-level shell, etc.
        for count in range(1, len(constellation.shells) + 1, 1):
            delay.create_group('shell' + str(count))

    for sh2_index, sh2 in enumerate(constellation_copy.shells):
        # the total number of satellites contained in the sh2 layer shell
        number_of_satellites_in_sh2 = len(sh2.satellites)
        # create the delay matrix of the constellation_copy constellation and write the h5 file
        for t in range(1, (int)(sh.orbit_cycle / dT) + 3, 1):
            constellation_copy_delay = [[0 for j in range(number_of_satellites_in_sh2 + 1)] for i in
                                        range(number_of_satellites_in_sh2 + 1)]
            for sat in sh2.satellites:
                for isls in sat.ISL:
                    sat1 = isls.satellite1
                    sat2 = isls.satellite2
                    if sat1 == sat.id:
                        other_satellite = sat2
                    else:
                        other_satellite = sat1

                    constellation_copy_delay[sat.id][other_satellite] = isls.delay[t - 1]


            with h5py.File(copy_file_path, 'a') as file:
                # access the existing first-level subgroup delay group
                delay_group = file['delay']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = delay_group['shell' + str(sh2_index + 1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=constellation_copy_delay)

        # create the satellite position matrix of the constellation_copy constellation and write the h5 file
        for t in range(1, (int)(sh.orbit_cycle / dT) + 3, 1):
            # this list is used to store the position information of all satellites in the current shell.
            # It is a two-dimensional list. Each element is a one-dimensional list. Each one-dimensional list
            # contains three elements, which respectively represent the longitude, latitude and altitude of a satellite.
            satellite_position = []
            for sat in sh2.satellites:
                satellite_position.append(
                    [str(sat.longitude[t - 1]), str(sat.latitude[t - 1]), str(sat.altitude[t - 1])])

            with h5py.File(copy_file_path, 'a') as file:
                # access the existing first-level subgroup position group
                position_group = file['position']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = position_group['shell' + str(sh2_index + 1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=satellite_position)

    # returns the damaged constellation after generation
    return constellation_copy
