"""
Author : zhifenghan

Date : 2025/05/09

Function : This function calculates the energy consumption of communication links for satellites
           in a constellation. It models power consumption for different communication subsystems
           (GSL and ISL transmitters/receivers) based on traffic loads, accounting for active,
           idle, and tail energy states to create a realistic energy consumption profile.
"""

import numpy as np
import os
import json


isl_traffic = []  # egress traffic per satellite
isl_sender_traffic = [] # ISL sending traffic of a certain satellite
isl_receiver_traffic = []   # ISL receiving traffic of a certain satellite
downlink_traffic = []  # downlink traffic per satellite
uplink_traffic = [] # uplink traffic per satellite
links_energy_sum = []   # The total energy consumed by the satellite link transmission 


def communication_link(constellation, time_slot, gsl_transmitter_idle=40, isl_transmitter_idle=10,
                        gsl_transmitter_active=200, isl_transmitter_active=50, gsl_transmitter_w=0.01,
                        isl_transmitter_w=0.0025, gsl_receiver_idle=40, isl_receiver_idle=10,
                        gsl_receiver_active=100, isl_receiver_active=25, gsl_receiver_w=0.008,
                        isl_receiver_w=0.002, tail_energy_time=2):
    """
    Parameters:
    - constellation: The constellation object containing satellite network parameters
    - time_slot: Current time slot for which to calculate energy consumption
    - gsl_transmitter_idle: Ground-to-Satellite Link transmitter idle power in W (default: 40)
    - isl_transmitter_idle: Inter-Satellite Link transmitter idle power in W (default: 10)
    - gsl_transmitter_active: GSL transmitter active power in W (default: 200)
    - isl_transmitter_active: ISL transmitter active power in W (default: 50)
    - gsl_transmitter_w: GSL transmitter power per traffic unit in W (default: 0.01)
    - isl_transmitter_w: ISL transmitter power per traffic unit in W (default: 0.0025)
    - gsl_receiver_idle: GSL receiver idle power in W (default: 40)
    - isl_receiver_idle: ISL receiver idle power in W (default: 10)
    - gsl_receiver_active: GSL receiver active power in W (default: 100)
    - isl_receiver_active: ISL receiver active power in W (default: 25)
    - gsl_receiver_w: GSL receiver power per traffic unit in W (default: 0.008)
    - isl_receiver_w: ISL receiver power per traffic unit in W (default: 0.002)
    - tail_energy_time: Duration of tail energy consumption in time slots (default: 2)

    Operation:
    1. Initializes constellation parameters and energy structures
    2. Loads or creates the tail state tracking file for persistent state between calls
    3. Loads traffic data for the current time slot:
       - Downlink traffic per satellite
       - Uplink traffic per satellite
       - ISL sender traffic per satellite
       - ISL receiver traffic per satellite
    4. For each satellite in the constellation:
       - Calculates downlink transmitter energy based on traffic or tail/idle state
       - Calculates uplink receiver energy based on traffic or tail/idle state
       - Calculates ISL sender transmitter energy based on traffic or tail/idle state
       - Calculates ISL receiver energy based on traffic or tail/idle state
       - Sums all energy components for total communication energy
    5. Updates and saves tail state for use in subsequent time slots
    6. Saves energy consumption data to output files

    Return:
    - None (Results are saved to files in the specified directory)

    Outputs:
    The function saves energy consumption data under the 'data/{constellation_name}_link_energy/{time_slot}/' directory:
    - link_energy.txt: Total communication link energy consumption per satellite

    Notes:
    - The model accounts for three power states for each communication subsystem:
      * Active: High power mode when actively transmitting/receiving traffic
      * Tail: Continued high power consumption for a short period after traffic stops
      * Idle: Low power standby mode when no traffic or tail energy is present
    - Tail energy modeling is important for realistic power profiles since communication
      systems typically don't immediately return to idle power after traffic stops
    - The model separately tracks four different communication subsystems per satellite:
      downlink transmitters, uplink receivers, ISL transmitters, and ISL receivers
    """

    global isl_traffic, isl_sender_traffic, isl_receiver_traffic, downlink_traffic, uplink_traffic, links_energy_sum

    cons_name = constellation.constellation_name
    shell = constellation.shells[0] # the first shell
    altitude = shell.altitude
    num_of_orbit = shell.number_of_orbits
    sat_of_orbit = shell.number_of_satellite_per_orbit
    inclination = shell.inclination
    sat_num = num_of_orbit * sat_of_orbit
    links_energy_sum = [0] * sat_num

    state_dir = os.path.join("data", f"{cons_name}_link_energy")
    state_file = os.path.join(state_dir, "tail_state.json")
    os.makedirs(state_dir, exist_ok=True)

    tail_state = {
        'downlink_tail_remaining': [0] * sat_num,
        'uplink_tail_remaining': [0] * sat_num,
        'isl_sender_tail_remaining': [0] * sat_num,
        'isl_receiver_tail_remaining': [0] * sat_num
    }

    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                tail_state = json.load(f)
        except Exception as e:
            print(f"Error loading state file: {e}")

    downlink_tail_remaining = tail_state['downlink_tail_remaining']
    uplink_tail_remaining = tail_state['uplink_tail_remaining']
    isl_sender_tail_remaining = tail_state['isl_sender_tail_remaining']
    isl_receiver_tail_remaining = tail_state['isl_receiver_tail_remaining']

    base_path = os.path.join("data", f"{cons_name}_link_traffic_data", str(time_slot))

    traffic_filename = os.path.join(base_path, 'downlink_traffic.txt')
    downlink_traffic = np.loadtxt(traffic_filename)
    downlink_traffic = list(map(int, downlink_traffic))
    traffic_filename = os.path.join(base_path, 'uplink_traffic.txt')
    uplink_traffic = np.loadtxt(traffic_filename)
    uplink_traffic = list(map(int, uplink_traffic))
    traffic_filename = os.path.join(base_path, 'isl_sender_traffic.txt')
    isl_sender_traffic = np.loadtxt(traffic_filename)
    isl_sender_traffic = list(map(int, isl_sender_traffic))
    traffic_filename = os.path.join(base_path, 'isl_receiver_traffic.txt')
    isl_receiver_traffic = np.loadtxt(traffic_filename)
    isl_receiver_traffic = list(map(int, isl_receiver_traffic))

    for sat_id in range(sat_num):
        if downlink_traffic[sat_id] > 0:
            links_energy_sum[sat_id] = links_energy_sum[sat_id] + gsl_transmitter_active + gsl_transmitter_w * downlink_traffic[sat_id]
            downlink_tail_remaining[sat_id] = tail_energy_time
        elif downlink_tail_remaining[sat_id] > 0:
            links_energy_sum[sat_id] += gsl_transmitter_active
            downlink_tail_remaining[sat_id] -= 1
        else:
            links_energy_sum[sat_id] += gsl_transmitter_idle
        
        if uplink_traffic[sat_id] > 0:
            links_energy_sum[sat_id] = links_energy_sum[sat_id] + gsl_receiver_active + gsl_receiver_w * uplink_traffic[sat_id]
            uplink_tail_remaining[sat_id] = tail_energy_time
        elif uplink_tail_remaining[sat_id] > 0:
            links_energy_sum[sat_id] += gsl_receiver_active
            uplink_tail_remaining[sat_id] -= 1
        else:
            links_energy_sum[sat_id] += gsl_receiver_idle
        
        if isl_sender_traffic[sat_id] > 0:
            links_energy_sum[sat_id] = links_energy_sum[sat_id] + isl_transmitter_active + isl_transmitter_w * isl_sender_traffic[sat_id]
            isl_sender_tail_remaining[sat_id] = tail_energy_time
        elif isl_sender_tail_remaining[sat_id] > 0:
            links_energy_sum[sat_id] += isl_transmitter_active
            isl_sender_tail_remaining[sat_id] -= 1
        else:
            links_energy_sum[sat_id] += isl_transmitter_idle

        if isl_receiver_traffic[sat_id] > 0:
            links_energy_sum[sat_id] = links_energy_sum[sat_id] + isl_receiver_active + isl_receiver_w * isl_receiver_traffic[sat_id]
            isl_receiver_tail_remaining[sat_id] = tail_energy_time
        elif isl_receiver_tail_remaining[sat_id] > 0:
            links_energy_sum[sat_id] += isl_receiver_active
            isl_receiver_tail_remaining[sat_id] -= 1
        else:
            links_energy_sum[sat_id] += isl_receiver_idle
    

    updated_tail_state = {
        'downlink_tail_remaining': downlink_tail_remaining,
        'uplink_tail_remaining': uplink_tail_remaining,
        'isl_sender_tail_remaining': isl_sender_tail_remaining,
        'isl_receiver_tail_remaining': isl_receiver_tail_remaining
    }

    try:
        with open(state_file, 'w') as f:
            json.dump(updated_tail_state, f)
    except Exception as e:
        print(f"Error saving state file: {e}")

    output_path = os.path.join("data", f"{cons_name}_link_energy", str(time_slot))
    os.makedirs(output_path, exist_ok=True)
    links_energy_sum = np.array(links_energy_sum, fmt=float)
    output_path = os.path.join("data", f"{cons_name}_link_energy", str(time_slot), "link_energy.txt")
    np.savetxt(output_path, links_energy_sum, fmt='%.3f')

