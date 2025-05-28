"""
Author : zhifenghan

Date : 2025/05/09

Function : This function implements a positive grid Icarus attack on satellite constellations.
           The attack strategically places malicious terminals (bots) across the Earth's surface
           to congest ground-to-satellite links (GSLs) and affect legitimate traffic.
           It uses a population-weighted approach to deploy bots in areas that maximize
           the attack impact while minimizing the number of required attack resources.

"""

import numpy as np
import math
import os
import sys
import json
import random

cons_name = ""
altitude = 0
orbit_num = 0
sat_per_cycle = 0
inclination = 0

bot_num = 0  # total number of malicious terminals
traffic_thre = 20  # upmost 20 malicious terminals accessed to a satellite
GSL_capacity = 4096
unit_traffic = 20  # 20Mbps per malicious terminal
sat_connect_gs = []  
block_num = 0
pop_count = []  # 53 ~ -53, traffic probability per block
weights = []  # weights for each block
flows_selected = {}  # legal background flows according to the probability. {(src_sat,dst,sat):bandwidth,...} 
weights_num = 0
cumulate_weight = []
sum_weight = 0
attack_gsl = [] # attacked GSLs
chosen_blocks = [] # blocks for deploying bots
cumu_affected_traffic_volume = 0  
cumu_downlink_malicious_traffic = []
path = []  # path[i][j] = k: k is the next hop from i to j; k == j shows that k/j is a landing satellite connected to a GS
given_bot_number = 950


def init_weight():  # initiate weights for each block
    global weights
    global sum_weight
    global cumulate_weight
    global weights_num
    for block in range(inclination * 2 * 360):
        if pop_count[block] == 0:
            continue
        weight = math.ceil(pop_count[block]) 
        weights.append([block, weight])
        sum_weight += weight
        cumulate_weight.append(sum_weight) 
    weights_num = len(cumulate_weight)
    

def get_one_block(
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


def find_next_sat(orbit_id, sat_id, sat_per_cycle,
                  sat_connect_gs):  # the the next satellite (-1: no landing satellite)
    next_sat = -1
    min_hops = int(sat_per_cycle / 2) + int(orbit_num / 2)
    sat_index = orbit_id * sat_per_cycle + sat_id
    if sat_connect_gs[sat_index] != -1:
        return sat_index, sat_index
    for item in range(orbit_num * sat_per_cycle):
        if sat_connect_gs[item] != -1:
            item_orbit = int(item / sat_per_cycle)
            item_sat = item % sat_per_cycle
            orbit_diff = abs(item_orbit -
                             orbit_id) if abs(item_orbit - orbit_id) <= int(
                                 orbit_num /
                                 2) else orbit_num - abs(item_orbit -
                                                            orbit_id)
            sat_diff = abs(item_sat - sat_id) if abs(item_sat - sat_id) <= int(
                sat_per_cycle / 2) else sat_per_cycle - abs(item_sat - sat_id)
            if (sat_diff + orbit_diff) >= min_hops:
                continue

            min_hops = (sat_diff + orbit_diff)
            if item_orbit == orbit_id:  # same orbit
                if item_sat > sat_id:
                    if (item_sat - sat_id) <= (sat_per_cycle -
                                               (item_sat - sat_id)):
                        next_sat = sat_index + 1
                    elif sat_id == 0:
                        next_sat = sat_index + sat_per_cycle - 1
                    else:
                        next_sat = sat_index - 1
                else:
                    if (sat_id - item_sat) <= (sat_per_cycle -
                                               (sat_id - item_sat)):
                        next_sat = sat_index - 1
                    elif sat_id == sat_per_cycle - 1:
                        next_sat = sat_index - sat_per_cycle + 1
                    else:
                        next_sat = sat_index + 1
            else:  # not same orbit
                if item_orbit > orbit_id:
                    if (item_orbit - orbit_id) <= (orbit_num -
                                                   (item_orbit - orbit_id)):
                        next_sat = sat_index + sat_per_cycle
                    elif orbit_id == 0:
                        next_sat = sat_index + sat_per_cycle * (orbit_num -
                                                               1)
                    else:
                        next_sat = sat_index - sat_per_cycle
                else:
                    if (orbit_id - item_orbit) <= (orbit_num -
                                                   (orbit_id - item_orbit)):
                        next_sat = sat_index - sat_per_cycle
                    elif orbit_id == orbit_num - 1:
                        next_sat = sat_index - sat_per_cycle * (orbit_num -
                                                               1)
                    else:
                        next_sat = sat_index + sat_per_cycle

    return next_sat, sat_index


def floyd():
    global path

    for orbit_id in range(orbit_num):
        for sat_id in range(sat_per_cycle):
            next_sat, sat_index = find_next_sat(
                orbit_id, sat_id, sat_per_cycle,
                sat_connect_gs)  # the nearest landing satellite (-1: no landing satellite)
            path[sat_index] = next_sat  # -1: no more landing satellite. Land from this satellite
            

def add_bot(block_id, user_connect_sat, traffic, sat_connect_gs, ratio):
    global cumu_affected_traffic_volume
    global cumu_downlink_malicious_traffic
    global attack_gsl

    landing_sat = path[user_connect_sat[block_id]]
    while landing_sat != path[landing_sat]:
        landing_sat = path[landing_sat]
    landing_gs = sat_connect_gs[landing_sat]
    if landing_gs != -1 and landing_sat != -1:
        if cumu_downlink_malicious_traffic[landing_sat] + traffic[landing_sat] + unit_traffic > GSL_capacity and cumu_downlink_malicious_traffic[landing_sat] + traffic[landing_sat] <= GSL_capacity:
            attack_gsl.append(landing_sat)
        if cumu_downlink_malicious_traffic[landing_sat] + traffic[landing_sat] + unit_traffic > GSL_capacity / ratio and cumu_downlink_malicious_traffic[landing_sat] + traffic[landing_sat] <= GSL_capacity / ratio:
            cumu_affected_traffic_volume += traffic[landing_sat]
        cumu_downlink_malicious_traffic[landing_sat] += unit_traffic    
    return


def positive_grid_icarus(constellation, time_slot, 
                        ratio=0.9, target_affected_traffic=300000,
                        traffic_threshold=20, gsl_capacity=4096, 
                        unit_traffic_cap=20, given_bot_num=950):
    """
    Parameters:
    - constellation: The constellation object containing the satellite network parameters
    - time_slot: Current time slot of the simulation
    - ratio: Link utilization ratio threshold (default: 0.9)
    - target_affected_traffic: Target amount of legitimate traffic to be affected (default: 300000)
    - traffic_threshold: Maximum number of malicious terminals that can access a single satellite (default: 20)
    - gsl_capacity: Capacity of ground-to-satellite links in Mbps (default: 4096)
    - unit_traffic_cap: Traffic generated by each malicious terminal in Mbps (default: 20)
    - given_bot_num: Maximum number of bots to deploy if target cannot be reached (default: 950)

    Operation:
    1. Initializes constellation parameters and attack variables
    2. Loads legitimate traffic data, satellite-ground station connections, and user-satellite mappings
    3. Loads population distribution data to weight the attack distribution
    4. Uses Floyd algorithm to compute shortest paths to ground stations for all satellites
    5. Deploys bots iteratively based on population-weighted selection of surface blocks
    6. For each deployed bot:
       - Identifies the landing satellite that will handle its traffic
       - Checks if adding malicious traffic will congest the GSL based on ratio
       - Tracks affected legitimate traffic volume
    7. Continues deployment until either:
       - The target affected traffic volume is reached, or
       - The maximum allowed number of bots is reached
    8. Saves attack results to output files

    Return:
    - None (Results are saved to files in the specified directory)

    Outputs:
    The function saves multiple files under the 'data/{constellation_name}_icarus/attack_traffic_data_land_only_bot/{parameters}/{time_slot}/' directory:
    - attack_gsl.txt: List of GSLs that were successfully attacked
    - bot_num.txt: Total number of bots deployed
    - block_num.txt: Number of unique surface blocks with bots
    - cumu_affected_traffic_volume.txt: Total legitimate traffic affected by the attack
    - attack_gsl_given_bot_num.txt: List of GSLs attacked if limited to given_bot_number (if applicable)
    - cumu_affected_traffic_volume_given_bot_num.txt: Traffic affected if limited to given_bot_number (if applicable)

    Notes:
    - This attack specifically targets downlink congestion at ground stations
    - Bot deployment is optimized using population density as a proxy for legitimate traffic
    - The attack strategically congests GSLs just above their capacity threshold to maximize impact
    - The function implements the "positive grid" variation of the Icarus attack
    """

    global cons_name, altitude, orbit_num, sat_per_cycle, inclination
    global bot_num, traffic_thre, GSL_capacity, unit_traffic, block_num, sat_connect_gs, pop_count
    global weights, flows_selected, cumulate_weight, weights_num, sum_weight, attack_gsl
    global chosen_blocks, cumu_affected_traffic_volume, cumu_downlink_malicious_traffic, path, given_bot_number

    traffic_thre = traffic_threshold
    GSL_capacity = gsl_capacity
    unit_traffic = unit_traffic_cap
    given_bot_number = given_bot_num

    cons_name = constellation.constellation_name
    shell = constellation.shells[0] # the first shell
    altitude = shell.altitude
    orbit_num = shell.number_of_orbits
    sat_per_cycle = shell.number_of_satellite_per_orbit
    inclination = shell.inclination
    inclination = math.ceil(inclination)

    bot_num = 0  # total number of malicious terminals
    sat_connect_gs = []  
    block_num = 0
    pop_count = []  # 53 ~ -53, traffic probability per block
    weights = []  # weights for each block
    flows_selected = {}  # legal background flows according to the probability. {(src_sat,dst,sat):bandwidth,...} 。
    weights_num = 0
    cumulate_weight = []
    sum_weight = 0
    attack_gsl = [] # attacked GSLs
    chosen_blocks = [] # blocks for deploying bots
    cumu_affected_traffic_volume = 0  
    cumu_downlink_malicious_traffic = [0 for i in range(orbit_num * sat_per_cycle)]
    path =[-1 for i in range(orbit_num * sat_per_cycle)]

    base_path = os.path.join("data", f"{cons_name}_link_traffic_data", str(time_slot))
    traffic_filename = os.path.join(base_path, 'downlink_traffic.txt')
    traffic = np.loadtxt(traffic_filename)
    traffic = list(map(int, traffic))
    traffic_filename = os.path.join(base_path, 'uplink_traffic.txt')
    uplink_traffic = np.loadtxt(traffic_filename)
    uplink_traffic = list(map(int, uplink_traffic))
    sat_connect_gs = np.loadtxt(os.path.join(base_path, 'sat_connect_gs.txt'))
    user_connect_sat = np.loadtxt(os.path.join(base_path, 'user_connect_sat.txt'))
    user_connect_sat = list(map(int, user_connect_sat))
    
    traffic_sum = np.sum(traffic)

    # load traffic distribution
    traffic_file = os.path.join("data", "starlink_count.txt")
    with open(traffic_file, 'r') as file:
        lines = file.readlines()
        for row in range(90 - inclination, 90 + inclination):
            pop_count.extend([float(x) for x in lines[row].split(' ')[:-1]] + [0])
    
    init_weight()

    floyd()

    dir_path = os.path.join(
        "data",
        cons_name + "_icarus",
        "attack_traffic_data_land_only_bot",
        f"{ratio}-{target_affected_traffic}-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}",
        str(time_slot)
    )

    os.makedirs(dir_path, exist_ok=True)

    # deploy bots according to traffic weights of each block
    while True:
        chosen_id = get_one_block(cumulate_weight, weights_num,
                               sum_weight)
        block_id = weights[chosen_id][0]
        bot_num += 0.1
        if block_id not in chosen_blocks:
            block_num += 0.1
            chosen_blocks.append(block_id)
        add_bot(block_id, user_connect_sat, traffic, sat_connect_gs, ratio)
        if cumu_affected_traffic_volume >= target_affected_traffic:
            break
        elif int(bot_num) == given_bot_number:
            folder_path = os.path.join(
                "data", f"{cons_name}_icarus", "attack_traffic_data_land_only_bot",
                f"{ratio}-{target_affected_traffic}-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}",
                str(time_slot)
            )
            attack_gsl_given_bot = np.array(attack_gsl, dtype=int)
            np.savetxt(
                os.path.join(folder_path, 'attack_gsl_given_bot_num.txt'),
                attack_gsl_given_bot,
                fmt='%d'
            )
            cumu_affected_traffic_volume_given_bot = np.array([cumu_affected_traffic_volume], dtype=int)
            np.savetxt(
                os.path.join(folder_path, 'cumu_affected_traffic_volume_given_bot_num.txt'),
                cumu_affected_traffic_volume_given_bot,
                fmt='%d'
            )

    output_dir = os.path.join(
        "data", f"{cons_name}_icarus", "attack_traffic_data_land_only_bot",
        f"{ratio}-{target_affected_traffic}-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}",
        str(time_slot)
    )
    attack_gsl = np.array(attack_gsl, dtype=int)
    np.savetxt(os.path.join(output_dir, 'attack_gsl.txt'), attack_gsl, fmt='%d')

    bot_num = np.array([bot_num], dtype=int)
    np.savetxt(os.path.join(output_dir, 'bot_num.txt'), bot_num, fmt='%d')

    block_num = np.array([block_num], dtype=int)
    np.savetxt(os.path.join(output_dir, 'block_num.txt'), block_num, fmt='%d')

    cumu_affected_traffic_volume = np.array([cumu_affected_traffic_volume], dtype=int)
    np.savetxt(os.path.join(output_dir, 'cumu_affected_traffic_volume.txt'), cumu_affected_traffic_volume, fmt='%d')

    # print("Finished calculating malicious terminals deployment and generating malicious traffic for +Grid at timeslot", str(time_slot))

