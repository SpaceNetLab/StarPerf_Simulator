'''

Author : yunanhou

Date : 2023/11/11

Function : the shortest path routing test cases at two locations under Constellation +Gird working mode

'''

import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_routing.routing_policy_plugin_manager as routing_policy_plugin_manager
import src.XML_constellation.constellation_entity.user as USER

# the shortest path routing test cases at two locations under Constellation +Gird working mode
def shortest_path():
    dT = 5730
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(-99.14, 19.41, "Mexico City")
    # the target of the communication pair
    target = USER.user(2.17, 41.39, "Barcelona")
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT,
                                                                            constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # initialize the routing policy plugin manager
    routingPolicyPluginManager = routing_policy_plugin_manager.routing_policy_plugin_manager()
    # execute the routing policy
    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source, target,
                                              constellation.shells[0])

    print("\t\t\tThe shortest path routing from ", source.user_name, " to ", target.user_name, " is " , minimum_path)
    # modify the source of the communication pair
    source = USER.user(116.41, 39.9, "Beijing")

    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source, target,
                                              constellation.shells[0])
    print("\t\t\tThe shortest path routing from ", source.user_name, " to ", target.user_name, " is " , minimum_path)

if __name__ == "__main__":
    shortest_path()