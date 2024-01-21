'''

Author : yunanhou

Date : 2023/10/14

Function : Calculate the betweeness value of each satellite in a satellite constellation shell

'''
import networkx as nx
import h5py
import numpy as np

# Parameters:
# constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
# sh : a shell class object, representing a shell in the constellation
# t : a certain time slot (timeslot)
def betweeness(constellation_name , sh , t=1):
    file_path = "data/XML_constellation/" + constellation_name + ".h5"  # h5 file path and name
    # read the delay matrix of the shell layer of the constellation constellation at time t
    with h5py.File(file_path, 'r') as file:
        # access the existing first-level subgroup delay group
        delay_group = file['delay']
        # access the existing secondary subgroup 'shell'+str(count) subgroup
        current_shell_group = delay_group[sh.shell_name]
        # read the data set
        delay = np.array(current_shell_group['timeslot' + str(t)]).tolist()

    G = nx.Graph()  # create an undirected graph object named G, which is empty at first, with no nodes and edges.
    satellite_nodes = []
    for i in range(1, len(delay), 1):
        satellite_nodes.append("satellite_" + str(i))
    G.add_nodes_from(satellite_nodes)  # add nodes to an undirected graph

    satellite_edges = []
    for i in range(1, len(delay), 1):
        for j in range(i + 1, len(delay), 1):
            if delay[i][j] > 0:
                satellite_edges.append(("satellite_" + str(i), "satellite_" + str(j), delay[i][j]))
    # add an edge to an undirected graph. The weight of the edge is the value in the delay matrix.
    G.add_weighted_edges_from(satellite_edges)
    # calculate the betweenness centrality value of each satellite
    score = nx.betweenness_centrality(G)
    bet = []
    for item in score.keys():
        bet.append(score[item])
    return bet