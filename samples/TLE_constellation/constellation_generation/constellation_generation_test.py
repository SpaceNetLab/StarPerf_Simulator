'''

Author : yunanhou

Date : 2023/12/09

Function : This script is used to test whether a constellation can be generated normally.

'''
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration


def constellation_generation_test():
    dT = 1000
    constellation_name = "Starlink"
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    print('\t\t\tDetails of the constellations are as follows :')
    print('\t\t\tThe name of the constellation is : ', constellation.constellation_name)
    print('\t\t\tThere are ', constellation.number_of_shells, ' shell(s) in this constellation')
    print('\t\t\tThe information for each shell is as follows:')
    for sh in constellation.shells:
        print('\t\t\tshell name : ', sh.shell_name)
        print('\t\t\tshell orbit altitude(km) : ', sh.altitude)
        print('\t\t\tThe shell contains ', len(sh.satellites), ' satellites')
        print('\t\t\tThe shell contains ', len(sh.orbits), ' orbits')
        print('\t\t\tshell orbital inclination(°) : ', sh.inclination)
        print('\t\t\tshell orbital period (s) : ', sh.orbit_cycle)
        print('\t\t\t==============================================')


if __name__ == '__main__':
    constellation_generation_test()