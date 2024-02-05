'''

Author: yunanhou

Date : 2023/12/16

Function : the least hop path routing test cases at two locations under Constellation +Gird working mode

'''
import src.TLE_constellation.constellation_entity.user as USER
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.TLE_constellation.constellation_routing.routing_policy_plugin_manager as routing_policy_plugin_manager


def least_hop_path():
    dT = 1000
    constellation_name = "Starlink"
    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # initialize the routing policy plugin manager
    routingPolicyPluginManager = routing_policy_plugin_manager.routing_policy_plugin_manager()
    # switch routing policy
    routingPolicyPluginManager.set_routing_policy("least_hop_path")
    # execute routing policy
    least_hop_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source,
                                                                       target, constellation.shells[4])
    print("\t\t\tThe least hop path from " , source.user_name  , " to " , target.user_name , " is " , least_hop_path)
    # modify the source of the communication pair
    source = USER.user(116.41, 39.9, "Beijing")
    # execute routing policy
    least_hop_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source,
                                                                       target, constellation.shells[4])
    print("\t\t\tThe least hop path from " , source.user_name  , " to " , target.user_name , " is " , least_hop_path)


if __name__ == "__main__":
    least_hop_path()