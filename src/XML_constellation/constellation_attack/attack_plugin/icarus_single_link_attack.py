"""
Author : zhifenghan

Date : 2025/05/09

Function : This function implements an Icarus attack targeting a specific communication link
           between two points in a satellite constellation. The attack generates artificial
           traffic on carefully selected paths to cause congestion and degradation of service
           between the source and destination locations.

"""

import math
import numpy as np
import random
import os
import heapq
import h5py
from scipy.constants import c


sat1_id_in_orbit = 0
sat1_orbit_id = 0
sat2_id_in_orbit = 0
sat2_orbit_id = 0
RADIUS = 6371


def is_valid_sat_for_sat1(candidate_sat, sat_of_orbit, num_of_orbit, is_same_orbit_isl):
    """
    Determine whether a satellite meets the constraints of sat1

    Parameters:
    - candidate_sat: candidate satellite ID
    - sat_of_orbit: number of satellites in each orbit
    - num_of_orbit: number of orbits

    Return:
    - bool: whether the constraints are met
    """
    candidate_orbit = candidate_sat // sat_of_orbit
    candidate_sat_id = candidate_sat % sat_of_orbit
    
    valid_orbit = False
    valid_sat_id = False

    if is_same_orbit_isl:
        if sat1_id_in_orbit < sat2_id_in_orbit:
            orbit_range_start = (sat1_orbit_id - num_of_orbit // 4) % num_of_orbit
            orbit_range_end = sat1_orbit_id

            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit <= num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)

            sat_range_start = (sat1_id_in_orbit - sat_of_orbit // 4) % sat_of_orbit
            sat_range_end = sat1_id_in_orbit

            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id <= sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
        else:
            orbit_range_start = sat1_orbit_id
            orbit_range_end = (sat1_orbit_id + num_of_orbit // 4) % num_of_orbit
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit <= num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)

            sat_range_start = sat1_id_in_orbit
            sat_range_end = (sat1_id_in_orbit + sat_of_orbit // 4) % sat_of_orbit

            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id <= sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
    
    else:
        if sat1_orbit_id < sat2_orbit_id:
            orbit_range_start = (sat1_orbit_id - num_of_orbit // 4) % num_of_orbit
            orbit_range_end = sat1_orbit_id
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit <= num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)

            sat_range_start = (sat1_id_in_orbit - sat_of_orbit // 4) % sat_of_orbit
            sat_range_end = sat1_id_in_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
            
        else:
            orbit_range_start = sat1_orbit_id
            orbit_range_end = (sat1_orbit_id + num_of_orbit // 4) % num_of_orbit
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit <= num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)
            
            sat_range_start = sat1_id_in_orbit
            sat_range_end = (sat1_id_in_orbit + sat_of_orbit // 4) % sat_of_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
        
    return valid_orbit and valid_sat_id



def is_valid_sat_for_sat2(candidate_sat, sat_of_orbit, num_of_orbit, is_same_orbit_isl):
    """
    Determine whether a satellite meets the constraints of sat2

    Parameters:
    - candidate_sat: candidate satellite ID
    - sat_of_orbit: number of satellites in each orbit
    - num_of_orbit: number of orbits

    Return:
    - bool: whether the constraints are met
    """
    candidate_orbit = candidate_sat // sat_of_orbit
    candidate_sat_id = candidate_sat % sat_of_orbit
    
    valid_orbit = False
    valid_sat_id = False
    
    if is_same_orbit_isl:
        if sat2_id_in_orbit > sat1_id_in_orbit:
            orbit_range_start = sat2_orbit_id
            orbit_range_end = (sat2_orbit_id + num_of_orbit // 4) % num_of_orbit
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit < num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)
            
            sat_range_start = sat2_id_in_orbit
            sat_range_end = (sat2_id_in_orbit + sat_of_orbit // 4) % sat_of_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
        else:
            orbit_range_start = (sat2_orbit_id - num_of_orbit // 4) % num_of_orbit
            orbit_range_end = sat2_orbit_id
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit < num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)
            
            sat_range_start = (sat2_id_in_orbit - sat_of_orbit // 4) % sat_of_orbit
            sat_range_end = sat2_id_in_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
    else:
        if sat2_orbit_id < sat1_orbit_id:
            orbit_range_start = (sat2_orbit_id - num_of_orbit // 4) % num_of_orbit
            orbit_range_end = sat2_orbit_id
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit < num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)

            sat_range_start = (sat2_id_in_orbit - sat_of_orbit // 4) % sat_of_orbit
            sat_range_end = sat2_id_in_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)

        else:
            orbit_range_start = sat2_orbit_id
            orbit_range_end = (sat2_orbit_id + num_of_orbit // 4) % num_of_orbit
            
            if orbit_range_start <= orbit_range_end:
                valid_orbit = orbit_range_start <= candidate_orbit <= orbit_range_end
            else:
                valid_orbit = (orbit_range_start <= candidate_orbit < num_of_orbit) or (0 <= candidate_orbit <= orbit_range_end)
            
            sat_range_start = sat2_id_in_orbit
            sat_range_end = (sat2_id_in_orbit + sat_of_orbit // 4) % sat_of_orbit
            
            if sat_range_start <= sat_range_end:
                valid_sat_id = sat_range_start <= candidate_sat_id <= sat_range_end
            else:
                valid_sat_id = (sat_range_start <= candidate_sat_id < sat_of_orbit) or (0 <= candidate_sat_id <= sat_range_end)
        
    return valid_orbit and valid_sat_id


def find_k_closest_paths(orbit_id, sat_id, sat_of_orbit, num_of_orbit, sat_connect_gs, k=3, is_sat1=True, is_same_orbit_isl = True):
    """
    Find links from a given satellite to the k nearest satellites connected to a ground station

    Parameters:
    - orbit_id: the orbit ID of the given satellite
    - sat_id: the ID of the given satellite in orbit
    - sat_of_orbit: the number of satellites in each orbit
    - num_of_orbit: the number of orbits
    - sat_connect_gs: the list of ground stations connected to each satellite
    - k: the number of nearest links to find

    Returns:
    - list: a list of k [next_hop, target_sat, hops] tuples, sorted by hop count
    """
    sat_num = num_of_orbit * sat_of_orbit
    sat_index = orbit_id * sat_of_orbit + sat_id
    
    closest_paths = []
    if sat_connect_gs[sat_index] != -1:
        closest_paths.append([sat_index, sat_index, 0])  # [next_hop, target_sat, hops]
    
    candidates = []
    
    for item in range(sat_num):
        if sat_connect_gs[item] != -1 and item != sat_index: 
            item_orbit = int(item / sat_of_orbit)
            item_sat = item % sat_of_orbit

            is_valid = is_valid_sat_for_sat1(item, sat_of_orbit, num_of_orbit, is_same_orbit_isl) if is_sat1 else \
                        is_valid_sat_for_sat2(item, sat_of_orbit, num_of_orbit, is_same_orbit_isl)
            
            if not is_valid:
                continue

            orbit_diff = abs(item_orbit - orbit_id)
            if orbit_diff > int(num_of_orbit / 2):
                orbit_diff = num_of_orbit - orbit_diff
            
            sat_diff = abs(item_sat - sat_id)
            if sat_diff > int(sat_of_orbit / 2):
                sat_diff = sat_of_orbit - sat_diff
            
            hops = orbit_diff + sat_diff
            
            next_hop = -1
            
            if item_orbit == orbit_id:
                if item_sat > sat_id:
                    if (item_sat - sat_id) <= (sat_of_orbit - (item_sat - sat_id)):
                        next_hop = sat_index + 1  
                    elif sat_id == 0:
                        next_hop = sat_index + sat_of_orbit - 1  
                    else:
                        next_hop = sat_index - 1 
                else:
                    if (sat_id - item_sat) <= (sat_of_orbit - (sat_id - item_sat)):
                        next_hop = sat_index - 1 
                    elif sat_id == sat_of_orbit - 1:
                        next_hop = sat_index - sat_of_orbit + 1  
                    else:
                        next_hop = sat_index + 1  
            else:
                if item_orbit > orbit_id:
                    if (item_orbit - orbit_id) <= (num_of_orbit - (item_orbit - orbit_id)):
                        next_hop = sat_index + sat_of_orbit 
                    elif orbit_id == 0:
                        next_hop = sat_index + sat_of_orbit * (num_of_orbit - 1)  
                    else:
                        next_hop = sat_index - sat_of_orbit  
                else:
                    if (orbit_id - item_orbit) <= (num_of_orbit - (orbit_id - item_orbit)):
                        next_hop = sat_index - sat_of_orbit  
                    elif orbit_id == num_of_orbit - 1:
                        next_hop = sat_index - sat_of_orbit * (num_of_orbit - 1)  
                    else:
                        next_hop = sat_index + sat_of_orbit  
            
            candidates.append([next_hop, item, hops])
    
    candidates.sort(key=lambda x: x[2])
    
    closest_paths.extend(candidates)
    
    return closest_paths[:k]



def find_complete_path(start_sat, target_sat, sat_of_orbit, num_of_orbit):
    """
    Find the complete path from the start satellite to the target satellite

    Parameters:
    - start_sat: start satellite ID
    - target_sat: target satellite ID
    - sat_of_orbit: number of satellites per orbit
    - num_of_orbit: number of orbits

    Returns:
    - list: list of satellite IDs on the complete path
    """
    if start_sat == target_sat:
        return [start_sat]
    
    path = [start_sat]
    current = start_sat
    
    start_orbit = int(start_sat / sat_of_orbit)
    start_pos = start_sat % sat_of_orbit
    target_orbit = int(target_sat / sat_of_orbit)
    target_pos = target_sat % sat_of_orbit

    while current // sat_of_orbit != target_orbit:
        current_orbit = current // sat_of_orbit
        
        orbit_diff = target_orbit - current_orbit
        if abs(orbit_diff) > num_of_orbit // 2:
            if orbit_diff > 0:
                orbit_diff = orbit_diff - num_of_orbit
            else:
                orbit_diff = num_of_orbit + orbit_diff
        
        if orbit_diff > 0:
            current = current + sat_of_orbit
            if current >= num_of_orbit * sat_of_orbit:
                current = current % sat_of_orbit  
        else:
            current = current - sat_of_orbit
            if current < 0:
                current = (num_of_orbit - 1) * sat_of_orbit + (current % sat_of_orbit)
        
        path.append(current)
    
    while current % sat_of_orbit != target_pos:
        current_pos = current % sat_of_orbit
        
        pos_diff = target_pos - current_pos
        if abs(pos_diff) > sat_of_orbit // 2:
            if pos_diff > 0:
                pos_diff = pos_diff - sat_of_orbit
            else:
                pos_diff = sat_of_orbit + pos_diff
        
        if pos_diff > 0:
            current = current + 1
            if current % sat_of_orbit == 0:
                current = current - sat_of_orbit  
        else:
            current = current - 1
            if current % sat_of_orbit == sat_of_orbit - 1 or current < 0:
                current = current + sat_of_orbit 
        
        path.append(current)
    
    return path



def get_k_nearest_gs_paths(sat_id, num_of_orbit, sat_of_orbit, sat_connect_gs, k, is_sat1=True, is_same_orbit_isl=True):
    """
    Get the path from the specified satellite to the k nearest ground stations connecting to the satellite

    Parameters:
    - sat_id: the specified satellite ID
    - k: the number of nearest paths to find
    - num_of_orbit: the number of orbits
    - sat_of_orbit: the number of satellites in each orbit
    - sat_connect_gs: the array of connections from the satellite to the ground station

    Returns:
    - dict: a dictionary containing information about k paths
    """

    orbit_id = sat_id // sat_of_orbit
    local_sat_id = sat_id % sat_of_orbit
    
    closest_paths = find_k_closest_paths(orbit_id, local_sat_id, sat_of_orbit, num_of_orbit, sat_connect_gs, k, is_sat1, is_same_orbit_isl)
    
    paths = []
    for i, (next_hop, target_sat, hops) in enumerate(closest_paths):
        complete_path = find_complete_path(sat_id, target_sat, sat_of_orbit, num_of_orbit)
        paths.append(complete_path)

        # result[f"path_{i+1}"] = {
        #     "target_satellite": target_sat,
        #     "ground_station": sat_connect_gs[target_sat],
        #     "hops": hops,
        #     "next_hop": next_hop,
        #     "complete_path": complete_path
        # }

    return paths



def find_satellite_id(lat, lng, inclination, user_connect_sat):
    """
    Find the connected satellite ID based on geographic coordinates

    Parameters:
    lat - decimal latitude, for example: 48.8667
    lng - decimal longitude, for example: 2.4167
    constellation_name - constellation name, used to locate the file path
    time_slot - time slot
    inclination - constellation inclination, default is 53 degrees

    Return:
    Connected satellite ID
    """

    block_lat = round(lat)
    block_lng = round(lng)

    lat_idx = inclination - block_lat
    lng_idx = block_lng + 180
    block_index = lat_idx * 360 + lng_idx

    return user_connect_sat[block_index]



def find_load_balanced_path(start_sat, target_sat, sat_of_orbit, num_of_orbit, isl_traffic, threshold):
    """
    Find a load-balanced path from the start satellite to the target satellite
    
    Parameters:
    - start_sat: start satellite ID
    - target_sat: target satellite ID
    - sat_of_orbit: number of satellites per orbit
    - num_of_orbit: number of orbits
    - isl_traffic: list of traffic load for each satellite link
    - threshold: maximum allowed traffic on a link (if None, will be determined automatically)
    
    Returns:
    - list: list of satellite IDs on the load-balanced path
    """
    if start_sat == target_sat:
        return [start_sat]
    
    distances = {i: float('infinity') for i in range(num_of_orbit * sat_of_orbit)}
    distances[start_sat] = 0
    predecessors = {i: None for i in range(num_of_orbit * sat_of_orbit)}
    
    priority_queue = [(0, start_sat)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == target_sat:
            break
            
        if current_distance > distances[current_node]:
            continue
            
        neighbors = get_neighbors(current_node, sat_of_orbit, num_of_orbit)
        
        for neighbor in neighbors:
            link_traffic = max(isl_traffic[current_node], isl_traffic[neighbor])
            
            if link_traffic > threshold:
                edge_weight = 100  
            else:
                edge_weight = 1 + (link_traffic / threshold) * 2
            
            distance = current_distance + edge_weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    path = []
    current = target_sat
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    return path[::-1]



def get_neighbors(sat_id, sat_of_orbit, num_of_orbit):
    """
    Get neighbor nodes of a satellite

    Parameters:
    - sat_id: satellite ID
    - sat_of_orbit: number of satellites per orbit
    - num_of_orbit: number of orbits

    Returns:
    - list: list of neighbor satellite IDs
    """
    neighbors = []
    
    orbit = sat_id // sat_of_orbit
    position = sat_id % sat_of_orbit
    
    prev_pos = (position - 1) % sat_of_orbit
    neighbors.append(orbit * sat_of_orbit + prev_pos)
    
    next_pos = (position + 1) % sat_of_orbit
    neighbors.append(orbit * sat_of_orbit + next_pos)
    
    left_orbit = (orbit - 1) % num_of_orbit
    neighbors.append(left_orbit * sat_of_orbit + position)
    
    right_orbit = (orbit + 1) % num_of_orbit
    neighbors.append(right_orbit * sat_of_orbit + position)
    
    return neighbors



def cir_to_car_np(lat, lng, h):
    x = (RADIUS + h) * math.cos(math.radians(lat)) * math.cos(
        math.radians(lng))
    y = (RADIUS + h) * math.cos(math.radians(lat)) * math.sin(
        math.radians(lng))
    z = (RADIUS + h) * math.sin(math.radians(lat))
    return np.array([x, y, z])



def calculate_queuing_delay(isl_traffic, capacity=20480, ratio=0.8, unit_traffic=40):
    """
    Calculate network delay, taking into account the tolerance overload factor

    Parameters:
    traffic_rate: traffic rate (e.g. Mbps)
    capacity: link capacity (same unit, e.g. Mbps)
    ratio: tolerance overload factor, the link can accommodate at most ratio*capacity traffic
    max_delay: estimated maximum delay when the link is congested

    Returns:
    delay: estimated average delay
    """

    effective_capacity = capacity / ratio

    if effective_capacity < isl_traffic:
        return 1
    rou = 1.0
    if isl_traffic > capacity:
        rou = 5.0
    
    queuing_delay = rou / ((effective_capacity / unit_traffic) - (isl_traffic / unit_traffic))

    return queuing_delay






def icarus_single_link_attack(constellation, time_slot, src_lat=48.8667, src_lon=2.4167, 
                              dst_lat=40.4168, dst_lon=-3.7038, link_num = 500, rate = 40,
                              capacity=20480):
    """
    Parameters:
    - constellation: The constellation object containing the satellite configuration
    - time_slot: Current time slot of the simulation
    - src_lat: Source latitude in degrees (default: 48.8667, near Paris)
    - src_lon: Source longitude in degrees (default: 2.4167, near Paris)
    - dst_lat: Destination latitude in degrees (default: 40.4168, near Madrid)
    - dst_lon: Destination longitude in degrees (default: -3.7038, near Madrid)
    - link_num: Number of attack paths to generate (default: 500)
    - rate: Traffic rate to inject on each path in Mbps (default: 40)
    - capacity: Link capacity in Mbps (default: 20480)

    Operation:
    1. Loads necessary constellation data from files for the given time slot
    2. Identifies satellites serving the source and destination locations
    3. Finds the regular path between these satellites
    4. Selects a critical link in this path to target
    5. Identifies multiple alternative paths that cross this critical link
    6. Injects artificial traffic on these paths to congest the targeted link
    7. Calculates both original and load-balanced path performance after the attack
    8. Computes propagation and queuing delays for both paths
    9. Saves attack results and modified traffic data to files

    Return:
    - None (Results are saved to files in the specified directory)

    Outputs:
    The function saves multiple files under the 'data/{constellation_name}_icarus/single_link_attack/{attack_size}_{coordinates}/{time_slot}/' directory:
    - ISL traffic data (sender, receiver, and combined)
    - Uplink and downlink traffic data
    - Original and load-balanced paths
    - Traffic levels on these paths
    - Propagation and queuing delays for both paths

    Notes:
    - This function specifically targets ISL (Inter-Satellite Link) congestion
    - The attack is strategic, focusing on a critical link rather than random distribution
    - The attack demonstrates how targeted congestion can force traffic onto longer paths
    - Delay calculations include both propagation (physical distance) and queuing (congestion) delays

    """

    global sat1_id_in_orbit, sat1_orbit_id, sat2_id_in_orbit, sat2_orbit_id

    cons_name = constellation.constellation_name
    shell = constellation.shells[0]
    orbit_num = shell.number_of_orbits
    sat_per_cycle = shell.number_of_satellite_per_orbit
    inclination = math.ceil(shell.inclination)

    user_connect_sat_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                             'user_connect_sat.txt')
    user_connect_sat = np.loadtxt(user_connect_sat_filename)
    user_connect_sat = list(map(int, user_connect_sat))

    sat_connect_gs_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                           'sat_connect_gs.txt')
    sat_connect_gs = np.loadtxt(sat_connect_gs_filename)
    sat_connect_gs = list(map(int, sat_connect_gs))

    isl_traffic_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot), 'isl_traffic.txt')
    isl_traffic = np.loadtxt(isl_traffic_filename)
    isl_traffic = list(map(int, isl_traffic))

    isl_sender_traffic_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                               'isl_sender_traffic.txt')
    isl_sender_traffic = np.loadtxt(isl_sender_traffic_filename)
    isl_sender_traffic = list(map(int, isl_sender_traffic))

    isl_receiver_traffic_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                                 'isl_receiver_traffic.txt')
    isl_receiver_traffic = np.loadtxt(isl_receiver_traffic_filename)
    isl_receiver_traffic = list(map(int, isl_receiver_traffic))

    downlink_traffic_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                             'downlink_traffic.txt')
    downlink_traffic = np.loadtxt(downlink_traffic_filename)
    downlink_traffic = list(map(int, downlink_traffic))

    uplink_traffic_filename = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot),
                                           'uplink_traffic.txt')
    uplink_traffic = np.loadtxt(uplink_traffic_filename)
    uplink_traffic = list(map(int, uplink_traffic))


    sat1_id = find_satellite_id(src_lat, src_lon, inclination, user_connect_sat)
    sat2_id = find_satellite_id(dst_lat, dst_lon, inclination, user_connect_sat)

    # print(sat1_id, sat2_id)

    path = find_complete_path(sat1_id, sat2_id, sat_per_cycle, orbit_num)

    ori_path = path
    ori_path_traffic = []
    for sat in ori_path:
        ori_path_traffic.append(isl_traffic[sat])

    path = path[1:-1]

    # for sat in path:
    #     print(sat)

    st_sat = ed_sat = 0
    if len(path) >= 2:
        i = random.randint(0, len(path) - 2)
        st_sat = path[i]
        ed_sat = path[i + 1]
    
    # print(st_sat, ed_sat)
    # print()

    sat1_id_in_orbit = st_sat % sat_per_cycle
    sat1_orbit_id = st_sat // sat_per_cycle
    sat2_id_in_orbit = ed_sat % sat_per_cycle
    sat2_orbit_id = ed_sat // sat_per_cycle

    is_sat1 = True
    is_same_orbit_isl = False

    if st_sat // sat_per_cycle == ed_sat // sat_per_cycle:
        is_same_orbit_isl = True

    st_paths = get_k_nearest_gs_paths(st_sat, orbit_num, sat_per_cycle, sat_connect_gs, 100, is_sat1, is_same_orbit_isl)

    # for p in st_paths:
    #     print(p)
    #     print()
    # print(len(st_paths))

    is_sat1 = False
    
    ed_paths = get_k_nearest_gs_paths(ed_sat, orbit_num, sat_per_cycle, sat_connect_gs, 100, is_sat1, is_same_orbit_isl)

    # print(len(ed_paths))

    for _ in range(link_num):
        path = []
        st = []
        ed = []
        p_a = random.choice(st_paths)
        p_b = random.choice(ed_paths)
        bit = bool(random.getrandbits(1))
        if bit:
            st = p_a[::-1]
            ed = p_b
        else:
            st = p_b[::-1]
            ed = p_a
        path = st + ed

        uplink_traffic[path[0]] += rate
        downlink_traffic[path[-1]] += rate
        
        if len(path) > 1:
            isl_traffic[path[0]] += rate
            isl_traffic[path[-1]] += rate
            isl_sender_traffic[path[0]] += rate
            isl_receiver_traffic[path[-1]] += rate
            path = path[1:-1]
        
        for sat in path:
            isl_traffic[sat] += rate
            isl_sender_traffic[sat] += rate
            isl_receiver_traffic[sat] += rate
    

    attack_path_traffic = []
    for sat in ori_path:
        attack_path_traffic.append(isl_traffic[sat])

    load_path = find_load_balanced_path(sat1_id, sat2_id, sat_per_cycle, orbit_num, isl_traffic, capacity * 0.6)
    load_path_traffic = []
    for sat in load_path:
        load_path_traffic.append(isl_traffic[sat])


    sat_pos_car = []
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


    st_pos = cir_to_car_np(src_lat, src_lon, 0)
    ed_pos = cir_to_car_np(dst_lat, dst_lon, 0)
    ori_delay = np.sqrt(np.sum(np.square(st_pos - sat_pos_car[ori_path[0]]))) / c + \
        np.sqrt(np.sum(np.square(ed_pos - sat_pos_car[ori_path[-1]]))) / c
    if len(ori_path) > 1:
        st_sat = ori_path[0]
        left_path = ori_path[1:]
        for sat in left_path:
            ori_delay += (np.sqrt(np.sum(np.square(sat_pos_car[st_sat] - sat_pos_car[sat])))) / c
            select_traffic = min(isl_traffic[st_sat], isl_traffic[sat])
            ori_delay += calculate_queuing_delay(select_traffic, capacity, 0.8, rate)
            st_sat = sat
    ori_delay = ori_delay * 2

    load_delay = np.sqrt(np.sum(np.square(st_pos - sat_pos_car[load_path[0]]))) / c + \
        np.sqrt(np.sum(np.square(ed_pos - sat_pos_car[load_path[-1]]))) / c
    if len(load_path) > 1:
        st_sat = load_path[0]
        left_path = load_path[1:]
        for sat in left_path:
            load_delay += (np.sqrt(np.sum(np.square(sat_pos_car[st_sat] - sat_pos_car[sat])))) / c
            select_traffic = min(isl_traffic[st_sat], isl_traffic[sat])
            load_delay += calculate_queuing_delay(select_traffic, capacity, 0.8, rate)
            st_sat = sat
    load_delay = load_delay * 2

    folder_name = f"{link_num * rate}_{src_lat}_{src_lon}_{dst_lat}_{dst_lon}"
    file_path = os.path.join("data", f"{cons_name}_icarus", "single_link_attack", folder_name, str(time_slot))
    os.makedirs(file_path, exist_ok=True)

    isl_traffic = np.array(isl_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'isl_traffic.txt'), isl_traffic, fmt='%d')

    isl_sender_traffic = np.array(isl_sender_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'isl_sender_traffic.txt'), isl_sender_traffic, fmt='%d')

    isl_receiver_traffic = np.array(isl_receiver_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'isl_receiver_traffic.txt'), isl_receiver_traffic, fmt='%d')

    downlink_traffic = np.array(downlink_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'downlink_traffic.txt'), downlink_traffic, fmt='%d')

    uplink_traffic = np.array(uplink_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'uplink_traffic.txt'), uplink_traffic, fmt='%d')

    ori_path = np.array(ori_path, dtype=int)
    np.savetxt(os.path.join(file_path, 'origin_path.txt'), ori_path, fmt='%d')

    load_path = np.array(load_path, dtype=int)
    np.savetxt(os.path.join(file_path, 'load_path.txt'), load_path, fmt='%d')

    ori_path_traffic = np.array(ori_path_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'origin_path_traffic.txt'), ori_path_traffic, fmt="%d")

    attack_path_traffic = np.array(attack_path_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'attack_path_traffic.txt'), attack_path_traffic, fmt='%d')

    load_path_traffic = np.array(load_path_traffic, dtype=int)
    np.savetxt(os.path.join(file_path, 'load_path_traffic.txt'), load_path_traffic, fmt='%d')

    ori_delay = np.array([ori_delay])
    np.savetxt(os.path.join(file_path, 'ori_delay.txt'), ori_delay, fmt='%.3f')

    load_delay = np.array([load_delay])
    np.savetxt(os.path.join(file_path, 'load_delay.txt'), load_delay, fmt='%.3f')

    # print("Finished calculating single link attack traffic generation at timeslot", str(time_slot))
