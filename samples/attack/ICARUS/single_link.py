"""
Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test single link ICARUS attack and get the results

"""


from src.constellation_generation.by_duration.constellation_configuration import constellation_configuration
import src.XML_constellation.constellation_attack.attack_plugin_manager as attack_plugin_manager
import numpy as np


def gather_delay(cons_name, src_lat, src_lon, dst_lat, dst_lon, link_num, rate, duration):
    ori_delay = []
    load_delay = []
    file_path = "data/" + cons_name + "_icarus/single_link_attack/" + str(link_num * rate) + "_" + str(src_lat) \
                + "_" + str(src_lon) + "_" + str(dst_lat) + "_" + str(dst_lon)

    for t in range(1, duration + 1):
        path = file_path + "/" + str(t)
        ori = np.loadtxt(path + '/ori_delay.txt')
        ori = float(ori)
        if ori > 1:
            ori = 1
        ori_delay.append(ori)

        load = np.loadtxt(path + '/load_delay.txt')
        load = float(load)
        if load > 1:
            load = 1
        load_delay.append(load)

    ori_delay = np.array(ori_delay)
    np.savetxt(file_path + '/attack_delays.txt', ori_delay, fmt='%.3f')

    load_delay = np.array(load_delay)
    np.savetxt(file_path + '/load_delays.txt', load_delay, fmt='%.3f')


def gather_throughput(cons_name, src_lat, src_lon, dst_lat, dst_lon, link_num, rate, duration, capacity):
    ori_traffics = []
    attack_traffics = []
    load_traffics = []
    attack_left_traffics = []
    load_left_traffics = []
    file_path = "data/" + cons_name + "_icarus/single_link_attack/" + str(link_num * rate) + "_" + str(src_lat) \
                + "_" + str(src_lon) + "_" + str(dst_lat) + "_" + str(dst_lon)

    for t in range(1, duration + 1):
        path = file_path + "/" + str(t)

        ori_traffic = np.loadtxt(path + '/origin_path_traffic.txt')
        ori_traffic = list(map(int, ori_traffic))
        ori_traffic = ori_traffic[1:-1]
        max_traffic = max(ori_traffic)
        ori_traffics.append(max_traffic)

        attack_traffic = np.loadtxt(path + '/attack_path_traffic.txt')
        attack_traffic = list(map(int, attack_traffic))
        attack_traffic = attack_traffic[1:-1]
        max_traffic = max(attack_traffic)
        if max_traffic >= capacity:
            max_traffic = capacity
        attack_traffics.append(max_traffic)
        attack_left_traffics.append(capacity - max_traffic)

        load_traffic = np.loadtxt(path + '/load_path_traffic.txt')
        load_traffic = list(map(int, load_traffic))
        load_traffic = load_traffic[1:-1]
        max_traffic = max(load_traffic)
        if max_traffic >= capacity:
            max_traffic = capacity
        load_traffics.append(max_traffic)
        load_left_traffics.append(capacity - max_traffic)

    ori_traffics = np.array(ori_traffics)
    np.savetxt(file_path + '/origin_traffics.txt', ori_traffics, fmt='%d')
    attack_traffics = np.array(attack_traffics)
    np.savetxt(file_path + '/attack_traffics.txt', attack_traffics, fmt='%d')
    load_traffics = np.array(load_traffics)
    np.savetxt(file_path + '/load_traffics.txt', load_traffics, fmt='%d')
    attack_left_traffics = np.array(attack_left_traffics)
    np.savetxt(file_path + '/attack_left_traffics.txt', attack_left_traffics, fmt='%d')
    load_left_traffics = np.array(load_left_traffics)
    np.savetxt(file_path + '/load_left_traffics.txt', load_left_traffics, fmt='%d')


def single_link_attack():
    duration = 200
    dT = 1
    constellation = constellation_configuration(duration, dT, "Starlink")

    attackPluginManage = attack_plugin_manager.attack_plugin_manager()
    attackPluginManage.set_attack_model('icarus_single_link_attack')

    times = [0, 100, 200, 300, 400, 500, 512, 550, 600]
    for time in times:
        for t in range(1, 201):
            attackPluginManage.execute_single_link_attack(constellation, t, 35.7, 139.7, 22.3, 114.2, time, 40)    # Tokyo to Hong Kong
            attackPluginManage.execute_single_link_attack(constellation, t, 39.9, 116.4, 41.9, 12.5, time, 40)     # Beijing to Rome
            attackPluginManage.execute_single_link_attack(constellation, t, 40.7, -74.0, -22.9, -43.2, time, 40)   # New Tork to Rio de Janeiro
            attackPluginManage.execute_single_link_attack(constellation, t, 48.9, 2.4, 40.4, -3.7, time, 40)       # paris to madrid
            attackPluginManage.execute_single_link_attack(constellation, t, -33.9, 151.2, 37.6, 126.9, time, 40)       # Sydney to Seoul

    for num in times:
        gather_delay("Starlink", 35.7, 139.7, 22.3, 114.2, num, 40, 200)
        gather_delay("Starlink", 39.9, 116.4, 41.9, 12.5, num, 40, 200)
        gather_delay("Starlink", 40.7, -74.0, -22.9, -43.2, num, 40, 200)
        gather_delay("Starlink", 48.9, 2.4, 40.4, -3.7, num, 40, 200)
        gather_delay("Starlink", -33.9, 151.2, 37.6, 126.9, num, 40, 200)
        gather_throughput("Starlink", 35.7, 139.7, 22.3, 114.2, num, 40, 200, 20480)
        gather_throughput("Starlink", 39.9, 116.4, 41.9, 12.5, num, 40, 200, 20480)
        gather_throughput("Starlink", 40.7, -74.0, -22.9, -43.2, num, 40, 200, 20480)
        gather_throughput("Starlink", 48.9, 2.4, 40.4, -3.7, num, 40, 200, 20480)
        gather_throughput("Starlink", -33.9, 151.2, 37.6, 126.9, num, 40, 200, 20480)



if __name__ == '__main__':
    single_link_attack()
