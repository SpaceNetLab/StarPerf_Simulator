'''

Author : yunanhou

Date : 2023/11/11

Function : In the constellation +Grid working mode, the satellite sunstorm damage model is used to destroy the constellation
           and perform constellation performance testing.

'''

import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_highsurvivability.damage_model_plugin_manager as constellation_damage_model_plugin_manager
import src.XML_constellation.constellation_routing.routing_policy_plugin_manager as routing_policy_plugin_manager
import src.XML_constellation.constellation_entity.user as USER
import src.XML_constellation.constellation_evaluation.exists_ISL.bandwidth as BANDWIDTH
import src.XML_constellation.constellation_evaluation.exists_ISL.coverage as COVERAGE
import src.XML_constellation.constellation_evaluation.exists_ISL.delay as DELAY
import src.XML_constellation.constellation_evaluation.exists_ISL.betweeness as BETWEENESS

def sunstorm_damaged_satellites():
    dT=5370
    constellation_name = "Starlink"
    # generate the constellations
    constellation= constellation_configuration.constellation_configuration(dT, constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation , dT=dT)
    # initialize the constellation damage model plugin manager
    constellationDamageModelPluginManager = constellation_damage_model_plugin_manager.damage_model_plugin_manager()
    # execute the constellation destruction model
    constellation_sunstorm_damaged = constellationDamageModelPluginManager.\
        execute_damage_model(constellation , constellation.shells[0] , 0.05 , dT , 230)

    # latency comparison of the two constellations before and after destruction
    # the source of the communication pair
    source = USER.user(116.397128 , 39.916527 , "Beijing")
    # the target of the communication pair
    target = USER.user(-74.00 , 40.43 , "NewYork")
    delay1 = DELAY.delay(constellation.constellation_name, source, target, dT, constellation.shells[0])
    print("\t\t\tThe delay time of original constellation from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay1, " s")
    delay2 = DELAY.delay(constellation_sunstorm_damaged.constellation_name, source, target, dT, constellation_sunstorm_damaged.shells[0])
    print("\t\t\tThe delay time of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay2, " s")


    # comparison of the shortest paths of the two constellations before and after destruction
    # initialize the routing policy plugin manager
    routingPolicyPluginManager = routing_policy_plugin_manager.routing_policy_plugin_manager()
    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation.constellation_name, source, target,
                                              constellation.shells[0])
    print("\t\t\tThe shortest path of original constellation from " , source.user_name  , " to " , target.user_name , " is " , minimum_path)
    minimum_path = routingPolicyPluginManager.execute_routing_policy(constellation_sunstorm_damaged.constellation_name, source, target,
                                              constellation_sunstorm_damaged.shells[0])
    print("\t\t\tThe shortest path of after executing the constellation destruction model from " , source.user_name  , " to " ,
          target.user_name , " is " , minimum_path)


    # coverage rate comparison of the two constellations before and after destruction
    coverage1= COVERAGE.coverage(constellation.constellation_name, dT, constellation.shells[0])
    print("\t\t\tThe coverage rates of every timeslot of the original constellation are ", coverage1)
    coverage2= COVERAGE.coverage(constellation_sunstorm_damaged.constellation_name, dT, constellation_sunstorm_damaged.shells[0])
    print("\t\t\tThe coverage rates of every timeslot of after executing the constellation destruction model are ", coverage2)


    # betweeness value comparison of the two constellations before and after destruction
    betweeness1 = BETWEENESS.betweeness(constellation.constellation_name, constellation.shells[0])
    print("\t\t\tThe betweeness values of each satellite in the original constellation are " , betweeness1)
    betweeness2 = BETWEENESS.betweeness(constellation_sunstorm_damaged.constellation_name, constellation_sunstorm_damaged.shells[0])
    print("\t\t\tThe betweeness values of each satellite in the after executing the constellation destruction model are " , betweeness2)



    # bandwidth comparison of the two constellations before and after destruction
    bandwidth1 = BANDWIDTH.bandwidth(constellation.constellation_name, source, target, constellation.shells[0], 1.1, 5, dT)
    print("\t\t\tThe average bandwidth of all timeslots of original constellation from ", source.user_name, " to ", target.user_name, " is ", bandwidth1)
    bandwidth2 = BANDWIDTH.bandwidth(constellation_sunstorm_damaged.constellation_name, source, target, constellation_sunstorm_damaged.shells[0], 1.1, 5, dT)
    print("\t\t\tThe average bandwidth of all timeslots of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " is ", bandwidth2)


if __name__ == "__main__":
    sunstorm_damaged_satellites()