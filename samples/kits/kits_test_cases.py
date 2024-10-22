'''

Author : yunanhou

Date : 2023/11/26

Function : This script is used to test each tool script under "kits/" in starperf 2.0

'''

def kits_test_cases():
    print("\t\t\033[31mTest(01/08) : get the h3id of all cells with h3 library resolution 0-4\033[0m")
    # get the h3id of all cells with h3 library resolution 0-4
    import kits.get_h3_all_cells as GET_ALL_RESOLUTION_CELLS_H3ID
    GET_ALL_RESOLUTION_CELLS_H3ID.get_h3_all_cells()


    print("\t\t\033[31mTest(02/09) : view the h3id of h3 cells\033[0m")
    # view the h3id of h3 cells
    import kits.view_h3id_of_cells as VIEW_H3ID_OF_CELLS
    VIEW_H3ID_OF_CELLS.view_h3id_of_cells()


    print("\t\t\033[31mTest(02/08) : obtain recursively read all groups and datasets in the .h5 file and obtain its tree directory structure\033[0m")
    # obtain recursively read all groups and datasets in the .h5 file and obtain its tree directory structure
    import h5py
    import kits.get_h5file_tree_structure as GET_H5FILE_TREE_STRUCTURE
    with h5py.File('data/TLE_constellation/Starlink.h5', 'r') as file:
        GET_H5FILE_TREE_STRUCTURE.print_hdf5_structure(file)

    print("\t\t\033[31mTest(03/08) : view the h3id of all cells with the specified resolution in \"data/h3_cells_id_res0-4.h5\"\033[0m")
    # view the h3id of all cells with the specified resolution in "data/h3_cells_id_res0-4.h5"
    import kits.print_h3_cells_h3id as PRINT_H3_CELLS_H3ID
    PRINT_H3_CELLS_H3ID.print_h3_cells_h3id(0)

    print("\t\t\033[31mTest(04/08) : read the position matrix data in the h5 file\033[0m")
    # read the position matrix data in the h5 file
    import kits.get_h5file_satellite_position_data as GET_H5FILE_SATELLITE_POSITION_DATA
    GET_H5FILE_SATELLITE_POSITION_DATA.get_h5file_satellite_position_data('data/XML_constellation/Starlink.h5')

    print("\t\t\033[31mTest(05/08) : read the delay matrix data in the h5 file\033[0m")
    # read the delay matrix data in the h5 file
    import kits.get_h5file_satellite_delay_data as GET_H5FILE_SATELLITE_DELAY_DATA
    GET_H5FILE_SATELLITE_DELAY_DATA.get_h5file_satellite_delay_data()

    print("\t\t\033[31mTest(06/08) : download today TLE data\033[0m")
    # download today TLE data
    import kits.download_today_TLE_data as DOWNLOAD_TODAY_TLE_DATA_TEST
    DOWNLOAD_TODAY_TLE_DATA_TEST.download_today_TLE_data(constellation_name = "Starlink")

    print("\t\t\033[31mTest(07/08) : view constellation TLE data\033[0m")
    # view constellation TLE data
    import kits.view_constellation_TLE_data as VIEW_CONSTELLATION_TLE_DATA_TEST
    constellation_name = "Starlink"
    VIEW_CONSTELLATION_TLE_DATA_TEST.view_constellation_TLE_data(constellation_name)

    print("\t\t\033[31mTest(08/08) : draw the sub-satellite point trajectories of all satellites in an orbit as well as the distribution of ground stations and POPs on a world map\033[0m")
    # draw the sub-satellite point trajectories of all satellites in an orbit as well as the distribution of
    # ground stations and POPs on a world map
    import kits.draw_subsatellite_point_track_and_GSs as draw
    draw.draw_subsatellite_point_track_and_GSs()

if __name__ == "__main__":
    kits_test_cases()