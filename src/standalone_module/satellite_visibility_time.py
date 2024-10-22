'''

Author : yunanhou

Date : 2023/12/25

Function : This script is used to calculate the length of time that a user on the ground can see the satellite.
           The lowest elevation angle that the user can see of the satellite is θ, the orbital height of the satellite
           is h (unit: kilometers), and the radius of the earth is R (unit: kilometers). Calculate the length of time
           from when the user can see the satellite to when the user cannot see the satellite based on the given parameters.

'''
import math


# Parameters:
# θ : the lowest elevation angle at which the user can see the satellite (unit: degrees)
# h : the height of a satellite's orbit above the earth's surface, in kilometers
def satellite_visibility_time(θ , h):
    # the Earth's gravitational constant (unit: m^3/kg*s^2)
    G = 6.67430e-11
    # mass of the Earth (unit: kg)
    M = 5.97219e24
    # radius of the earth (km)
    R = 6371
    # calculate the orbital period of the satellite (unit: seconds)
    T = 2 * math.pi * math.sqrt(math.pow((R+h)*1000, 3) / (G * M))
    # convert θ from angle to radian
    θ = math.radians(θ)
    # calculate the time the user can see the satellite
    t = 1.0*T/math.pi*(math.pi/2-θ-math.asin(R/(R+h)*math.cos(θ)))

    return t


if __name__ == '__main__':
    print(satellite_visibility_time(25, 550))