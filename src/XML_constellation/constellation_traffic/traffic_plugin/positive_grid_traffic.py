"""
Author : zhifenghan

Date : 2025/05/09

Function : This function generates realistic network traffic for satellite constellations using the
           +Grid connectivity model. It simulates geographic user distribution, satellite-to-ground
           connections, inter-satellite routing, and traffic flow allocation based on population
           density to create a comprehensive traffic model for constellation simulations.
"""

import math
import sys
import numpy as np
import random
import json
import os
import h5py

RADIUS = 6371
Flow_size = 0.5

cons_name = ""
altitude = 0
num_of_orbit = 0
sat_of_orbit = 0
inclination = 0

sat_num = num_of_orbit * sat_of_orbit
user_num = inclination * 2 * 360
sat_pos_car = []  # 1584 satellites' positions
user_pos_car = []  # inclination * 2 * 360 blocks' positions (from high-latitude to low-latitude and high-longitude to low-longitude areas)
GS_pos_car = []  # GS positions
pop_count = []  # 53 ~ -53, traffic probability per block
user_connect_sat = []  # satellite connected to each block 
sat_connect_gs = []  # GS connected to each satellite 
gsl_occurrence = [] # blocks served by each GSL 
gsl_occurrence_num = [] # number of blocks served by each GSL 
path = []  # path[i][j] = k: k is the next hop from i to j; k == j shows that k/j is a landing satellite connected to a GS
link_utilization_ratio = 100
isl_capacity = 20480 
uplink_capacity = downlink_capacity = 4096
bandwidth_isl = isl_capacity * link_utilization_ratio / 100
bandwidth_uplink = uplink_capacity * link_utilization_ratio / 100
bandwidth_downlink = uplink_capacity * link_utilization_ratio / 100
link_traffic = []  # 6 links in total for a satellite, including 4 ISLs, one downlink (6*i+2), and one uplink (6*i+3)
isl_traffic = []  # egress traffic per satellite
isl_sender_traffic = [] # ISL sending traffic of a certain satellite
isl_receiver_traffic = [] # ISL receiving traffic of a certain satellite
downlink_traffic = []  # downlink traffic per satellite
uplink_traffic = [] # uplink traffic per satellite
sat_cover_pop = [] # total user traffic accessed by a satellite
sat_cover_user = []  
flows = []  # all the candidate flows. flow[k] = [src_sat, dst_sat, weight]. 
flows_selected = {}  # legal background flows according to the probability. {(src_sat,dst,sat):bandwidth,...} 
flows_num = 0
flows_cumulate_weight = []
flows_sum_weight = 0


def cir_to_car_np(lat, lng, h):
    x = (RADIUS + h) * math.cos(math.radians(lat)) * math.cos(
        math.radians(lng))
    y = (RADIUS + h) * math.cos(math.radians(lat)) * math.sin(
        math.radians(lng))
    z = (RADIUS + h) * math.sin(math.radians(lat))
    return np.array([x, y, z])


def link_seq(sati, satj): 
    orbiti = int(sati / sat_of_orbit)
    orbitj = int(satj / sat_of_orbit)
    if orbiti == orbitj and (satj == sati + 1 or satj == sati -
                             (sat_of_orbit - 1)):
        return sati * 6
    elif satj == (sati + sat_of_orbit) % sat_num:
        return sati * 6 + 1
    elif orbiti == orbitj and (satj == sati - 1 or satj == sati +
                               (sat_of_orbit - 1)):
        return sati * 6 + 2
    elif satj == (sati - sat_of_orbit + sat_num) % sat_num:
        return sati * 6 + 3
    else:
        return -1


def floyd(): # calculate the next hop from A to B
    global path
    global gsl_occurrence
    global sat_cover_user
    # inter-orbit first, then intra-orbit
    for orbit_id in range(num_of_orbit):
        for sat_id in range(sat_of_orbit):
            next_sat, sat_index = find_next_sat(
                orbit_id, sat_id, sat_of_orbit,
                sat_connect_gs)  # the nearest landing satellite (-1: no landing satellite)
            path[sat_index] = next_sat  # -1: no more landing satellite. Land from this satellite
    for orbit_id in range(num_of_orbit):
        for sat_id in range(sat_of_orbit):
            landing_sat = path[orbit_id * sat_of_orbit + sat_id]
            while landing_sat != path[landing_sat]:
                landing_sat = path[landing_sat]
            for item in sat_cover_user[orbit_id * sat_of_orbit + sat_id]:
                gsl_occurrence[landing_sat].append(item)


def find_next_sat(orbit_id, sat_id, sat_of_orbit,
                  sat_connect_gs):  # the the next satellite (-1: no landing satellite)
    next_sat = -1
    min_hops = int(sat_of_orbit / 2) + int(num_of_orbit / 2)
    sat_index = orbit_id * sat_of_orbit + sat_id
    if sat_connect_gs[sat_index] != -1:
        return sat_index, sat_index
    for item in range(sat_num):
        if sat_connect_gs[item] != -1:
            item_orbit = int(item / sat_of_orbit)
            item_sat = item % sat_of_orbit
            orbit_diff = abs(item_orbit -
                             orbit_id) if abs(item_orbit - orbit_id) <= int(
                                 num_of_orbit /
                                 2) else num_of_orbit - abs(item_orbit -
                                                            orbit_id)
            sat_diff = abs(item_sat - sat_id) if abs(item_sat - sat_id) <= int(
                sat_of_orbit / 2) else sat_of_orbit - abs(item_sat - sat_id)
            if (sat_diff + orbit_diff) >= min_hops:
                continue

            min_hops = (sat_diff + orbit_diff)
            if item_orbit == orbit_id:  # same orbit
                if item_sat > sat_id:
                    if (item_sat - sat_id) <= (sat_of_orbit -
                                               (item_sat - sat_id)):
                        next_sat = sat_index + 1
                    elif sat_id == 0:
                        next_sat = sat_index + sat_of_orbit - 1
                    else:
                        next_sat = sat_index - 1
                else:
                    if (sat_id - item_sat) <= (sat_of_orbit -
                                               (sat_id - item_sat)):
                        next_sat = sat_index - 1
                    elif sat_id == sat_of_orbit - 1:
                        next_sat = sat_index - sat_of_orbit + 1
                    else:
                        next_sat = sat_index + 1
            else:  # not same orbit
                if item_orbit > orbit_id:
                    if (item_orbit - orbit_id) <= (num_of_orbit -
                                                   (item_orbit - orbit_id)):
                        next_sat = sat_index + sat_of_orbit
                    elif orbit_id == 0:
                        next_sat = sat_index + sat_of_orbit * (num_of_orbit -
                                                               1)
                    else:
                        next_sat = sat_index - sat_of_orbit
                else:
                    if (orbit_id - item_orbit) <= (num_of_orbit -
                                                   (orbit_id - item_orbit)):
                        next_sat = sat_index - sat_of_orbit
                    elif orbit_id == num_of_orbit - 1:
                        next_sat = sat_index - sat_of_orbit * (num_of_orbit -
                                                               1)
                    else:
                        next_sat = sat_index + sat_of_orbit

    return next_sat, sat_index


def init_flows():  # initiate flows and weights
    global flows
    global flows_sum_weight
    global flows_cumulate_weight
    global flows_num
    for block in range(inclination * 2 * 360):
        if pop_count[block] == 0:
            continue
        weight = math.ceil(pop_count[block]) 
        flows.append([block, weight])
        flows_sum_weight += weight
        flows_cumulate_weight.append(flows_sum_weight)  # weight for each link
    flows_num = len(flows_cumulate_weight)


def get_one_flow(
        cumulate_weight, num,
        sum_weight):  # randomly choose one
    rand = random.randint(1, sum_weight)
    low = 0
    high = num - 1
    while low < high:
        mid = (low + high) >> 1
        if rand > cumulate_weight[mid]:
            low = mid + 1
        elif rand < cumulate_weight[mid]:
            high = mid
        else:
            return mid
    return low


def add_flow(src_block, rate=Flow_size):  
    global link_traffic
    src_sat = user_connect_sat[src_block]
    if src_sat == -1:
        return -1
    # traverse all the paths to update link_traffic
    uplink = src_sat * 6 + 5
    # determine whether the constraints are met
    from_sat = src_sat
    if path[from_sat] == -1:
        return 0
    while True:
        to_sat = path[from_sat]
        if to_sat != from_sat:
            link_id_1 = link_seq(from_sat, to_sat)
            if link_id_1 == -1:
                print('error!')
                print(from_sat, to_sat)
                exit(0)
            link_traffic[link_id_1] += rate
            if link_id_1 % 6 == 0:
                isl_traffic[from_sat] += rate  # isl_traffic for dual-traffic 
                isl_sender_traffic[from_sat] += rate
            elif link_id_1 % 6 == 1:
                isl_traffic[to_sat] += rate  # isl_traffic for dual-traffic 
                isl_receiver_traffic[to_sat] += rate
            from_sat = to_sat
        else:
            break
    downlink = from_sat * 6 + 4
    link_traffic[uplink] += rate
    link_traffic[downlink] += rate
    uplink_traffic[src_sat] += rate
    downlink_traffic[from_sat] += rate

    if downlink_traffic[from_sat] < downlink_capacity:
        # not enough traffic
        return 0
    else:  # minus extra traffic if overloaded
        src_sat = user_connect_sat[src_block]
        # traverse all the paths to update link_traffic
        uplink = src_sat * 6 + 5
        # determine whether the constraints are met
        from_sat = src_sat
        while True:
            to_sat = path[from_sat]
            if to_sat != from_sat:
                link_id_1 = link_seq(from_sat, to_sat)
                if link_id_1 == -1:
                    print('error!')
                    print(from_sat, to_sat)
                    exit(0)
                link_traffic[link_id_1] -= rate
                if link_id_1 % 6 == 0:
                    isl_traffic[from_sat] -= rate  # isl_traffic for dual-traffic 
                    isl_sender_traffic[from_sat] -= rate
                elif link_id_1 % 6 == 1:
                    isl_traffic[to_sat] -= rate  # isl_traffic for dual-traffic 
                    isl_receiver_traffic[to_sat] -= rate
                from_sat = to_sat
            else:
                break
        downlink = from_sat * 6 + 4
        link_traffic[uplink] -= rate
        link_traffic[downlink] -= rate
        uplink_traffic[src_sat] -= rate
        downlink_traffic[from_sat] -= rate
        return -1


def positive_grid_traffic(constellation, time_slot, 
                          minimum_elevation=25, isl=20480,
                          uplink=4096, downlink=4096,
                          ratio=0.5, flow_size=0.5):
    """
    Parameters:
    - constellation: The constellation object containing satellite network parameters
    - time_slot: Current time slot for which to generate traffic
    - minimum_elevation: Minimum elevation angle in degrees for establishing connections (default: 25)
    - isl: Inter-Satellite Link capacity in Mbps (default: 20480)
    - uplink: Uplink capacity in Mbps (default: 4096)
    - downlink: Downlink capacity in Mbps (default: 4096)
    - ratio: Link utilization ratio as percentage (default: 0.5)
    - flow_size: Unit traffic flow size in MB (default: 0.5)

    Operation:
    1. Initializes constellation parameters and traffic structures
    2. Loads satellite positions from constellation data files
    3. Generates user positions based on global geographic grid
    4. Loads population density data for traffic distribution weighting
    5. Connects users to satellites based on closest satellite within visibility
    6. Connects satellites to ground stations based on proximity
    7. Computes routing paths using a modified Floyd-Warshall algorithm
    8. Creates traffic flows by:
       - Selecting source blocks based on population-weighted distribution
       - Computing paths from sources to destinations
       - Adding traffic to links along the path
       - Repeating until links reach saturation or flow limit
    9. Saves traffic data to output files

    Return:
    - None (Results are saved to files in the specified directory)

    Outputs:
    The function saves multiple files under the 'data/{constellation_name}_energy_drain/link_traffic_data/{time_slot}/' directory:
    - isl_traffic.txt: Combined ISL traffic per satellite
    - isl_sender_traffic.txt: ISL sending traffic per satellite
    - isl_receiver_traffic.txt: ISL receiving traffic per satellite
    - downlink_traffic.txt: Downlink traffic per satellite
    - uplink_traffic.txt: Uplink traffic per satellite
    - sat_connect_gs.txt: Ground station connections per satellite
    - user_connect_sat.txt: Satellite connections per user block
    - gsl_occurrence_num.txt: Number of user blocks served by each GSL
    - gs_occurrence_num.txt: Number of user blocks served by each ground station

    Notes:
    - Traffic is generated based on population density to create realistic patterns
    - The algorithm balances traffic across the network to achieve target utilization levels
    - Visibility constraints are enforced based on minimum elevation angle
    - The model accounts for both user-to-satellite and satellite-to-ground station connections
    """

    global cons_name, altitude, num_of_orbit, sat_of_orbit, inclination, sat_num, user_num
    global path, gsl_occurrence, gsl_occurrence_num, link_traffic, isl_traffic, downlink_traffic
    global uplink_traffic, sat_cover_pop, sat_cover_user, link_utilization_ratio
    global isl_capacity, uplink_capacity, downlink_capacity, bandwidth_isl
    global bandwidth_uplink, bandwidth_downlink, Flow_size
    global sat_pos_car, user_pos_car, GS_pos_car, pop_count
    global user_connect_sat, sat_connect_gs, flows, flows_selected
    global flows_cumulate_weight, flows_sum_weight, flows_num
    global isl_sender_traffic, isl_receiver_traffic


    cons_name = constellation.constellation_name
    shell = constellation.shells[0] # the first shell
    altitude = shell.altitude
    num_of_orbit = shell.number_of_orbits
    sat_of_orbit = shell.number_of_satellite_per_orbit
    inclination = shell.inclination

    sat_num = num_of_orbit * sat_of_orbit
    user_num = math.ceil(inclination) * 2 * 360

    path = [[-1 for i in range(sat_num)]
        for j in range(sat_num)]
    gsl_occurrence = [[] for i in range(sat_num)] 
    gsl_occurrence_num = [-1 for i in range(sat_num)] 
    link_traffic = [0] * sat_num * 6 
    isl_traffic = [0] * sat_num 
    downlink_traffic = [0] * sat_num 
    uplink_traffic = [0] * sat_num 
    sat_cover_pop = [0] * sat_num 
    sat_cover_user = [[] for i in range(sat_num)]  
    isl_sender_traffic = [0] * sat_num
    isl_receiver_traffic = [0] * sat_num

    link_utilization_ratio = ratio
    isl_capacity = isl
    uplink_capacity = uplink
    downlink_capacity = downlink
    bandwidth_isl = isl_capacity * link_utilization_ratio / 100
    bandwidth_uplink = uplink_capacity * link_utilization_ratio / 100
    bandwidth_downlink = uplink_capacity * link_utilization_ratio / 100

    sat_pos_car = []  # 1584 satellites' positions
    user_pos_car = []  # inclination * 2 * 360 blocks' positions (from high-latitude to low-latitude and high-longitude to low-longitude areas)
    GS_pos_car = []  # GS positions
    pop_count = []  # 53 ~ -53, traffic probability per block
    user_connect_sat = []  # satellite connected to each block 
    sat_connect_gs = []  # GS connected to each satellite 
    flows = []  # all the candidate flows. flow[k] = [src_sat, dst_sat, weight]. 
    flows_selected = {}  # legal background flows according to the probability. {(src_sat,dst,sat):bandwidth,...} 
    flows_num = 0
    flows_cumulate_weight = []
    flows_sum_weight = 0

    minimum_elevation = math.radians(minimum_elevation)
    bound = math.sqrt((RADIUS + altitude)**2 - (RADIUS * math.cos(minimum_elevation))**2) - RADIUS * math.sin(minimum_elevation)
    Flow_size = flow_size

    # load satellite positions
    h5file_path = os.path.join("data", "XML_constellation", "Starlink_shell1.h5")
    with h5py.File(h5file_path, 'r') as file:
        position_group = file['position']
        shell_group = position_group['shell1']
        position_tt = np.array(shell_group['timeslot' + str(time_slot)])
        for lla in position_tt:
            sat_pos_car.append(
                cir_to_car_np(
                    float(lla[1]), float(lla[0]), float(lla[2])))
        sat_pos_car = np.array(sat_pos_car)
    
    inclination = math.ceil(inclination)
    # load user positions
    for lat in range(inclination, -inclination, -1):  # [inclination, -inclination]
        for lon in range(-180, 180, 1):  # [-179.5,179.5]
            user_pos_car.append(cir_to_car_np(lat - 0.5, lon + 0.5, 0))
    user_pos_car = np.array(user_pos_car)

    # load traffic distribution
    traffic_file = os.path.join("data", "starlink_count.txt")
    with open(traffic_file, 'r') as file:
        lines = file.readlines()
        for row in range(90 - inclination, 90 + inclination):
            pop_count.extend([float(x) for x in lines[row].split(' ')[:-1]] + [0])

    print("generating +Grid traffic for timeslot: " + str(time_slot) + "...")  

    # the satellite each block is connected to
    for user_id in range(inclination * 2 * 360):
        # determining the satellite each user is connected to 
        dis2 = np.sqrt(
            np.sum(np.square(sat_pos_car - user_pos_car[user_id]),
                   axis=1)) 
        if min(dis2) > bound:
            user_connect_sat.append(-1) 
            continue
        min_dis_sat = np.argmin(dis2) 
        user_connect_sat.append(
            min_dis_sat) 
        if pop_count[user_id] > 0:
            sat_cover_pop[min_dis_sat] += pop_count[user_id] 
            sat_cover_user[min_dis_sat].append(user_id)  

    # load GS positions
    f = open(os.path.join("data", "GS.json"), "r", encoding='utf8')
    GS_info = json.load(f)
    count = 0
    for key in GS_info:
        GS_pos_car.append(
            cir_to_car_np(float(GS_info[key]['lat']),
                          float(GS_info[key]['lng']), 0))
        count = count + 1
    GS_pos_car = np.array(GS_pos_car)

    # the GS a satellite is connected to
    for sat_id in range(sat_num):
        dis2 = np.sqrt(
            np.sum(np.square(GS_pos_car - sat_pos_car[sat_id]),
                   axis=1))  
        if min(dis2) > bound:
            sat_connect_gs.append(-1)  # -1 for no connection
            continue
        min_dis_sat = np.argmin(dis2)  
        sat_connect_gs.append(min_dis_sat) 

    # initiate topology and routing
    floyd() 

    # initiate traffic flows and weights
    init_flows() 

    for add_flow_times in range(2000000):  # randomly choose 2000000 flows
        flow_id = get_one_flow(flows_cumulate_weight, flows_num,
                                flows_sum_weight)
        res = add_flow(flows[flow_id][0], Flow_size)
        if res == -1:
            continue
        # add a new flow
        flow_pair = (flows[flow_id][0], flows[flow_id][1])
        if flow_pair in flows_selected:
            flows_selected[flow_pair] += Flow_size  
        else:
            flows_selected[flow_pair] = Flow_size

    # outputs: ISL, GSL down/uplink, block connecstions, satellite connections and so on
    # output_path = "data/" + cons_name + "_link_traffic_data/" + str(time_slot)
    output_path = os.path.join("data", cons_name + "_link_traffic_data", str(time_slot))
    os.makedirs(output_path, exist_ok=True)

    isl_traffic = np.array(isl_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, 'isl_traffic.txt'), isl_traffic, fmt='%d')

    isl_sender_traffic = np.array(isl_sender_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, 'isl_sender_traffic.txt'), isl_sender_traffic, fmt='%d')

    isl_receiver_traffic = np.array(isl_receiver_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, 'isl_receiver_traffic.txt'), isl_receiver_traffic, fmt='%d')

    downlink_traffic = np.array(downlink_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, 'downlink_traffic.txt'), downlink_traffic, fmt='%d')

    uplink_traffic = np.array(uplink_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, 'uplink_traffic.txt'), uplink_traffic, fmt='%d')

    sat_connect_gs = np.array(sat_connect_gs, dtype=int)
    np.savetxt(os.path.join(output_path, 'sat_connect_gs.txt'), sat_connect_gs, fmt='%d')

    user_connect_sat = np.array(user_connect_sat, dtype=int)
    np.savetxt(os.path.join(output_path, 'user_connect_sat.txt'), user_connect_sat, fmt='%d')

    id = 0
    gs_occurrence_num = [0 for _ in range(len(GS_pos_car))]
    for item in gsl_occurrence:
        gsl_occurrence_num[id] = len(item) if len(item) > 0 else -1
        if sat_connect_gs[id] != -1:
            gs_occurrence_num[sat_connect_gs[id]] += gsl_occurrence_num[id]
        id += 1

    gsl_occurrence_num = np.array(gsl_occurrence_num, dtype=int)
    np.savetxt(os.path.join(output_path, 'gsl_occurrence_num.txt'), gsl_occurrence_num, fmt='%d')

    gs_occurrence_num = np.array(gs_occurrence_num, dtype=int)
    np.savetxt(os.path.join(output_path, 'gs_occurrence_num.txt'), gs_occurrence_num, fmt='%d')

