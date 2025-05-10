"""

Author : zhifenghan

Date : 2025/05/09

Function :  This script defines the function of generating trajectories. Unlike src/constellaton_generation/
            by_XML/orbit_configuration, it specifies the simulation duration and specifies a single-layer
            network for the simulated constellation instead of the original multi-layer network.

"""

import math
from skyfield.api import load, wgs84, EarthSatellite
from datetime import datetime
from sgp4.api import Satrec, WGS72, WGS84
import numpy as np
import pandas as pd
import src.XML_constellation.constellation_entity.orbit as ORBIT
import src.XML_constellation.constellation_entity.satellite as SATELLITE

# Parameters:
# sh : the shell class object of the orbit to be generated
# dT : how often the position of the constellation satellite is updated. (in seconds)
# duration : simulation duration (in seconds) 
def orbit_configuration(sh, duration, dT):
    a = 6371.0 + sh.altitude # satellite orbit semi-major axis, unit: kilometers
    inc = sh.inclination # orbital inclination, unit is °
    ecc = 0  # orbit eccentricity
    # orbital perigee argument. When the eccentricity ecc=0, the orbit is a standard circle, and the perigee coincides
    # with the ascending node. At this time, the perigee argument is 0.
    argp = 0
    # generate the right ascension of the ascending node of the satellite orbit. The number of orbits in the sh layer
    # shell is the length of raan.
    raan = []
    if inc > 80 and inc < 100:
        raan = [i * (180.0/sh.number_of_orbits) for i in range(sh.number_of_orbits)]
    else:
        raan = [i * (360.0/sh.number_of_orbits) for i in range(sh.number_of_orbits)]
    # generate the angle between two adjacent satellites in the same orbit
    meanAnomaly1 = [i * (360.0/sh.number_of_satellite_per_orbit) for i in range(sh.number_of_satellite_per_orbit)]
    ts = load.timescale()
    since = datetime(1949, 12, 31, 0, 0, 0)
    start = datetime(2023, 10, 1, 0, 0, 0)
    epoch = (start - since).days  # epoch represents the number of days between the two dates since and start
    inc = inc * 2 * np.pi / 360  # orbital inclination (radians)
    # the Earth's gravitational constant is equal to the Earth's mass times the universal gravitational constant
    GM = 3.9860044e14
    # radius of the Earth (meters)
    R = 6371393
    altitude = sh.altitude * 1000  # orbit height (meters)
    mean_motion = np.sqrt(GM / (R + altitude) ** 3) * 60  # average satellite speed
    num_of_orbit = sh.number_of_orbits  # number of orbit
    sat_per_orbit = sh.number_of_satellite_per_orbit  # number of satellites per orbit
    num_of_sat = num_of_orbit * sat_per_orbit  # total number of satellites
    F = 1
    total_timestamps = range(0, duration, dT)

    for i in range(1, sh.number_of_orbits+1, 1):
        orbit = ORBIT.orbit(a=a, ecc=ecc, inc=inc, raan=raan[i - 1], argp = argp)
        for j in range(1 , sh.number_of_satellite_per_orbit+1 , 1):
            # generate each satellite here... After generating the satellite, add each satellite to the satellites
            # attribute of the orbit object.
            nu = meanAnomaly1[j-1]  # satellite's true approach angle
            satrec = Satrec()
            satrec.sgp4init(
                WGS84,  # coordinate system
                'i',  # 'a' = old AFSPC mode, 'i' = improved mode
                i * sat_per_orbit + j,  # satnum: Satellite number
                epoch,  # epoch: days since 1949 December 31 00:00 UT
                2.8098e-05,  # bstar: drag coefficient (/earth radii)
                6.969196665e-13,  # ndot: ballistic coefficient (revs/day)
                0.0,  # nddot: second derivative of mean motion (revs/day^3)
                0.001,  # ecco: eccentricity
                0.0,  # argpo: argument of perigee (radians)
                inc,  # inclo: inclination (radians)
                math.radians(nu),  # mo: mean anomaly (radians)
                mean_motion,  # no_kozai: mean motion (radians/minute)
                math.radians(raan[i-1]),  # nodeo: right ascension of ascending node (radians)
            )
            sat = EarthSatellite.from_satrec(satrec, ts)  # generate satellite object
            # a list containing timestamps within cycle seconds, generating a timestamp every dT seconds
            t_ts = ts.utc(2025, 6, 1, 0, 0, total_timestamps)
            
            geocentric = sat.at(t_ts)
            satellite_position = pd.DataFrame()
            subpoint = wgs84.subpoint(geocentric)
            satellite_position['latitude'] = subpoint.latitude.degrees
            satellite_position['longitude'] = subpoint.longitude.degrees
            satellite_position['altitude'] = subpoint.elevation.km
            satellite = SATELLITE.satellite(nu=nu, orbit=orbit, true_satellite = sat)
            satellite.longitude = list(satellite_position['longitude'].values.tolist())
            satellite.latitude = list(satellite_position['latitude'].values.tolist())
            satellite.altitude = list(satellite_position['altitude'].values.tolist())
            orbit.satellites.append(satellite)
        sh.orbits.append(orbit)