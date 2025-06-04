'''

Author : yunanhou

Date : 2025/06/04

Function : Given the minimum elevation Angle of the satellite visible from the ground and the name of the
           constellation (it is necessary to ensure that there is an xml file with the same name under config/XML_constellation),
           this script can calculate the coverage of the polar orbit constellation.
           Principle: Calculate the position of the satellite in each time slice, then randomly select 1000 coordinate points from
           the ground, and calculate the coverage rate based on the coverage of these coordinate points by the constellation.

'''
from global_land_mask import globe
import random
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import math



def judgePointToSatellite(sat_x , sat_y , sat_z , point_x , point_y , point_z , minimum_elevation):
    A = 1.0 * point_x * (point_x - sat_x) + point_y * (point_y - sat_y) + point_z * (point_z - sat_z)
    B = 1.0 * math.sqrt(point_x * point_x + point_y * point_y + point_z * point_z)
    C = 1.0 * math.sqrt(math.pow(sat_x - point_x, 2) + math.pow(sat_y - point_y, 2) + math.pow(sat_z - point_z, 2))
    angle = math.degrees(math.acos(A / (B * C))) # find angles and convert radians to degrees
    if angle < 90 + minimum_elevation or math.fabs(angle - 90 - minimum_elevation) <= 1e-6:
        return False
    else:
        return True



def latilong_to_descartes(satellite_latitude, satellite_longitude, satellite_altitude):
    a = 6371000.0
    e2 = 0.00669438002290
    longitude = math.radians(satellite_longitude)
    latitude = math.radians(satellite_latitude)
    fac1 = 1 - e2 * math.sin(latitude) * math.sin(latitude)
    N = a / math.sqrt(fac1)
    # the unit of satellite height above the ground is meters
    h = satellite_altitude * 1000
    X = (N + h) * math.cos(latitude) * math.cos(longitude)
    Y = (N + h) * math.cos(latitude) * math.sin(longitude)
    Z = (N * (1 - e2) + h) * math.sin(latitude)
    return X, Y, Z




# Enter the latitude and longitude to determine whether you are on land
def is_land(latitude,longitude):
    return globe.is_land(latitude,longitude)





# parameters:
# θ : the lowest elevation angle at which the user can see the satellite (unit: degrees)
# points : a list of points where the user can see the satellite, each point is a list of [longitude, latitude]
# orbits : a list of orbits in the constellation, each orbit is a list of satellites
# Returns:  the coverage ratios
def polar_constellation_coverage(θ, points, orbits):

    # get the number of timeslot
    number_of_timeslot = len(orbits[0].satellites[0].longitude)

    # initialize the coverage ratio
    coverage_ratio = [0] * number_of_timeslot
    # loop through the points
    for time in range(number_of_timeslot):
        # loop through the points
        # the number of points coveraged in the current timeslot
        number_points_covered = 0
        for point in points:
            longitude = point[0]
            latitude = point[1]

            # convert latitude and longitude to descartes coordinates
            point_x, point_y, point_z = latilong_to_descartes(latitude, longitude, 0)

            # loop through the orbits
            for orbit in orbits:
                flag = False
                # loop through the satellites in the orbit
                for satellite in orbit.satellites:
                    # get the longitude and latitude of the satellite at this time
                    satellite_longitude = satellite.longitude[time]
                    satellite_latitude = satellite.latitude[time]

                    # convert satellite longitude and latitude and height to  xyz
                    satellite_x, satellite_y, satellite_z = latilong_to_descartes(satellite_latitude, satellite_longitude, satellite.altitude[time])

                    # judge whether the point can see the satellite
                    if judgePointToSatellite(satellite_x, satellite_y, satellite_z, point_x, point_y, point_z, θ):
                        number_points_covered += 1
                        flag = True
                        break
                if flag:
                    break

        # calculate the coverage ratio for this timeslot
        coverage_ratio[time] = number_points_covered / len(points)

    # print the coverage ratio
    print(f"Coverage ratio for constellation at {θ} degrees elevation angle : ", min(coverage_ratio))




def start(constellation_name = "Polar", θ = 25):
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT=15,
                                                                            constellation_name=constellation_name)

    points = []
    while len(points) < 1000:
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        points.append([longitude, latitude])


    polar_constellation_coverage(θ, points, constellation.shells[0].orbits)


