'''

Author: yunanhou

Date : 2023/12/15

Function : Betweeness test cases under Constellation +Gird working mode

'''
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_evaluation.exists_ISL.betweeness as BETWEENESS


def betweeness():
    dT = 1000
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation, dT)
    betweeness = BETWEENESS.betweeness(constellation_name, constellation.shells[4])
    print("\t\t\tThe betweeness values of each satellite in the constellation are : ", betweeness)

if __name__ == "__main__":
    betweeness()