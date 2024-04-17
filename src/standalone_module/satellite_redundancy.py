"""

Author : yunanhou

Date : 2024/04/17

Function : This script is used to calculate the satellite redundancy of a constellation.
           The so-called satellite redundancy refers to how many satellites a ground user
           can see in the sky at a time. In order to better calculate the redundancy of a
           constellation, this script uses the h3 library to divide the earth's surface
           into several hexagons, calculate the number of visible satellites in each
           timeslot from the center point of each hexagon, and finally calculate The
           average of all timeslots is the satellite redundancy of the hexagon in one
           orbital period.

"""
import src.constellation_generation.by_XML.constellation_configuration as XML_constellation_configuration
import src.constellation_generation.by_TLE.constellation_configuration as TLE_constellation_configuration
import h3
import numpy as np
import h5py
import math
import matplotlib.pyplot as plt



class Cell:
    def __init__(self, h3id, center_latitude, center_longitude):
        # the h3id in the h3 library corresponding to the current cell is a value of type str.
        self.h3id = h3id
        # latitude of cell center point
        self.center_latitude = center_latitude
        # longitude of cell center point
        self.center_longitude = center_longitude
        # the number of satellites visible in each timeslot
        self.visible_satellite_count = []
        self.visible_satellite_count_average_per_timeslot = 0





"""
Given the coordinates of a ground point and a satellite in the three-dimensional Cartesian system, determine
whether the ground point can see the satellite.
@param sx      Satellite x coordinate
@param sy      Satellite y coordinate
@param sz      Satellite z coordinate
@param px      point x coordinate
@param py      point y coordinate
@param pz      point z coordinate
@param e        The minimum elevation angle at which the satellite can be seen from the ground
@return        Return true to indicate that it can be seen, false to indicate that it cannot be seen.
"""
def judgePointToSatellite(sx , sy , sz , px , py , pz , e):
    A = px * (px - sx) + py * (py - sy) + pz * (pz - sz)
    B = math.sqrt(px * px + py * py + pz * pz)
    C = math.sqrt(math.pow(sx - px, 2) + math.pow(sy - py, 2) + math.pow(sz - pz, 2))
    angle = math.degrees(math.acos(A / (B * C))) # Find angles and convert radians to degrees
    if angle < 90 + e or abs(angle - 90 - e) <= 1e-6:
        return False
    else:
        return True






"""
Convert the [longitude,latitude,altitude(km)] coordinates of satellites into three-dimensional Cartesian coordinates
@param satellites      [longitude,latitude,altitude(km)] coordinates
@return            Three-dimensional Cartesian coordinates
"""
def LongitudeAndLatitudeToDescartesPoints(satellites):
    result = []

    for sat in satellites:
        R = 6371.0 + sat[2]
        lon_rad = math.radians(sat[0])
        lat_rad = math.radians(sat[1])

        x = R * math.cos(lat_rad) * math.cos(lon_rad)
        y = R * math.cos(lat_rad) * math.sin(lon_rad)
        z = R * math.sin(lat_rad)
        result.append([x, y, z])

    return result



# Parameters:
# h3_resolution : int : the resolution of h3 library
# constellation_name : str : the name of the constellation
# dT : int : the time interval of the constellation
# type : str : the type of the constellation, either "TLE" or "XML"
# min_elevation_angle : float : the minimum elevation angle at which the satellite can be seen
#                               from a ground point
def satellite_redundancy(h3_resolution , constellation_name , dT , type , min_elevation_angle = 25):

    # generate the constellation
    if type == "TLE":
        constellation = TLE_constellation_configuration.constellation_configuration(
            dT=dT, constellation_name=constellation_name)
    else:
        constellation = XML_constellation_configuration.constellation_configuration(
            dT=dT, constellation_name=constellation_name)

    # get the orbit cycle of the constellation
    orbit_cycle = min([sh.orbit_cycle for sh in constellation.shells])


    # get h3 hexagon center point
    Cells = []
    with h5py.File('data/h3_cells_id_res0-4.h5', 'r') as file:
        h3_cells = []
        cells = np.array(file['res' + str(h3_resolution) + '_cells']).tolist()
        for element in cells:
            h3_cells.append(element.decode('utf-8'))

        for c in h3_cells:
            center_latitude, center_longitude = h3.cell_to_latlng(c)
            Cells.append(Cell(h3id=c, center_latitude=center_latitude, center_longitude=center_longitude))


    # calculate the number of visible satellites at each timeslot for each cell center point
    for t in range(1, (int)(orbit_cycle / dT) + 2, 1):
        # Get the position information of all satellites in the current timeslot constellation and
        # store it in a list object. The location information format here is
        # [longitude, latitude, altitude (km)]

        satellite_positions = []
        with h5py.File("data/"+type+"_constellation/"+constellation_name+".h5",
                       'r') as file:
            position = file['position']
            for shell_index in range(1 , len(constellation.shells)+1,1):
                data = np.array(position['shell'+str(shell_index)]['timeslot'+str(t)]).tolist()
                data = [element.decode('utf-8') for row in data for element in row]
                data = [data[i:i + 3] for i in range(0, len(data), 3)]
                data = [[float(element) for element in row] for row in data]
                satellite_positions = satellite_positions + data


        # convert [longitude, latitude, altitude] coordinates to three-dimensional Cartesian coordinates
        satellite_positions = LongitudeAndLatitudeToDescartesPoints(satellite_positions)


        for cell in Cells:
            visible_satellite_count = 0
            center_point_xyz = LongitudeAndLatitudeToDescartesPoints([[cell.center_longitude,cell.center_latitude,0]])
            for sat in satellite_positions:
                # judge whether the point can see the satellite
                if judgePointToSatellite(sat[0],sat[1],sat[2],center_point_xyz[0][0],center_point_xyz[0][1],
                                      center_point_xyz[0][2],min_elevation_angle):
                    visible_satellite_count += 1
            cell.visible_satellite_count.append(visible_satellite_count)

    for cell in Cells:
        cell.visible_satellite_count_average_per_timeslot = (
                sum(cell.visible_satellite_count)/len(cell.visible_satellite_count))
        print("The average number of visible satellites in the hexagon with h3id " + cell.h3id + " is " +
              str(sum(cell.visible_satellite_count)/len(cell.visible_satellite_count)) + " in one orbital period.")

    visible_satellite_count = [c.visible_satellite_count_average_per_timeslot for c in Cells]

    plt.hist(visible_satellite_count, bins=len(set(visible_satellite_count)), edgecolor='black', alpha=0.7)

    # 添加标题和标签
    plt.title(constellation_name)
    plt.xlabel('visible satellite count')
    plt.ylabel('cell count')

    # 添加图例
    plt.legend()

    # 显示图形
    plt.show()