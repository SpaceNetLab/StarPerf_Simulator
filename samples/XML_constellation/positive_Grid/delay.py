'''

Author : yunanhou

Date : 2023/11/11

Function : Delay test cases at two locations under Constellation +Gird working mode

'''

import src.XML_constellation.constellation_entity.user as USER
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_evaluation.exists_ISL.delay as DELAY


# Delay test cases at two locations under Constellation +Gird working mode
def delay():
    dT=5730
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(0.00 , 51.30 , "London")
    # the target of the communication pair
    target = USER.user(-74.00 , 40.43 , "NewYork")
    # generate the constellations
    constellation= constellation_configuration.constellation_configuration(dT=dT, constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation , dT=dT)
    delay = DELAY.delay(constellation.constellation_name, source, target, dT, constellation.shells[0])
    print("\t\t\tThe delay time from " , source.user_name  , " to " , target.user_name , " for every timeslot is " , delay , " s")

if __name__ == "__main__":
    delay()