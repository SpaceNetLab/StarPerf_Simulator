'''

Author : yunanhou

Date : 2023/12/15

Function : This script is used to test the core module functionality of various TLE constellations

'''


def TLE_constellation_test_cases():
    print("\t\t\033[31mTest(01/16) : constellation generation\033[0m")
    # constellation generation test
    import samples.TLE_constellation.constellation_generation.constellation_generation_test as CONSTELLATION_GENERATION_TEST
    CONSTELLATION_GENERATION_TEST.constellation_generation_test()

    print("\t\t\033[31mTest(02/16) : calculate the bandwidth of two locations in +Grid mode\033[0m")
    # calculate the bandwidth of two locations in +Grid mode
    import samples.TLE_constellation.positive_Grid.bandwidth as POSITIVE_GRID_BANDWIDTH_TEST
    POSITIVE_GRID_BANDWIDTH_TEST.bandwidth()

    print("\t\t\033[31mTest(03/16) : calculate the delay between two locations in +Grid mode\033[0m")
    # calculate the delay of two locations in +Grid mode
    import samples.TLE_constellation.positive_Grid.delay as POSITIVE_GRID_DELAY_TEST
    POSITIVE_GRID_DELAY_TEST.delay()

    print("\t\t\033[31mTest(04/16) : calculate the constellation betweenness centrality value betweeness in +Grid mode\033[0m")
    # calculate the constellation betweenness centrality value betweeness in +Grid mode
    import samples.TLE_constellation.positive_Grid.betweeness as POSITIVE_GRID_BETWEENESS_TEST
    POSITIVE_GRID_BETWEENESS_TEST.betweeness()

    print("\t\t\033[31mTest(05/16) : calculate the constellation coverage rate in +Grid mode\033[0m")
    # calculate the constellation coverage rate in +Grid mode
    import samples.TLE_constellation.positive_Grid.coverage as POSITIVE_GRID_COVERAGE_TEST
    POSITIVE_GRID_COVERAGE_TEST.coverage()

    print("\t\t\033[31mTest(06/16) : calculate the bandwidth of two locations in bent-pipe mode\033[0m")
    # calculate the bandwidth of two locations in bent_pipe mode
    import samples.TLE_constellation.bent_pipe.bandwidth as BENT_PIPE_BANDWIDTH_TEST
    BENT_PIPE_BANDWIDTH_TEST.bandwidth()

    print("\t\t\033[31mTest(07/16) : calculate the constellation coverage rate in bent-pipe mode\033[0m")
    # calculate the coverage in bent_pipe mode
    import samples.TLE_constellation.bent_pipe.coverage as BENT_PIPE_COVERAGE_TEST
    BENT_PIPE_COVERAGE_TEST.coverage()

    print("\t\t\033[31mTest(08/16) : calculate the delay between two locations in bent-pipe mode\033[0m")
    # calculate the delay of two locations in bent_pipe mode
    import samples.TLE_constellation.bent_pipe.delay as BENT_PIPE_DELAY_TEST
    BENT_PIPE_DELAY_TEST.delay()

    print("\t\t\033[31mTest(09/16) : calculate the shortest path route in +Grid mode\033[0m")
    # calculate the shortest path route in +Grid mode
    import samples.TLE_constellation.positive_Grid.shortest_path as POSITIVE_GRID_SHORTEST_PATH_ROUTING_TEST
    POSITIVE_GRID_SHORTEST_PATH_ROUTING_TEST.shortest_path()

    print("\t\t\033[31mTest(10/16) : calculate the second shortest path route in +Grid mode\033[0m")
    # calculate the second-shortest path route in +Grid mode
    import samples.TLE_constellation.positive_Grid.second_shortest_path as POSITIVE_GRID_SECOND_SHORTEST_PATH_ROUTING_TEST
    POSITIVE_GRID_SECOND_SHORTEST_PATH_ROUTING_TEST.second_shortest_path()


    print("\t\t\033[31mTest(11/16) : calculate the least hop path route in +Grid mode\033[0m")
    # calculate the least hop path route in +Grid mode
    import samples.TLE_constellation.positive_Grid.least_hop_path as POSITIVE_GRID_LEAST_HOP_PATH_ROUTING_TEST
    POSITIVE_GRID_LEAST_HOP_PATH_ROUTING_TEST.least_hop_path()

    print("\t\t\033[31mTest(12/16) : run the random beam placement module\033[0m")
    # random beam placement test case
    import samples.TLE_constellation.beam_placement.random_placement as RANDOM_PLACEMENT_TEST
    RANDOM_PLACEMENT_TEST.random_placement()

    print("\t\t\033[31mTest(13/16) : test the performance of the constellation after natural satellite damage in +Grid mode\033[0m")
    # constellation performance test after the constellation is in +Grid connection mode and the satellite is naturally
    # damaged and destroys the constellation.
    import samples.TLE_constellation.positive_Grid.natural_failure_satellites as POSITIVE_GRID_NATURAL_FAILURE_SATELLITES_TEST
    POSITIVE_GRID_NATURAL_FAILURE_SATELLITES_TEST.natural_failure_satellites()

    print("\t\t\033[31mTest(14/16) : test the performance of the constellation after natural satellite damage in bent-pipe mode\033[0m")
    # test the performance of the constellation after natural satellite damage in bent-pipe mode
    import samples.TLE_constellation.bent_pipe.natural_failure_satellites as BENT_PIPE_NATURAL_FAILURE_SATELLITES_TEST
    BENT_PIPE_NATURAL_FAILURE_SATELLITES_TEST.natural_failure_satellites()

    print("\t\t\033[31mTest(15/16) : test the performance of the constellation after solar storm destroys in +Grid mode\033[0m")
    # the constellation is in the +Grid connection mode and the constellation performance test is performed after a solar
    # storm destroys satellites in an area.
    import samples.TLE_constellation.positive_Grid.sunstorm_damaged_satellites as POSITIVE_GRID_SUNSTORM_DAMAGED_SATELLITES_TEST
    POSITIVE_GRID_SUNSTORM_DAMAGED_SATELLITES_TEST.sunstorm_damaged_satellites()

    print("\t\t\033[31mTest(16/16) : test the performance of the constellation after solar storm destroys in bent-pipe mode\033[0m")
    # test the constellation performance after a concentrated solar storm destroys satellites in an area in bent-pipe mode
    import samples.TLE_constellation.bent_pipe.sunstorm_damaged_satellites as BENT_PIPE_SUNSTORM_DAMAGED_SATELLITES_TEST
    BENT_PIPE_SUNSTORM_DAMAGED_SATELLITES_TEST.sunstorm_damaged_satellites()



if __name__ == "__main__":
    TLE_constellation_test_cases()