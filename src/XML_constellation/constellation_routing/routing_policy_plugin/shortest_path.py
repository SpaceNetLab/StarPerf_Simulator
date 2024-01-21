'''

Author : yunanhou

Date : 2023/08/24

Function : Use the shortest path algorithm to calculate the path from source to destination target

'''
import numpy as np
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import h5py


# Function : calculate the distance between the ground station and a satellite (the calculation results take into
#            account the curvature of the earth), the unit of the return value is kilometers
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



# Parameters :
# constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
# source : the source ground station
# target : the target ground station
# t : a certain time slot (timeslot)
# sh : a shell class object, representing a shell in the constellation
def shortest_path(constellation_name , source , target , sh , t):
    file_path = "data/XML_constellation/" + constellation_name + ".h5"  # h5 file path and name
    # read the delay matrix of the shell layer of the constellation constellation at time t
    with h5py.File(file_path, 'r') as file:
        # access the existing first-level subgroup delay group
        delay_group = file['delay']
        # access the existing secondary subgroup 'shell'+str(count) subgroup
        current_shell_group = delay_group[sh.shell_name]
        # read the data set
        delay = np.array(current_shell_group['timeslot' + str(t)]).tolist()
    # find the satellite closest to the source ground station
    # the satellite closest to the source ground station
    nearest_satellite_to_source_groundstation = None
    # initialize the nearest distance to the source base station to be infinite
    satellite_to_source_groundstation_distance = float('inf')
    # the satellite closest to the target ground station
    nearest_satellite_to_target_groundstation = None
    # initialize the nearest distance to the target base station to be infinite
    satellite_to_target_groundstation_distance = float('inf')
    # traverse each satellite in the sh layer shell
    for orbit in sh.orbits:
        for satellite in orbit.satellites:
            # calculate the distance between the currently traversed satellite and the source ground station
            dis1 = distance_between_satellite_and_user(source, satellite, t)
            # calculate the distance between the currently traversed satellite and the target ground station
            dis2 = distance_between_satellite_and_user(target, satellite, t)
            if dis1 < satellite_to_source_groundstation_distance:
                satellite_to_source_groundstation_distance = dis1
                nearest_satellite_to_source_groundstation = satellite
            if dis2 < satellite_to_target_groundstation_distance:
                satellite_to_target_groundstation_distance = dis2
                nearest_satellite_to_target_groundstation = satellite

    # after the above for loop ends, the variable nearest_satellite_to_source_groundstation represents the satellite
    # closest to the source ground station, and the variable nearest_satellite_to_target_groundstation represents the
    # satellite closest to the target ground station.

    # create an graph object named G, which is empty at first, with no nodes and edges.
    G = nx.Graph()
    satellite_nodes = []
    for i in range(1, len(delay), 1):
        satellite_nodes.append("satellite_" + str(i))
    G.add_nodes_from(satellite_nodes)  # add nodes to graph

    satellite_edges = []
    edge_weights = []
    for i in range(1, len(delay), 1):
        for j in range(i + 1, len(delay), 1):
            if delay[i][j] > 0:
                satellite_edges.append(("satellite_" + str(i), "satellite_" + str(j), delay[i][j]))
                edge_weights.append(delay[i][j])
    # add an edge to an graph. The weight of the edge is the value in the delay matrix.
    G.add_weighted_edges_from(satellite_edges)

    # the number of the starting routing satellite
    start_satellite = "satellite_" + str(nearest_satellite_to_source_groundstation.id)
    # the number of the terminating routing satellite
    end_satellite = "satellite_" + str(nearest_satellite_to_target_groundstation.id)

    # find the shortest path
    minimum_path = nx.dijkstra_path(G, source=start_satellite, target=end_satellite)

    return minimum_path
