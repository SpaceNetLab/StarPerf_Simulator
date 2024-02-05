'''

Author : yunanhou

Date : 2023/11/11

Function : Delay test case of constellation in bent-pipe working mode

'''


import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_entity.user as USER
import src.XML_constellation.constellation_evaluation.not_exists_ISL.delay as DELAY


# Delay test case of constellation in bent-pipe working mode
def delay():
    dT=1000
    constellation_name = "Starlink"
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # generate the bent-pipe constellations
    bent_pipe_constellation= constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # modify and execute the constellation connection mode
    connectionModePluginManager.current_connection_mode = "bent_pipe"
    connectionModePluginManager.execute_connection_policy(constellation=bent_pipe_constellation , dT=dT)
    # the source of the communication pair
    source = USER.user(0.00 , 51.30 , "London")
    # the target of the communication pair
    target = USER.user(-74.00 , 40.43 , "NewYork")
    # the ground station and POP point data file paths
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    POP_file = "config/POPs/" + constellation_name + ".xml"
    minimum_delay_time = DELAY.delay(source, target, dT, bent_pipe_constellation.shells[0], ground_station_file, POP_file)
    print("\t\t\tThe delay time from ", source.user_name, " to ", target.user_name, " for every timeslot is ", minimum_delay_time,
          " s")


if __name__ == "__main__":
    delay()