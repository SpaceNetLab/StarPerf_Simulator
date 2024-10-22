"""

Author: yunanhou

Date: 2024/03/17

Function: This script is used to calculate the orbital period of a satellite.

Input : Satellite orbital altitude (i.e., the distance from the satellite to the ground, in kilometers)

Output : The orbital period of the satellite (i.e., the time it takes for the satellite to complete one orbit around the Earth, in seconds)

"""
import math


# Parameters :
# alitude : the height of a satellite's orbit above the earth's surface, in kilometers
def satellite_orbital_period(alitude):
    # the Earth's gravitational constant (unit: m^3/kg*s^2)
    G = 6.67430e-11
    # mass of the Earth (unit: kg)
    M = 5.97219e24
    # radius of the earth (km)
    R = 6371
    # calculate the orbital period of the satellite (unit: seconds)
    T = round(2 * math.pi * math.sqrt(math.pow((R+alitude)*1000, 3) / (G * M)))
    return T


print(satellite_orbital_period(1200))