'''

Author : yunanhou

Date : 2023/12/16

Function : the shortest path routing test cases at two locations under Constellation +Gird working mode

'''
import src.TLE_constellation.constellation_entity.user as USER
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_routing.routing_policy_plugin_manager as routing_policy_plugin_manager


def shortest_path():
    dT = 5730
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation, dT)
    # initialize the routing policy plugin manager
    routingPolicyPluginManager = routing_policy_plugin_manager.routing_policy_plugin_manager()
    # execute the routing policy
    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source, target,
                                                                     constellation.shells[4])

    print("\t\t\tThe shortest path routing from ", source.user_name, " to ", target.user_name, " is " , minimum_path)
    # modify the source of the communication pair
    source = USER.user(116.41, 39.9, "Beijing")

    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source, target,
                                                                     constellation.shells[4])
    print("\t\t\tThe shortest path routing from ", source.user_name, " to ", target.user_name, " is " , minimum_path)

if __name__ == "__main__":
    shortest_path()