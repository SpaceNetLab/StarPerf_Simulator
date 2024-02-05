'''

Author: yunanhou

Date : 2023/12/15

Function : Coverage test cases under Constellation +Gird working mode

'''
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_evaluation.exists_ISL.coverage as COVERAGE


def coverage():
    dT = 1000
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation, dT)
    coverage = COVERAGE.coverage(constellation.constellation_name, dT, constellation.shells[4])
    print("\t\t\tThe coverage rates of the constellation for every timeslot are : " , coverage)
    satellite_in_latitude, satellite_in_longitude = COVERAGE.coverage_aggregated_by_latitude_and_longitude(
        constellation.constellation_name, dT, constellation.shells[4])
    print("\t\t\tThe average number of visible satellites per timeslot is distributed by latitude : ",
          satellite_in_latitude)
    print("\t\t\tThe average number of visible satellites per timeslot is distributed by longitude : ",
          satellite_in_longitude)


if __name__ == "__main__":
    coverage()