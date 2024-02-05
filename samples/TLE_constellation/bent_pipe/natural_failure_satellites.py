'''

Author: yunanhou

Date : 2023/12/17

Function : In the bent-pipe working mode of the constellation, the satellite natural damage model is used to destroy
           the constellation and test the performance of the constellation.

'''
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_highsurvivability.damage_model_plugin_manager as constellation_damage_model_plugin_manager
import src.TLE_constellation.constellation_entity.user as USER
import src.TLE_constellation.constellation_evaluation.not_exists_ISL.delay as DELAY
import src.TLE_constellation.constellation_evaluation.not_exists_ISL.coverage as COVERAGE
import src.TLE_constellation.constellation_evaluation.not_exists_ISL.bandwidth as BANDWIDTH




def natural_failure_satellites():
    dT = 1000
    constellation_name = "Starlink"
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # generate the bent-pipe constellations
    bent_pipe_constellation = constellation_configuration.constellation_configuration(dT,
                                                                                      constellation_name=constellation_name)
    # modify and execute the constellation connection mode
    connectionModePluginManager.current_connection_mode = "bent_pipe"
    connectionModePluginManager.execute_connection_policy(constellation=bent_pipe_constellation, dT=dT)

    # initialize the constellation damage model plugin manager
    constellationDamageModelPluginManager = constellation_damage_model_plugin_manager.damage_model_plugin_manager()
    # switch the constellation destruction model to natural_failure_satellites
    constellationDamageModelPluginManager.current_damage_model = "natural_failure_satellites"
    # execute constellation destruction model
    constellation_natural_failure = constellationDamageModelPluginManager. \
        execute_damage_model(bent_pipe_constellation, bent_pipe_constellation.shells[4], 0.05, dT)

    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # the ground station and POP point data file paths
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    POP_file = "config/POPs/" + constellation_name + ".xml"

    # latency comparison of the two constellations before and after destruction
    delay1 = DELAY.delay(source, target, dT, bent_pipe_constellation.shells[4], ground_station_file, POP_file)
    print("\t\t\tThe delay time of original constellation from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay1, " s")
    delay2 = DELAY.delay(source, target, dT, constellation_natural_failure.shells[4], ground_station_file, POP_file)
    print("\t\t\tThe delay time of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay2, " s")

    # coverage rate comparison of the two constellations before and after destruction
    coverage1 = COVERAGE.coverage(dT, bent_pipe_constellation.shells[4], ground_station_file)
    print("\t\t\tThe coverage rates of every timeslot of the original constellation are ", coverage1)
    coverage2 = COVERAGE.coverage(dT, constellation_natural_failure.shells[4], ground_station_file)
    print("\t\t\tThe coverage rates of every timeslot of after executing the constellation destruction model are ", coverage2)

    # bandwidth comparison of the two constellations before and after destruction
    bandwidth1 = BANDWIDTH.bandwidth(source, target, dT, bent_pipe_constellation.shells[4], ground_station_file)
    print("\t\t\tThe average bandwidth of all timeslots of original constellation from ", source.user_name, " to ", target.user_name, " is ", bandwidth1)
    bandwidth2 = BANDWIDTH.bandwidth(source, target, dT, constellation_natural_failure.shells[4], ground_station_file)
    print("\t\t\tThe average bandwidth of all timeslots of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " is ", bandwidth2)



if __name__ == "__main__":
    natural_failure_satellites()