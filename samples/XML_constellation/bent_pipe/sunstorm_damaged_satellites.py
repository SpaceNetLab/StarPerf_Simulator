'''

Author : yunanhou

Date : 2023/11/15

Function : In the bent-pipe working mode, the constellation performs a test case of a damage model in which solar
           storms focus on destroying satellites in an area.

Note : The test script is generated in +Grid mode when generating constellations, but is executed in bent-pipe mode
       when evaluating specific indicators (latency, bandwidth, coverage). This is because the solar storm damage model
       needs to read .h5 during execution. The delay matrix of the file, and the delay matrix of the .h5 file does not
       exist in bent-pipe mode, and an error will be reported, so +Grid mode is used to generate the constellation, but
       there is no problem using bent-pipe mode for specific evaluation.

'''
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_highsurvivability.damage_model_plugin_manager as constellation_damage_model_plugin_manager
import src.XML_constellation.constellation_entity.user as USER
import src.XML_constellation.constellation_evaluation.not_exists_ISL.delay as DELAY
import src.XML_constellation.constellation_evaluation.not_exists_ISL.coverage as COVERAGE
import src.XML_constellation.constellation_evaluation.not_exists_ISL.bandwidth as BANDWIDTH

def sunstorm_damaged_satellites():
    dT = 1000
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT,
                                                                            constellation_name=constellation_name)
    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)
    # initialize the constellation damage model plugin manager
    constellationDamageModelPluginManager = constellation_damage_model_plugin_manager.damage_model_plugin_manager()
    # execute constellation destruction model
    constellation_sunstorm_damaged = constellationDamageModelPluginManager. \
        execute_damage_model(constellation, constellation.shells[0], 0.05, dT, 230)
    # the source of the communication pair
    source = USER.user(0.00, 51.30, "London")
    # the target of the communication pair
    target = USER.user(-74.00, 40.43, "NewYork")
    # the ground station and POP point data file paths
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    POP_file = "config/POPs/" + constellation_name + ".xml"

    # latency comparison of the two constellations before and after destruction
    delay1 = DELAY.delay(source, target, dT, constellation.shells[0], ground_station_file, POP_file)
    print("\t\t\tThe delay time of original constellation from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay1, " s")
    delay2 = DELAY.delay(source, target, dT, constellation_sunstorm_damaged.shells[0], ground_station_file, POP_file)
    print("\t\t\tThe delay time of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " for every timeslot are : ", delay2, " s")


    # coverage rate comparison of the two constellations before and after destruction
    coverage1 = COVERAGE.coverage(dT, constellation.shells[0], ground_station_file)
    print("\t\t\tThe coverage rates of every timeslot of the original constellation are ", coverage1)
    coverage2 = COVERAGE.coverage(dT, constellation_sunstorm_damaged.shells[0], ground_station_file)
    print("\t\t\tThe coverage rates of every timeslot of after executing the constellation destruction model are ", coverage2)


    # bandwidth comparison of the two constellations before and after destruction
    bandwidth1 = BANDWIDTH.bandwidth(source, target, dT, constellation.shells[0], ground_station_file)
    print("\t\t\tThe average bandwidth of all timeslots of original constellation from ", source.user_name, " to ", target.user_name, " is ", bandwidth1)
    bandwidth2 = BANDWIDTH.bandwidth(source, target, dT, constellation_sunstorm_damaged.shells[0], ground_station_file)
    print("\t\t\tThe average bandwidth of all timeslots of after executing the constellation destruction model from ", source.user_name, " to ", target.user_name, " is ", bandwidth2)


if __name__ == "__main__":
    sunstorm_damaged_satellites()