'''

Author: yunanhou

Date : 2023/12/16

Function : Coverage test case of constellation in bent-pipe working mode

'''
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_evaluation.not_exists_ISL.coverage as COVERAGE


def coverage():
    dT = 1000
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # modify and execute the constellation connection mode
    connectionModePluginManager.current_connection_mode = "bent_pipe"
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # the ground station data file path
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    coverage_rate = COVERAGE.coverage(dT, constellation.shells[4], ground_station_file)
    print("\t\t\tThe coverage rates of the constellation for every timeslot are : ", coverage_rate)


if __name__ == "__main__":
    coverage()