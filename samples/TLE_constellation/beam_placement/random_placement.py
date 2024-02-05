'''

Author: yunanhou

Date : 2023/12/16

Function : random beam placement algorithm test case in beam placement strategy

'''
import src.TLE_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration
import src.TLE_constellation.constellation_beamplacement.beam_placement_plugin_manager as beam_placement_plugin_manager

def random_placement():
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
    # initialize the beam placement plugin manager
    beamPlacementPluginManager = beam_placement_plugin_manager.beam_placement_plugin_manager()

    # execute the beam placement algorithm and return two values:
    # (1) the first return value is the set of all cells that can be covered by the beam in each timeslot.
    #     it is a two-dimensional list, each element in it is a one-dimensional list, representing the set
    #     of all covered cells in a certain timeslot.
    # (2) the second return value is the collection Cells composed of all cells.

    # h3 cell resolution
    h3_resolution = 1
    # the number of antennas each satellite is equipped with
    antenna_count_per_satellite = 8
    # the minimum elevation angle at which a satellite can be seen from a point on the ground
    minimum_elevation = 25
    covered_cells_per_timeslot, Cells = beamPlacementPluginManager.execute_beamplacement_policy(
        bent_pipe_constellation.shells[4],
        h3_resolution, antenna_count_per_satellite, dT, minimum_elevation)


    # covered_cells_per_timeslot is a two-dimensional list, each element of which is a one-dimensional list,
    # representing the set of all covered cells in a certain timeslot
    print("\t\t\tThe number of cells covered at every timeslot are")
    count = 1
    print("\t\t\t============================================")
    for every_timeslot_covered_cells in covered_cells_per_timeslot:
        # print("\t\t\t============================================")
        print("\t\t\tThe number of cells covered at timeslot-" + str(count) + " is : ",
              len(every_timeslot_covered_cells),
              " , and the total number of cells is : ", len(Cells))
        count += 1
        # print("\t\t\th3id" , "\t" , "the longitude of the center point" , "\t" , "the latitude of the center point")
        # for cell in every_timeslot_covered_cells:
        #    print("\t\t\t", cell.h3id , "\t" , cell.center_longitude , "\t" , cell.center_latitude)
        # print("\t\t\t============================================")
    print("\t\t\t============================================")



if __name__ == "__main__":
    random_placement()