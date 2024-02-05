'''

Author : yunanhou

Date : 2023/11/11

Function : Bandwidth test case of constellation in bent-pipe working mode

'''


import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_entity.user as USER
import src.XML_constellation.constellation_evaluation.not_exists_ISL.bandwidth as BANDWIDTH

# Bandwidth test case of constellation in bent-pipe working mode
def bandwidth():
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
    # the ground station data file path
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    bandwidth = BANDWIDTH.bandwidth(source, target, dT, bent_pipe_constellation.shells[0], ground_station_file)
    print("\t\t\tThe bandwidth from ", source.user_name, " to ", target.user_name,
          " for the average of all timeslots is ", bandwidth)


if __name__ == "__main__":
    bandwidth()