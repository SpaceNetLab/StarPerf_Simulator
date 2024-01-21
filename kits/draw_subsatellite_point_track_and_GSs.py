'''

Author : yunanhou

Date : 2023/12/06

Function : Given a number of satellites, draw the sub-satellite point trajectories of these satellites within an
           orbital period based on their TLE data.

'''
from datetime import datetime, timedelta
import src.constellation_generation.by_TLE.get_satellite_position as GET_SATELLITE_POSITION
from pyecharts import options as opts
from pyecharts.charts import Geo
import xml.etree.ElementTree as ET
import src.TLE_constellation.constellation_entity.ground_station as GS
import src.TLE_constellation.constellation_entity.POP as POP_POINT
import src.constellation_generation.by_TLE.constellation_configuration as constellation_configuration


# Read xml document
def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

# Read xml document
def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: xml_to_dict(root)}





# Parameter :
# satellites : list type parameter, which stores some satellites. Each element is a
#              "src/TLE_constellation/constellation_entity/orbit.py" class object
# ground_station_file , POP_file : the ground station and POP point data file paths
# dT : how often the satellite position is recorded (unit: seconds)
def draw_subsatellite_point_track_and_GSs():
    dT = 1000
    constellation_name = "Starlink"
    ground_station_file = "config/ground_stations/" + constellation_name + ".xml"
    POP_file = "config/POPs/" + constellation_name + ".xml"
    constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
    satellites = constellation.shells[6].orbits[17].satellites

    # method for calculating satellite orbit period (seconds):
    # there is a field in the JSON format TLE data called "MEAN_MOTION", which means: how many times a satellite can
    # orbit around in one day. Then the reciprocal of this field is how many days it takes to fly around the orbit,
    # and then convert it into seconds
    orbit_period = float('-inf')
    all_satellites_TLE_2LE = []
    for satellite in satellites:
        all_satellites_TLE_2LE.append(satellite.tle_2le[0])
        all_satellites_TLE_2LE.append(satellite.tle_2le[1])
        orbit_period = max(orbit_period , 1/satellite.tle_json["MEAN_MOTION"] * 24 * 60 * 60)
    orbit_period = int(orbit_period)

    moments = []
    start_datetime = datetime.now()
    end_datetime = start_datetime + timedelta(seconds=orbit_period)
    while start_datetime < end_datetime:
        moments.append((start_datetime.year, start_datetime.month, start_datetime.day,
                        start_datetime.hour, start_datetime.minute, start_datetime.second))
        start_datetime += timedelta(seconds=dT)
    moments.append((end_datetime.year, end_datetime.month, end_datetime.day,
                        end_datetime.hour, end_datetime.minute, end_datetime.second))

    all_moments_subsatellite_points_longitude_latitude = []
    for moment in moments:
        moment_subsatellite_points_longitude_latitude = GET_SATELLITE_POSITION.get_satellite_position(
            all_satellites_TLE_2LE,moment[0],moment[1],moment[2],moment[3],moment[4],moment[5])
        all_moments_subsatellite_points_longitude_latitude.append(moment_subsatellite_points_longitude_latitude)

    # read ground base station data
    ground_station = read_xml_file(ground_station_file)
    # generate GS
    GSs = []
    for gs_count in range(1, len(ground_station['GSs']) + 1, 1):
        gs = GS.ground_station(longitude=float(ground_station['GSs']['GS' + str(gs_count)]['Longitude']),
                                latitude=float(ground_station['GSs']['GS' + str(gs_count)]['Latitude']),
                                description=ground_station['GSs']['GS' + str(gs_count)]['Description'],
                                frequency=ground_station['GSs']['GS' + str(gs_count)]['Frequency'],
                                antenna_count=int(ground_station['GSs']['GS' + str(gs_count)]['Antenna_Count']),
                                uplink_GHz=float(ground_station['GSs']['GS' + str(gs_count)]['Uplink_Ghz']),
                                downlink_GHz=float(ground_station['GSs']['GS' + str(gs_count)]['Downlink_Ghz']))
        GSs.append(gs)
    # read ground POP point data
    POP = read_xml_file(POP_file)
    # generate POP
    POPs = []
    for pop_count in range(1, len(POP['POPs']) + 1, 1):
        pop = POP_POINT.POP(longitude=float(POP['POPs']['POP' + str(pop_count)]['Longitude']),
                            latitude=float(POP['POPs']['POP' + str(pop_count)]['Latitude']),
                            POP_name=POP['POPs']['POP' + str(pop_count)]['Name'])
        POPs.append(pop)

    trajectory_GS_POP = Geo()
    trajectory_GS_POP.add_schema(maptype="world")

    for moment_subsatellite_points_longitude_latitude in all_moments_subsatellite_points_longitude_latitude:
        for longitude_latitude in moment_subsatellite_points_longitude_latitude:
            trajectory_GS_POP.add_coordinate("", longitude_latitude[0], longitude_latitude[1])
            trajectory_GS_POP.add("sub-satellite point", [("", 10)],
                                              itemstyle_opts=opts.ItemStyleOpts(color="red"),symbol_size=5)
            trajectory_GS_POP.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    for gs in GSs:
        trajectory_GS_POP.add_coordinate("" , gs.longitude , gs.latitude)
        trajectory_GS_POP.add("GS" , [("", 10)],itemstyle_opts=opts.ItemStyleOpts(color="blue"),symbol_size=5)
    for pop in POPs:
        trajectory_GS_POP.add_coordinate("", pop.longitude, pop.latitude)
        trajectory_GS_POP.add("POP", [("", 10)], itemstyle_opts=opts.ItemStyleOpts(color="green"), symbol_size=5)

    trajectory_GS_POP.set_global_opts(title_opts=opts.TitleOpts(title="sub-satellite point track,GSs and POPs"))
    trajectory_GS_POP.render('data/trajectory_GS_POP.html')
    print("\t\t\tThe trajectory_GS_POP.html.html file has been generated and is located under \"data/\".")

