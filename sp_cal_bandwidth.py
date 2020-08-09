import copy
import scipy.io as scio
import networkx as nx


def bandwidth(parameter, dT):
    constellation_num = len(parameter[0])
    for constellation_index in range(constellation_num):
        constellation_name = parameter[0][constellation_index]
        satellite_num = int(parameter[1][constellation_index])
        cycle = int(parameter[2][constellation_index])
        bound = parameter[5][constellation_index]
        city_num = 4
        # labellist = ['BJ-NY','BJ-LD','BJ-SN','NY-LD','NY-SN','LD-SN']
        path_num = [[0 for i in range((cycle - 1) / dT + 1)] for i in range(6)]
        for time in range(1, cycle + 1, dT):
            edge = []
            G = nx.Graph()
            path = constellation_name + '\\delay\\' + str(time) + '.mat'
            data = scio.loadmat(path)
            delay = data['delay']
            G.add_nodes_from(range(satellite_num + city_num))
            for i in range(satellite_num):
                for j in range(i + 1, satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i, j, delay[i][j]))
                for j in range(satellite_num, satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i, j, delay[i][j]))
            G.add_weighted_edges_from(edge)
            count = 0
            for i in range(satellite_num, satellite_num + city_num - 1):
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

