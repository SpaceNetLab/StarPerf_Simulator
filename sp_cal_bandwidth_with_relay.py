import copy
import scipy.io as scio
import networkx as nx
import numpy as np


def bandwidth(constellation_name, satellite_num, cycle, bound, elevation, depression, dT):
    R = 6371 * 1000
    city_num = 4
    path = constellation_name + '\\position.mat'
    data = scio.loadmat(path)
    central_angle = 180 - 2 * (depression + elevation)
    cos_central_angle = np.cos(central_angle * np.pi / 180)
    position_xyz = data['position_cbf']
    position = data['position']
    path_num = [[0 for i in range((cycle - 1) / dT + 1)] for i in range(6)]
    for time in range(1, cycle + 1, dT):
        print(time)
        G = nx.Graph()
        edge = []
        path = 'matlab_code\\' + constellation_name + '\\delay\\' + str(time) + '.mat'
        data = scio.loadmat(path)
        delay = data['delay']
        G.add_nodes_from(range(satellite_num + city_num))
        for i in range(satellite_num):
            for j in range(i + 1, satellite_num):
                i_xyz = np.array(
                    [position_xyz[i][0][0][time - 1], position_xyz[i][0][1][time - 1], position_xyz[i][0][2][time - 1]])
                j_xyz = np.array(
                    [position_xyz[j][0][0][time - 1], position_xyz[j][0][1][time - 1], position_xyz[j][0][2][time - 1]])
                cos_angel = i_xyz.dot(j_xyz) / (np.sqrt(i_xyz.dot(i_xyz)) * np.sqrt(j_xyz.dot(j_xyz)))
                if cos_angel > cos_central_angle:
                    relay_latitude = (position[i][0][0][time - 1] + position[j][0][0][time - 1]) / 2
                    if position[i][0][1][time - 1] * position[j][0][1][time - 1] > 0:
                        relay_longitude = (position[i][0][1][time - 1] + position[j][0][1][time - 1]) / 2
                    else:
                        relay_longitude_over_0 = (position[i][0][1][time - 1] + position[j][0][1][time - 1]) / 2
                        delta_over_0 = np.abs(position[i][0][1][time - 1] - relay_longitude_over_0)
                        delta_over_180 = 180 - delta_over_0
                        if delta_over_0 < delta_over_180:
                            relay_longitude = relay_longitude_over_0
                        else:
                            if position[i][0][1][time - 1] > 0:
                                positive_longitude = position[i][0][1][time - 1]
                            else:
                                positive_longitude = position[j][0][1][time - 1]
                            if 180 - positive_longitude < delta_over_180:
                                relay_longitude = -180 + delta_over_180 - (180 - positive_longitude)
                            else:
                                relay_longitude = positive_longitude + delta_over_180
                    Theta = np.pi / 2 - relay_latitude * np.pi / 180
                    Phi = 2 * np.pi + relay_longitude * np.pi / 180
                    relay_x = (R * np.sin(Theta)) * np.cos(Phi)
                    relay_y = (R * np.sin(Theta)) * np.sin(Phi)
                    relay_z = R * np.cos(Theta)
                    relay_xyz = np.array([relay_x, relay_y, relay_z])
                    distance = np.linalg.norm(relay_xyz - i_xyz) + np.linalg.norm(relay_xyz - j_xyz)
                    edge.append((i, j, distance / (3 * 100000)))
            for j in range(satellite_num, satellite_num + city_num):
                if delay[i][j] < bound:
                    edge.append((i, j, delay[i][j]))
        G.add_weighted_edges_from(edge)
        count = 0
        for i in range(satellite_num, satellite_num + city_num - 1):  # city to city
            for j in range(i + 1, satellite_num + city_num):
                if nx.has_path(G, source=i, target=j):
                    shortest = nx.dijkstra_path_length(G, source=i, target=j)
                    tempG = copy.copy(G)
                    while nx.has_path(tempG, source=i, target=j):
                        cur_shortet = nx.dijkstra_path_length(tempG, source=i, target=j)
                        if cur_shortet > shortest * 1.1:
                            break
                        path = nx.dijkstra_path(tempG, source=i, target=j)
                        path_num[count][(time - 1) / dT] += 1
                        for x in range(1, len(path) - 2):
                            tempG.remove_edge(path[x], path[x + 1])
                count += 1

    avg_bandwidth = [0 for i in range(6)]
    for i in range(6):
        sum = 0.
        for j in range((cycle - 1) / dT + 1):
            sum += (path_num[i][j] * 5)
        if sum == 0:
            avg_bandwidth[i] = -1
        else:
            avg_bandwidth[i] = sum / ((cycle - 1) / dT + 1)
    print(avg_bandwidth)

