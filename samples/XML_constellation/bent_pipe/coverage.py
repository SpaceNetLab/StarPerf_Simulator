'''

Author : yunanhou

Date : 2023/11/11

Function : Coverage rate test case of constellation in bent-pipe working mode

'''

import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_evaluation.not_exists_ISL.coverage as COVERAGE

# Coverage rate test case of constellation in bent-pipe working mode
def coverage():
    dT=1000
    constellation_name = "Starlink"
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # generate the bent-pipe constellations
    bent_pipe_constellation= constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # modify and execute the constellation connection mode
    connectionModePluginManager.current_connection_mode = "bent_pipe"
    connectionModePluginManager.execute_connection_policy(constellation=bent_pipe_constellation , dT=dT)
    # the ground station data file path
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    coverage_rate = COVERAGE.coverage(dT, bent_pipe_constellation.shells[0], ground_station_file)

    print("\t\t\tThe coverage rates of the constellation for every timeslot are : ", coverage_rate)

if __name__ == "__main__":
    coverage()