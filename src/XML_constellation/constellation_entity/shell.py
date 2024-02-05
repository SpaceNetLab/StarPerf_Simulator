'''

Author : yunanhou

Date : 2023/08/24

Function : This file defines one layer of the constellation (that is, the shell). The fields in the class describe some
           information about the shell, including the height of the shell, the number of satellites it contains, the
           number of orbits it contains, etc.

'''

class shell:
    def __init__(self , altitude , number_of_satellites , number_of_orbits , inclination , orbit_cycle ,
                 number_of_satellite_per_orbit , phase_shift , shell_name):
        self.altitude = altitude # height of shell (km)
        self.number_of_satellites = number_of_satellites # the number of satellites included in this shell
        self.number_of_orbits = number_of_orbits  # the number of orbits contained in this shell
        self.inclination = inclination # the inclination angle of the orbit in this shell
        self.orbit_cycle = orbit_cycle # the orbital period of this layer’s shell
        # the number of satellites per orbit in this layer’s shell
        self.number_of_satellite_per_orbit = number_of_satellite_per_orbit
        self.phase_shift = phase_shift # phase shift, used when generating satellites
        # the name of this layer's shell, name format: shell+number, such as: "shell1", "shell2", etc.
        self.shell_name = shell_name
        # a list type object is used to store which orbits are included in the shell of this layer. It stores orbit
        # objects.
        self.orbits = []