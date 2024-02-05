'''

Author: yunanhou

Date : 2023/12/16

Function : Delay test case of constellation in bent-pipe working mode

'''


import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_entity.user as USER
import src.TLE_constellation.constellation_evaluation.not_exists_ISL.delay as DELAY

def delay():
    dT = 1000
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # modify and execute the constellation connection mode
    connectionModePluginManager.current_connection_mode = "bent_pipe"
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # the ground station and POP point data file paths
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    POP_file = "config/POPs/" + constellation_name + ".xml"
    minimum_delay_time = DELAY.delay(source, target, dT, constellation.shells[4], ground_station_file, POP_file)
    print("\t\t\tThe delay time from ", source.user_name, " to ", target.user_name, " for every timeslot is ",
          minimum_delay_time, " s")



if __name__ == "__main__":
    delay()