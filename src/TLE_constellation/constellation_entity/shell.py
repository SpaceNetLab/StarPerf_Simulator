'''

Author : yunanhou

Date : 2023/11/30

Function : This file defines the shell class for Constellation

'''


class shell:
    def __init__(self, altitude, inclination , shell_name):
        self.altitude = altitude # km
        self.inclination = inclination # degree
        # list type variable, each element of which is a satellite class object, this attribute is used to store all
        # satellites in this layer of shell
        self.satellites = []
        # orbits in this layer of shell
        self.orbits = []
        # the orbital period of this layer’s shell
        self.orbit_cycle = None
        # the name of the shell
        self.shell_name = shell_name
