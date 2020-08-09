import networkx as nx
import numpy as np
import random
import scipy.io as scio


def dij_delay(constellation_name, satellite_num, cycle, bound, elevation, depression, error_rate, dT):
    R = 6371 * 1000
    city_num = 4
    dl = [[0 for i in range((cycle - 1) / dT + 1)] for i in range(6)]
    path = 'matlab_code\\' + constellation_name + '\\position.mat'
    data = scio.loadmat(path)
    central_angle = 180 - 2 * (depression + elevation)
    cos_central_angle = np.cos(central_angle * np.pi / 180)
    position_xyz = data['position_cbf']
    position = data['position']
    error = [0 for i in range(6)]
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
        if error_rate > 0:
            for i in range(satellite_num):
                destroy = random.randint(1, int(100 / error_rate))
                if destroy == 1:
                    G.remove_node(i)
        count = 0
        for i in range(satellite_num, satellite_num + city_num - 1):  # city to city
            for j in range(i + 1, satellite_num + city_num):
                if nx.has_path(G, source=i, target=j):
                    dl[count][(time - 1) / dT] = nx.dijkstra_path_length(G, source=i, target=j)
                else:  # GSL is broken down
                    error[count] += 1
                    dl[count][(time - 1) / dT] = 0.
                count += 1

    avg_delay = [0 for i in range(6)]
    for i in range(6):
        sum = 0.
        for j in range((cycle - 1) / dT + 1):
            sum += dl[i][j]
        avg_delay[i] = sum / ((cycle - 1) / dT + 1 - error[i])
    print(avg_delay)

