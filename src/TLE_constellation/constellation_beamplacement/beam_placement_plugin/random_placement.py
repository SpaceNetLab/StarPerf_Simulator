'''

Author: yunanhou

Date : 2023/12/16

Function : This script implements the random beam placement algorithm

           Specifically: each satellite is equipped with n antennas, each antenna can emit a spot beam,
           and then the earth's surface is divided into several cells according to a certain resolution
           using the h3 library. Each spot beam can cover one cell. Then calculate the set of all cells
           visible to each satellite, and then find the cells that are not covered by the beam in the set.
           The satellite randomly selects a cell from these uncovered cells to allocate the beam, indicating
           that the cell is covered by the satellite. If all n antennas of the satellite have been used up,
           or all cells within the visible range of the satellite have been covered, no more beams will be
           allocated to the ground.

           Set the above process to be repeated every dT seconds, so that the simulated constellation occurs
           beam scheduling every dT seconds. For example, when dT=15, it can be used to indicate that Starlink
           beam scheduling occurs every 15 seconds, etc.

'''
import h5py
import h3
import numpy as np
import math
import src.TLE_constellation.constellation_entity.user as USER



# customize a class to represent each ground cell, this class is equivalent to encapsulating the cell of the h3 library.
class Cell:
    def __init__(self, h3id, center_latitude, center_longitude):
        # the h3id in the h3 library corresponding to the current cell is a value of type str.
        self.h3id = h3id
        # latitude of cell center point
        self.center_latitude = center_latitude
        # longitude of cell center point
        self.center_longitude = center_longitude
        # this attribute indicates whether the current cell is covered by a beam, False means it is not covered by any
        # beam, True means it is covered by a beam. This value defaults to False and can be modified to True later.
        self.is_covered = False



# this function is used to convert the longitude and latitude coordinates of ground GS/POP points/user terminals/
# satellites into three-dimensional Cartesian coordinates.
# Parameters:
# transformed_object : the GS class object/satellite class object that needs to be converted
# object_type : the type of the parameter transformed_object. The type of object_type is a string. The value of the
#               string is "GS" or "satellite" or "POP" or "User".
# t : the timeslot number, starting from 1. Among them, when object_type is "GS", this parameter is invalid. When
#     object_type is "satellite", this parameter represents the t-th timeslot of the satellite.
# Return value : the x, y, z coordinates of the converted GS, and xyz are all in meters.
def latilong_to_descartes(transformed_object , object_type , t=None):
    a = 6371000.0
    e2 = 0.00669438002290
    if object_type == "satellite":
        longitude = math.radians(transformed_object.longitude[t - 1])
        latitude = math.radians(transformed_object.latitude[t - 1])
        fac1 = 1 - e2 * math.sin(latitude) * math.sin(latitude)
        N = a / math.sqrt(fac1)
        h = transformed_object.altitude[t - 1] * 1000  # the unit of satellite height above the ground is meters
        X = (N + h) * math.cos(latitude) * math.cos(longitude)
        Y = (N + h) * math.cos(latitude) * math.sin(longitude)
        Z = (N * (1 - e2) + h) * math.sin(latitude)
        return X, Y, Z
    else:
        longitude = math.radians(transformed_object.longitude)
        latitude = math.radians(transformed_object.latitude)
        fac1 = 1 - e2 * math.sin(latitude) * math.sin(latitude)
        N = a / math.sqrt(fac1)
        h = 0  # GS height from the ground, unit is meters
        X = (N + h) * math.cos(latitude) * math.cos(longitude)
        Y = (N + h) * math.cos(latitude) * math.sin(longitude)
        Z = (N * (1 - e2) + h) * math.sin(latitude)
        return X, Y, Z



# Function: given a point on land (user, POP or GS, etc.) and the coordinates of a satellite in the three-dimensional
#           Cartesian system, determine whether the point on land can see the satellite.
# Parameters:
# sat_x, sat_y, sat_z : the xyz coordinates of the satellite in the three-dimensional Cartesian coordinate system
# point_x, point_y, point_z : the xyz coordinates of points on land in the three-dimensional Cartesian coordinate system
# minimum_elevation : the minimum elevation angle at which a point on land can see the satellite
# Return value : True means it can be seen, False means it can't be seen
# Implementation idea: Calculate the vector from the ground point to the satellite and the vector from the ground point
#                to the center of the earth respectively, and then calculate the angle between the two vectors. If the
#                angle is greater than or equal to (90°+minimum_elevation), it means it is visible, otherwise it means
#                it is invisible.
def judgePointToSatellite(sat_x , sat_y , sat_z , point_x , point_y , point_z , minimum_elevation):
    A = 1.0 * point_x * (point_x - sat_x) + point_y * (point_y - sat_y) + point_z * (point_z - sat_z)
    B = 1.0 * math.sqrt(point_x * point_x + point_y * point_y + point_z * point_z)
    C = 1.0 * math.sqrt(math.pow(sat_x - point_x, 2) + math.pow(sat_y - point_y, 2) + math.pow(sat_z - point_z, 2))
    angle = math.degrees(math.acos(A / (B * C))) # calculate angles and convert radians to degrees
    if angle < 90 + minimum_elevation or math.fabs(angle - 90 - minimum_elevation) <= 1e-6:
        return False
    else:
        return True




# Function: Implement satellite beam random scheduling algorithm
# Parameters:
# sh : sh is a shell class object, representing a layer of shell in the constellation
# h3_resolution : the resolution of cells divided by h3 library. The currently supported resolutions are: 0/1/2/3/4
# antenna_count_per_satellite : the number of antennas each satellite is equipped with. This parameter determines how
#                               many spot beams a satellite can emit.
# dT : the beam scheduling time interval. For example, dT=15s means that the beam is scheduled every 15s.
# minimum_elevation : the minimum elevation angle at which a satellite can be seen from a point on the ground
# There are two return values :
# Return value 1: The set of all cells that can be covered by the beam in each timeslot. This is a two-dimensional
#                 list. Each element in it is a one-dimensional list, representing the set of all covered cells in
#                 a certain timeslot.
# Return value 2: Cells, a collection of all cells
def random_placement(sh , h3_resolution , antenna_count_per_satellite , dT , minimum_elevation):
    Cells = []  # used to store all cells, each element inside is a Cell class object
    # read all cells with resolution h3_resolution
    with h5py.File('data/h3_cells_id_res0-4.h5', 'r') as file:
        h3_cells = []
        cells = np.array(file['res' + str(h3_resolution) + '_cells']).tolist()
        for element in cells:
            h3_cells.append(element.decode('utf-8'))
        # the h3_cells collection stores the h3id of all cells, it is a list collection, and the type of each element
        # is str. Now get the latitude and longitude coordinates of the hexagon center of each cell to create a Cell
        # class object
        for c in h3_cells:
            center_latitude, center_longitude = h3.cell_to_latlng(c)
            Cells.append(Cell(h3id=c, center_latitude=center_latitude, center_longitude=center_longitude))

    # Now, the information of all cells has been stored in the Cells list.
    # Calculate each time slice separately, traverse each orbit and each satellite in the sh layer shell within each
    # time slice, find the cells that each satellite can see, and use a list to list all the cells that each satellite
    # can see. Save it, so you will get a list with the same number of satellites. When judging whether a satellite can
    # see a cell, use the longitude and latitude coordinates of the center point of the cell to represent it, that is:
    # create a User class object, which represents a ground user and the user's position is the center point coordinates
    # of the cell. , and then determine whether the satellite and the User are visible. If the satellite can see the
    # User, it means the satellite can see the cell, and the cell is added to the list corresponding to the satellite.
    # The next step is to traverse these lists. If the satellite has remaining antennas that are not used, randomly
    # select an uncovered cell and assign a spot beam (that is, assign an antenna) until all satellite antennas are
    # used up, or all satellites can be seen. cells are covered. After all satellites have performed the above
    # operations, calculate how many cells are covered in total.

    # this is a two-dimensional list, each element of which is a one-dimensional list, representing the set of all
    # cells that can be covered by the beam at each moment.
    covered_cells_per_timeslot = []
    for t in range(1, (int)(sh.orbit_cycle / dT) + 3, 1):
        # define a two-dimensional list, where each element is a list, and each sublist represents all the cells
        # that a satellite can see.
        all_satellites_visible_cells = []
        for satellite in sh.satellites:
            # define a one-dimensional list that represents the set of all cells visible to the current satellite
            satellite_visible_cells = []
            # traverse the Cells
            for cell in Cells:
                # generate a user with the center point of the cell as the position
                user = USER.user(longitude=cell.center_longitude, latitude=cell.center_latitude)
                # get the three-dimensional Cartesian coordinates of user
                user_x, user_y, user_z = latilong_to_descartes(user, "User")
                # get the three-dimensional Cartesian coordinates of the satellite satellite at time t
                sat_x, sat_y, sat_z = latilong_to_descartes(satellite, "satellite", t)
                # determine whether the satellite and user are visible. If visible, add the current cell to
                # satellite_visible_cells.
                if judgePointToSatellite(sat_x, sat_y, sat_z, user_x, user_y, user_z, minimum_elevation):
                    satellite_visible_cells.append(cell)
            # after the current satellite is executed, satellite_visible_cells is added to all_satellites_visible_cells
            all_satellites_visible_cells.append(satellite_visible_cells)

        # all cells visible to all satellites at the current moment are stored in all_satellites_visible_cells.
        # Now beam allocation is performed for all cells visible to each satellite.
        for every_satellite_visible_cells in all_satellites_visible_cells:
            # number of satellite antennas available
            satellite_available_antenna_count = antenna_count_per_satellite
            for every_cell in every_satellite_visible_cells:
                # if every_cell is not covered by any beam and the number of satellite available antennas is greater
                # than 0, then assign an antenna to every_cell
                if (not every_cell.is_covered) and (satellite_available_antenna_count > 0):
                    every_cell.is_covered = True
                    satellite_available_antenna_count = satellite_available_antenna_count - 1
                # if the number of available antennas of the satellite is 0, then the loop is terminated early
                if satellite_available_antenna_count == 0:
                    break

        # at this point in execution, it is completely determined which cells are covered and which cells are not
        # covered at the current moment. All covered cells at the current moment are added to a list.
        current_covered_cells = []
        for every_cell in Cells:
            if every_cell.is_covered:
                current_covered_cells.append(every_cell)

        # at this point, the current_covered_cells collection stores all cells covered by the beam at the current
        # moment. Add the current_covered_cells collection to covered_cells_per_timeslot.
        covered_cells_per_timeslot.append(current_covered_cells)

        # after the execution at the current moment is completed, the is_covered attribute of all cells in Cells
        # needs to be set to False, otherwise it will affect the calculation results of the next timeslot.
        for every_cell in Cells:
            every_cell.is_covered = False

    # after execution, the set of cells that can be covered in each timeslot and the set of all Cells are returned.
    return covered_cells_per_timeslot , Cells
