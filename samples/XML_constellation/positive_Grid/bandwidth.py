'''

Author : yunanhou

Date : 2023/11/11

Function : Bandwidth test cases at two locations under Constellation +Gird working mode

'''


import src.XML_constellation.constellation_entity.user as USER
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_evaluation.exists_ISL.bandwidth as BANDWIDTH

# Bandwidth test cases at two locations under Constellation +Gird working mode
def bandwidth():
    dT=1000
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(0.00 , 51.30 , "London")
    # the target of the communication pair
    target = USER.user(-74.00 , 40.43 , "NewYork")
    # generate the constellations
    constellation= constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation , dT=dT)
    bandwidth = BANDWIDTH.bandwidth(constellation_name, source, target, constellation.shells[0], 1.1, 5, dT)
    print("\t\t\tThe bandwidth from " , source.user_name  , " to " , target.user_name , " for the average of all timeslots is " , bandwidth)


if __name__ == "__main__":
    bandwidth()