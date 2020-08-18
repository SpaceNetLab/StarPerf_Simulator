import networkx as nx
import scipy.io as scio


def betweenness(parameter):
    """Calculate the betweenness of mega-constellations
    :param parameter: two-dimensional list about parameter of constellations
    """
    constellation_num = len(parameter[0])
    for constellation_index in range(constellation_num):
        constellation_name = parameter[0][constellation_index]
        satellite_num = int(parameter[1][constellation_index])
        G = nx.Graph()
        path = 'matlab_code\\' + constellation_name + '\\delay\\1.mat'
        data = scio.loadmat(path)
        delay = data['delay']
        G.add_nodes_from(range(satellite_num))
        for i in range(satellite_num):
            for j in range(i + 1, satellite_num):
                if delay[i][j] > 0:
                    G.add_edge(i, j)
        score = nx.betweenness_centrality(G)
        bet = []
        for item in score.keys():
            bet.append(score[item])
        print(bet)

