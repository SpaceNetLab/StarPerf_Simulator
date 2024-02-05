'''

Author : yunanhou

Date : 2023/11/11

Function : the second shortest path routing test cases at two locations under Constellation +Gird working mode

'''

import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_routing.routing_policy_plugin_manager as routing_policy_plugin_manager
import src.XML_constellation.constellation_entity.user as USER

# the second shortest path routing test cases at two locations under Constellation +Gird working mode
def second_shortest_path():
    dT = 5730
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT,
                                                                            constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # initialize the routing policy plugin manager
    routingPolicyPluginManager = routing_policy_plugin_manager.routing_policy_plugin_manager()
    # switch the routing policy
    routingPolicyPluginManager.set_routing_policy("second_shortest_path")
    # execute the routing policy
    second_minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source,
                                                                  target, constellation.shells[0])

    print("\t\t\tThe second shortest path routing from ", source.user_name, " to ", target.user_name, " is " , second_minimum_path)

    # modify the source of the communication pair
    source = USER.user(116.41, 39.9, "Beijing")

    second_minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source,
                                                                  target, constellation.shells[0])
    print("\t\t\tThe second shortest path routing from ", source.user_name, " to ", target.user_name, " is " , second_minimum_path)


if __name__ == "__main__":
    second_shortest_path()