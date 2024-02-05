'''

Author : yunanhou

Date : 2023/11/11

Function : Betweeness test cases at two locations under Constellation +Gird working mode

'''

import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_evaluation.exists_ISL.betweeness as BETWEENESS

# Betweeness test cases at two locations under Constellation +Gird working mode
def betweeness():
    dT=5730
    constellation_name = "Starlink"
    # generate the constellations
    constellation= constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation , dT=dT)
    betweeness = BETWEENESS.betweeness(constellation_name, constellation.shells[0])
    print("\t\t\tThe betweeness values of each satellite in the constellation are : " , betweeness)

if __name__ == "__main__":
    betweeness()