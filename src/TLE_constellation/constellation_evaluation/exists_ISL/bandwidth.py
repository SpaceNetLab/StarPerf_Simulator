'''

Author: yunanhou

Date: 2023/12/14

Function : This script is used to calculate the bandwidth between two users

Implementation idea: First, pass in a shell in a constellation, as well as two user objects source and target,
                     pass in a parameter λ, and then calculate the bandwidth between the source and target. Among them,
                     the calculation of the bandwidth value refers to the comprehensive bandwidth of all paths from the
                     source to the target whose delay time does not exceed λ times the shortest delay time. λ is a
                     floating point number not less than 1 (that is, the minimum value of λ is 1).

'''
import h5py
import numpy as np
from math import radians, cos, sin, asin, sqrt
import networkx as nx


# Calculate the distance between the ground station and a satellite (the calculation results take into account the
# curvature of the earth), the unit of the return value is kilometers
def distance_between_satellite_and_user(groundstation , satellite , t):
    longitude1 = groundstation.longitude
    latitude1 = groundstation.latitude
    longitude2 = satellite.longitude[t-1]
    latitude2 = satellite.latitude[t-1]
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



# Parameters:
# constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
# source : the source end, target : the target end. Both parameters are user class objects.
# sh : a shell class object, representing a shell in the constellation
# λ : the maximum multiple of the minimum delay time allowed from source to target. The smaller the λ value, the fewer
#    the number of paths from source to target. When λ=1, only one path meets the requirements (i.e. the shortest path).
# isl_capacity : the capacity of a single ISL, such as 5Gbps, etc.
# dT : how often a timeslot is recorded
def bandwidth(constellation_name , source , target ,sh, λ , isl_capacity , dT):
    file_path = "data/TLE_constellation/" + constellation_name + ".h5"  # h5 file path and name
    # list variable, used to store the number of paths that meet the requirements in each timeslot
    path_num_per_timeslot = [0 for i in range((int)(sh.orbit_cycle / dT) + 2)]

    for t in range(1, (int)(sh.orbit_cycle / dT) + 3, 1):
        # read the delay matrix of the shell layer of the constellation constellation at time t
        with h5py.File(file_path, 'r') as file:
            # access the existing first-level subgroup delay group
            delay_group = file['delay']
            # access the existing secondary subgroup 'shell'+str(count) subgroup
            current_shell_group = delay_group[sh.shell_name]
            # read the data set
            delay = np.array(current_shell_group['timeslot' + str(t)]).tolist()
        # find the satellite closest to the source user
        # the satellite closest to the source user
        nearest_satellite_to_source_groundstation = None
        # initialize the nearest distance to the source user to be infinite
        satellite_to_source_groundstation_distance = float('inf')
        # the satellite closest to the target user
        nearest_satellite_to_target_groundstation = None
        # initialize the nearest distance to the target user to be infinite
        satellite_to_target_groundstation_distance = float('inf')
        # traverse each satellite in the sh layer shell
        for satellite in sh.satellites:
            # calculate the distance between the currently traversed satellite and the source user
            dis1 = distance_between_satellite_and_user(source, satellite, t)
            # calculate the distance between the currently traversed satellite and the target user
            dis2 = distance_between_satellite_and_user(target, satellite, t)
            if dis1 < satellite_to_source_groundstation_distance:
                satellite_to_source_groundstation_distance = dis1
                nearest_satellite_to_source_groundstation = satellite
            if dis2 < satellite_to_target_groundstation_distance:
                satellite_to_target_groundstation_distance = dis2
                nearest_satellite_to_target_groundstation = satellite


        # after the above for loop ends, the variable nearest_satellite_to_source_groundstation represents the satellite
        # closest to the source ground station, and the variable nearest_satellite_to_target_groundstation represents
        # the satellite closest to the target ground station.

        G = nx.Graph()  # create an undirected graph object named G, which is empty at first, with no nodes and edges.
        satellite_nodes = []
        for i in range(1, len(delay), 1):
            satellite_nodes.append("satellite_" + str(i))
        G.add_nodes_from(satellite_nodes)  # add nodes to an undirected graph

        satellite_edges = []
        edge_weights = []
        for i in range(1, len(delay), 1):
            for j in range(i + 1, len(delay), 1):
                if delay[i][j] > 0:
                    satellite_edges.append(("satellite_" + str(i), "satellite_" + str(j), delay[i][j]))
                    edge_weights.append(delay[i][j])

        # add an edge to an undirected graph. The weight of the edge is the value in the delay matrix.
        G.add_weighted_edges_from(satellite_edges)
        # the number of the starting routing satellite
        start_satellite = "satellite_" + str(nearest_satellite_to_source_groundstation.id)
        # the number of the terminating routing satellite
        end_satellite = "satellite_" + str(nearest_satellite_to_target_groundstation.id)

        # find the delay time (seconds) corresponding to the shortest path
        minimum_delay_time = nx.dijkstra_path_length(G, source=start_satellite, target=end_satellite)
        # count the number of paths from source to target
        path_num = 0
        while nx.has_path(G, source=start_satellite, target=end_satellite):
            cur_shortet = nx.dijkstra_path_length(G, source=start_satellite, target=end_satellite)
            if cur_shortet > minimum_delay_time * λ:
                break
            path = nx.dijkstra_path(G, source=start_satellite, target=end_satellite)
            path_num = path_num + 1
            for x in range(1, len(path) - 2):
                G.remove_edge(path[x], path[x + 1])
        path_num_per_timeslot[t - 1] = path_num

    # computational bandwidth
    sum = 0.
    for num in path_num_per_timeslot:
        sum = sum + num * isl_capacity
    if sum == 0:
        avg_bandwidth = -1  # returning -1 indicates that there is no feasible path from source to target.
    else:
        avg_bandwidth = sum / len(path_num_per_timeslot)

    return avg_bandwidth





