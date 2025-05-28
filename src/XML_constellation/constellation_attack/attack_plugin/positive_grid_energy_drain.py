"""
Author : zhifenghan

Date : 2025/05/09

Function : This function implements an energy drain attack on satellite constellations.
           The attack targets satellites during eclipse periods when they rely on battery power,
           injecting malicious traffic to drain energy resources through increased communications.
           It uses a geographically-aware approach that considers satellite positions relative
           to the Earth's shadow and landmasses to optimize attack impact.
"""

import math
# from skyfield.api import load
import numpy as np
import h5py
# import cartopy.io.shapereader as shpreader
# import shapely.geometry as sgeom
# from shapely.prepared import prep
import os


RADIUS = 6371

def cir_to_car_np(lat, lng, h):
    x = (RADIUS + h) * math.cos(math.radians(lat)) * math.cos(
        math.radians(lng))
    y = (RADIUS + h) * math.cos(math.radians(lat)) * math.sin(
        math.radians(lng))
    z = (RADIUS + h) * math.sin(math.radians(lat))
    return np.array([x, y, z])


# def cal_sun_pos(time_slot, dT):
#     """
#     Calculate the sun's position at a given time

#     Parameters:
#     timestamp: datetime object

#     Returns:
#     numpy.array: sun's position [x, y, z] (km)
#     """

#     planets = load('de421.bsp')
#     earth = planets['earth']
#     sun = planets['sun']

#     ts = load.timescale()
#     t = ts.utc(2025, 6, 1, 
#                0, 0, time_slot * dT)

#     sun_pos = earth.at(t).observe(sun).position.km

#     return sun_pos


def cal_sun_pos(time_slot, dT):
    """
    Calculate the sun's position at a given time without using Skyfield
    
    Parameters:
    time_slot: time slot index
    dT: time step in seconds
    
    Returns:
    numpy.array: sun's position [x, y, z] (km)
    """
    import math
    import numpy as np
    from datetime import datetime, timedelta
    
    # Calculate the date and time
    base_date = datetime(2025, 6, 1, 0, 0, 0)
    current_time = base_date + timedelta(seconds=time_slot * dT)
    
    # Convert to day of year
    day_of_year = current_time.timetuple().tm_yday
    
    # Calculate the orbital elements
    # Mean anomaly of the Earth (in radians)
    M = 2 * math.pi * (day_of_year - 4) / 365.25
    
    # Earth's eccentricity
    e = 0.01671
    
    # Solve Kepler's equation iteratively
    E = M
    for i in range(5):  # Usually converges in a few iterations
        E = M + e * math.sin(E)
    
    # True anomaly
    v = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E/2), math.sqrt(1 - e) * math.cos(E/2))
    
    # Distance from the Sun to the Earth (in AU)
    r = 1.000001018 * (1 - e * math.cos(E))
    
    # Convert to km (1 AU ≈ 149,597,870.7 km)
    r_km = r * 149597870.7
    
    # Calculate the solar coordinates (the negative of Earth's position)
    x = -r_km * math.cos(v)
    y = -r_km * math.sin(v)
    z = 0  # Simplified model assumes Sun lies in Earth's orbital plane
    
    # Add slight inclination to account for Earth's axis tilt
    # This is a simplified approach
    inclination = math.radians(23.44)  # Earth's axial tilt
    y_new = y * math.cos(inclination)
    z_new = y * math.sin(inclination)
    
    return np.array([x, y_new, z_new])


def is_satellite_in_eclipse(satellite_position, sun_position, earth_center=np.array([0, 0, 0])):
    """
    Determine if the satellite is in the Earth's shadow (solar eclipse state)

    Parameters:
    satellite_position: satellite position vector in geocentric Cartesian coordinate system [x, y, z] (km)
    sun_position: sun position vector in geocentric Cartesian coordinate system [x, y, z] (km)
    earth_center: Earth center position, default is coordinate origin [0, 0, 0]

    Returns:
    bool: Returns True if the satellite is in the Earth's shadow, otherwise returns False
    """

    earth_to_sat = satellite_position - earth_center
    sat_distance = np.linalg.norm(earth_to_sat)
    
    earth_to_sun = sun_position - earth_center
    sun_distance = np.linalg.norm(earth_to_sun)
    
    earth_to_sat_unit = earth_to_sat / sat_distance
    earth_to_sun_unit = earth_to_sun / sun_distance
    
    cos_angle = np.dot(earth_to_sat_unit, earth_to_sun_unit)
    
    if cos_angle < 0:
        sin_angle = np.sqrt(1 - cos_angle**2)
        perpendicular_distance = sat_distance * sin_angle
        
        if perpendicular_distance < RADIUS:
            return True
    
    return False


# def is_land(lat, lon, land_geom):
#     """
#     Determines whether the given longitude and latitude is on land

#     Parameters:
#     lat: latitude (degrees)
#     lon: longitude (degrees)
#     land_geom: preprocessed land geometry

#     Return:
#     Boolean value, True means on land, False means on the ocean
#     """
#     point = sgeom.Point(lon, lat)
#     return land_geom.contains(point)


# def load_land_geometry():
#     """
#     Load global land geometry data

#     Returns:
#     Preprocessed land geometry
#     """
#     land_shp_fname = shpreader.natural_earth(
#         resolution='10m', category='physical', name='land')
    
#     land_geom = list(shpreader.Reader(land_shp_fname).geometries())
#     land_geom = sgeom.MultiPolygon(land_geom)
    
#     return prep(land_geom)

def simplified_is_land(lat, lon):
    """
    Simplified version of the land judgment function, based on a simple approximation of the latitude and longitude range

    Parameters:
    lat: latitude (degrees)
    lon: longitude (degrees)

    Return:
    Boolean value, returns True if it is estimated to be on land, otherwise returns False
    """
    continents = [
        {'lat_min': 35, 'lat_max': 70, 'lon_min': -10, 'lon_max': 180},
        {'lat_min': 0, 'lat_max': 35, 'lon_min': 30, 'lon_max': 150},
        {'lat_min': -35, 'lat_max': 35, 'lon_min': -20, 'lon_max': 55},
        {'lat_min': 15, 'lat_max': 70, 'lon_min': -170, 'lon_max': -50},
        {'lat_min': -55, 'lat_max': 15, 'lon_min': -80, 'lon_max': -35},
        {'lat_min': -40, 'lat_max': -10, 'lon_min': 110, 'lon_max': 155},
        {'lat_min': -90, 'lat_max': -60, 'lon_min': -180, 'lon_max': 180}
    ]
    
    for continent in continents:
        if (continent['lat_min'] <= lat <= continent['lat_max'] and 
            continent['lon_min'] <= lon <= continent['lon_max']):
            return True
    
    for continent in continents:
        if (continent['lat_min']-5 <= lat <= continent['lat_max']+5 and 
            continent['lon_min']-5 <= lon <= continent['lon_max']+5):
            return np.random.random() < 0.3
    
    return False


def energy_cal(sat_id, downlink_traffic, uplink_traffic, isl_send, isl_rec):
    """
    Calculate the energy consumption for a satellite using two separate ISL systems:
    Radio ISL and Laser ISL

    Parameters:
    sat_id: Satellite ID
    downlink_traffic: Downlink traffic per satellite
    uplink_traffic: Uplink traffic per satellite
    isl_send: ISL sending traffic per satellite
    isl_rec: ISL receiving traffic per satellite

    Returns:
    tuple: (total_energy, radio_isl_energy, laser_isl_energy)
    """
    
    # GSL parameters (same for both Radio and Laser models)
    gsl_transmitter_idle = 40
    gsl_transmitter_active = 200
    gsl_transmitter_w = 0.01
    gsl_receiver_idle = 40
    gsl_receiver_active = 100
    gsl_receiver_w = 0.008
    
    # Radio ISL parameters
    radio_isl_transmitter_idle = 20
    radio_isl_transmitter_active = 100
    radio_isl_transmitter_w = 0.005
    radio_isl_receiver_idle = 20
    radio_isl_receiver_active = 50
    radio_isl_receiver_w = 0.004
    
    # Laser ISL parameters
    laser_isl_transmitter_idle = 10
    laser_isl_transmitter_active = 50
    laser_isl_transmitter_w = 0.0025
    laser_isl_receiver_idle = 10
    laser_isl_receiver_active = 25
    laser_isl_receiver_w = 0.002
    
    downlink_energy = 0
    uplink_energy = 0
    radio_isl_send = 0
    radio_isl_rec = 0
    laser_isl_send = 0
    laser_isl_rec = 0

    # Calculate GSL energy consumption
    if downlink_traffic[sat_id] > 0:
        downlink_energy = gsl_transmitter_active + gsl_transmitter_w * downlink_traffic[sat_id]
    else:
        downlink_energy = gsl_transmitter_idle
    
    if uplink_traffic[sat_id] > 0:
        uplink_energy = gsl_receiver_active + gsl_receiver_w * uplink_traffic[sat_id]
    else:
        uplink_energy = gsl_receiver_idle
    
    gsl_energy = downlink_energy + uplink_energy
    
    # Calculate Radio ISL energy consumption
    if isl_send[sat_id] > 0:
        radio_isl_send = radio_isl_transmitter_active + radio_isl_transmitter_w * isl_send[sat_id]
    else:
        radio_isl_send = radio_isl_transmitter_idle
    
    if isl_rec[sat_id] > 0:
        radio_isl_rec = radio_isl_receiver_active + radio_isl_receiver_w * isl_rec[sat_id]
    else:
        radio_isl_rec = radio_isl_receiver_idle
    
    radio_energy = radio_isl_send + radio_isl_rec + gsl_energy
    
    # Calculate Laser ISL energy consumption
    if isl_send[sat_id] > 0:
        laser_isl_send = laser_isl_transmitter_active + laser_isl_transmitter_w * isl_send[sat_id]
    else:
        laser_isl_send = laser_isl_transmitter_idle
    
    if isl_rec[sat_id] > 0:
        laser_isl_rec = laser_isl_receiver_active + laser_isl_receiver_w * isl_rec[sat_id]
    else:
        laser_isl_rec = laser_isl_receiver_idle
    
    laser_energy = laser_isl_send + laser_isl_rec + gsl_energy
    
    return radio_energy, laser_energy




def positive_grid_energy_drain(constellation, time_slot, dT=30, bot_num=500, unit_traffic=20, base_power=1000):
    """
    Parameters:
    - constellation: The constellation object containing the satellite network parameters
    - time_slot: Current time slot of the simulation
    - dT: Time step in seconds (default: 30)
    - bot_num: Number of malicious terminals (bots) to deploy per targeted satellite (default: 500)
    - unit_traffic: Traffic generated by each malicious terminal in Mbps (default: 20)
    - base_power: Base power consumption for satellites in W (default: 1000)

    Operation:
    1. Loads constellation parameters and traffic data for the given time slot
    2. Calculates satellite positions and sun position to determine which satellites are in eclipse
    3. For each satellite in the constellation:
       - Calculates original energy consumption without attack
       - If satellite is in eclipse (on battery power), performs attack by:
         * Adding malicious bot traffic to uplinks/downlinks if over land areas
         * Adding malicious traffic to ISLs (inter-satellite links) in all cases
       - Calculates new energy consumption with attack traffic
    4. Computes energy drain effects for both radio and laser communication systems
    5. Saves attack results and modified traffic data to output files

    Return:
    - None (Results are saved to files in the specified directory)

    Outputs:
    The function saves multiple files under two directories:
    1. data/{constellation_name}_energy_drain/attack_traffic_{bot_num}/{time_slot}/:
       - Modified traffic data files (downlink, uplink, ISL traffic)

    2. data/{constellation_name}_energy_drain/energy_{bot_num}/{time_slot}/:
       - Original and attack energy consumption for radio and laser systems
       - Energy consumption with and without base power included

    Notes:
    - The attack specifically targets satellites in eclipse when they rely on limited battery power
    - Different traffic allocation strategies are used for satellites over land vs. over oceans
    - For satellites over land, the attack balances GSL (ground-to-satellite link) and ISL traffic
    - For satellites over oceans, the attack focuses exclusively on ISL traffic
    - Energy calculations consider idle power, active power, and traffic-dependent power for each subsystem
    """

    cons_name = constellation.constellation_name
    shell = constellation.shells[0]
    orbit_num = shell.number_of_orbits
    sat_per_cycle = shell.number_of_satellite_per_orbit
    cons_sat_num = orbit_num * sat_per_cycle

    np.random.seed(42)

    sat_pos_car = []
    ori_radio_energy = []
    ori_laser_energy = []
    attack_radio_energy = []
    attack_laser_energy = []
    ori_all_radio_energy = []
    attack_all_radio_energy = []
    ori_all_laser_energy = []
    attack_all_laser_energy = []

    base_path = os.path.join("data", cons_name + '_link_traffic_data', str(time_slot))

    downgsl_filename = os.path.join(base_path, 'downlink_traffic.txt')
    downlink_traffic = np.loadtxt(downgsl_filename)
    downlink_traffic = list(map(int, downlink_traffic))

    upgsl_filename = os.path.join(base_path, 'uplink_traffic.txt')
    uplink_traffic = np.loadtxt(upgsl_filename)
    uplink_traffic = list(map(int, uplink_traffic))

    isl_filename = os.path.join(base_path, 'isl_traffic.txt')
    isl_traffic = np.loadtxt(isl_filename)
    isl_traffic = list(map(int, isl_traffic))

    isl_send_filename = os.path.join(base_path, 'isl_sender_traffic.txt')
    isl_send = np.loadtxt(isl_send_filename)
    isl_send = list(map(int, isl_send))

    isl_rec_filename = os.path.join(base_path, 'isl_receiver_traffic.txt')
    isl_rec = np.loadtxt(isl_rec_filename)
    isl_rec = list(map(int, isl_rec))


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
    
    sun_pos = cal_sun_pos(time_slot, dT)
    # land_geom = load_land_geometry()

    
    for sat_id in range(cons_sat_num):
        sat_pos = sat_pos_car[sat_id]
        if not is_satellite_in_eclipse(sat_pos, sun_pos):
            ori_radio_energy.append(0)
            ori_laser_energy.append(0)
            attack_radio_energy.append(0)
            attack_laser_energy.append(0)
            ori_all_radio_energy.append(0)
            attack_all_radio_energy.append(0)
            ori_all_laser_energy.append(0)
            attack_all_laser_energy.append(0)
            continue

        ori_energy = energy_cal(sat_id, downlink_traffic, uplink_traffic, isl_send, isl_rec)
        ori_radio_energy.append(ori_energy[0] * dT)
        ori_laser_energy.append(ori_energy[1] * dT)
        ori_all_radio_energy.append(ori_energy[0] * dT + base_power * dT)
        ori_all_laser_energy.append(ori_energy[1] * dT + base_power * dT)
        
        # if simplified_is_land(sat_pos[0], sat_pos[1]):
        #     uplink_traffic[sat_id] += bot_num * 0.2 * unit_traffic
        #     downlink_traffic[sat_id] += bot_num * 0.2 * unit_traffic
        #     isl_traffic[sat_id] += bot_num * 0.8 * unit_traffic
        #     isl_send[sat_id] += bot_num * 0.8 * unit_traffic
        #     isl_rec[sat_id] += bot_num * 0.8 * unit_traffic
        # else:
        #     isl_traffic[sat_id] += bot_num * unit_traffic
        #     isl_send[sat_id] += bot_num * unit_traffic
        #     isl_rec[sat_id] += bot_num * unit_traffic

        if simplified_is_land(sat_pos[0], sat_pos[1]):
            current_traffic = bot_num * unit_traffic
            GS_traffic = max(0, 4096-uplink_traffic[sat_id], 4096-downlink_traffic[sat_id])
            current_traffic -= GS_traffic
            uplink_traffic[sat_id] += GS_traffic
            downlink_traffic[sat_id] += GS_traffic
            isl_traffic[sat_id] += current_traffic
            isl_send[sat_id] += current_traffic
            isl_rec[sat_id] += current_traffic

            # uplink_traffic[sat_id] += bot_num * 0.2 * unit_traffic
            # downlink_traffic[sat_id] += bot_num * 0.2 * unit_traffic
            # isl_traffic[sat_id] += bot_num * 0.8 * unit_traffic
            # isl_send[sat_id] += bot_num * 0.8 * unit_traffic
            # isl_rec[sat_id] += bot_num * 0.8 * unit_traffic
        else:
            isl_traffic[sat_id] += bot_num * unit_traffic
            isl_send[sat_id] += bot_num * unit_traffic
            isl_rec[sat_id] += bot_num * unit_traffic
    
        attack_energy = energy_cal(sat_id, downlink_traffic, uplink_traffic, isl_send, isl_rec)
        attack_radio_energy.append(attack_energy[0] * dT)
        attack_laser_energy.append(attack_energy[1] * dT)
        attack_all_radio_energy.append(attack_energy[0] * dT + base_power * dT)
        attack_all_laser_energy.append(attack_energy[1] * dT + base_power * dT)

    output_path = os.path.join(
        "data",
        cons_name + "_energy_drain",
        "attack_traffic_" + str(bot_num),
        str(time_slot)
    )
    os.makedirs(output_path, exist_ok=True)

    downlink_traffic = np.array(downlink_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, "downlink_traffic.txt"), downlink_traffic, fmt='%d')
    uplink_traffic = np.array(uplink_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, "uplink_traffic.txt"), uplink_traffic, fmt='%d')
    isl_traffic = np.array(isl_traffic, dtype=int)
    np.savetxt(os.path.join(output_path, "isl_traffic.txt"), isl_traffic, fmt='%d')
    isl_send = np.array(isl_send, dtype=int)
    np.savetxt(os.path.join(output_path, "isl_send.txt"), isl_send, fmt='%d')
    isl_rec = np.array(isl_rec, dtype=int)
    np.savetxt(os.path.join(output_path, "isl_rec.txt"), isl_rec, fmt='%d')

    output_path = os.path.join(
        "data",
        f"{cons_name}_energy_drain",
        f"energy_{bot_num}",
        str(time_slot)
    )
    os.makedirs(output_path, exist_ok=True)

    ori_radio_energy = np.array(ori_radio_energy)
    np.savetxt(os.path.join(output_path, 'ori_radio_energy.txt'), ori_radio_energy, fmt='%.3f')
    ori_laser_energy = np.array(ori_laser_energy)
    np.savetxt(os.path.join(output_path, 'ori_laser_energy.txt'), ori_laser_energy, fmt='%.3f')
    attack_radio_energy = np.array(attack_radio_energy)
    np.savetxt(os.path.join(output_path, 'attack_radio_energy.txt'), attack_radio_energy, fmt='%.3f')
    attack_laser_energy = np.array(attack_laser_energy)
    np.savetxt(os.path.join(output_path, 'attack_laser_energy.txt'), attack_laser_energy, fmt='%.3f')
    ori_all_radio_energy = np.array(ori_all_radio_energy)
    np.savetxt(os.path.join(output_path, 'ori_all_radio_energy.txt'), ori_all_radio_energy, fmt='%.3f')
    attack_all_radio_energy = np.array(attack_all_radio_energy)
    np.savetxt(os.path.join(output_path, 'attack_all_radio_energy.txt'), attack_all_radio_energy, fmt='%.3f')
    ori_all_laser_energy = np.array(ori_all_laser_energy)
    np.savetxt(os.path.join(output_path, 'ori_all_laser_energy.txt'), ori_all_laser_energy, fmt='%.3f')
    attack_all_laser_energy = np.array(attack_all_laser_energy)
    np.savetxt(os.path.join(output_path, 'attack_all_laser_energy.txt'), attack_all_laser_energy, fmt='%.3f')

    # print("Complete an energy drain attack at timeslot", str(time_slot))
