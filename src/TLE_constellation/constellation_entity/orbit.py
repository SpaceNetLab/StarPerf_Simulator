'''

Author : yunanhou

Date : 2023/12/02

Function : This file defines the orbit class for Constellation

'''


class orbit:
    def __init__(self , shell , raan_lower_bound , raan_upper_bound):
        # shell class variables are used to represent the shell to which the current orbit belongs
        self.shell = shell
        # satellites in this orbit
        self.satellites = []
        # the lower and upper bounds of the right ascension of the ascending node of the satellite in this orbit
        self.raan_lower_bound = raan_lower_bound
        self.raan_upper_bound = raan_upper_bound