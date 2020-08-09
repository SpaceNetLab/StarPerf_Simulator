# -*- coding: UTF-8 -*-
import errno
import h3
import os
from geopy import distance

import sp_topology
import sp_utils

light_of_speed_m_s = 299792458;  # m / s
attenuation_factor = 2 / 3;  # light travels in 2/3 speed of light in free-space
light_of_speed_km_ms = light_of_speed_m_s / (10 ** 6)
constellation_name = 'StarLink';


# constellation_name = 'OneWeb';


class lla_slot_cache_entry:
    def __init__(self):
        self.name = "";
        self.lines = "";


# reference: https://geopy.readthedocs.io/en/stable/#module-geopy.distance
def calculate_distance():
    # prepare the results dict
    distance_results = {}
    rtt_results = {}

    # prepare the data cache
    lla_location_file_lists_by_slots = sp_utils.sp_walkFile((constellation_name.lower() + "/slots/"))
    lla_data_cache = {}
    # load all lla data in memory cache.
    for lla_filename in lla_location_file_lists_by_slots:
        f = open(lla_filename, "r+")
        lines = f.readlines()
        f.close();
        lla_data_cache[lla_filename] = lla_slot_cache_entry();
        lla_data_cache[lla_filename].name = lla_filename;
        lla_data_cache[lla_filename].lines = lines;

    # print(observation_point);
    print(len(sp_topology.ground_station_points));
    print("Start to calculate distance for each observation point.");

    for ob in sp_topology.ground_station_points:
        # for each observation point, find the nearest satellite and distance in every slots
        src_location = (ob.latitude, ob.longitude);
        distance_results[ob.id] = [];
        rtt_results[ob.id] = [];
        # save the results for the current observation point into file
        ob_result_filename = constellation_name.lower() + "/observation_point/" + str(ob.id) + ".csv";
        sp_utils.sp_create_file_if_not_exit(ob_result_filename);
        ob_result_csvfile = open(ob_result_filename, "w+");
        print("Calculating distance from %s." % ob.id);
        lla_location_file_lists_by_slots.sort()
        for lla_filename in lla_location_file_lists_by_slots:
            # f = open(lla_filename, "r+")
            # lines = f.readlines()
            # f.close();
            lines = lla_data_cache[lla_filename].lines;
            ob_distance = float('inf')
            print("Searching the nearest satellite in %s ..." % lla_filename);
            for lla_locations_in_current_slot in lines:
                lla = lla_locations_in_current_slot.split(',');
                daytime = lla[1];
                altitude = lla[4];
                altitude = 550;  # negative value observed in TLE data, should we fix it to 550km?
                dst_location = (lla[2], lla[3]);
                distance_sample = distance.distance(src_location, dst_location).km
                distance_sample = distance_sample + float(altitude)
                if (distance_sample <= ob_distance):
                    ob_distance = distance_sample;
            estimated_RTT_ms = 2 * (ob_distance / light_of_speed_km_ms);
            distance_results[ob.id].append(ob_distance);
            rtt_results[ob.id].append(estimated_RTT_ms);
            print("Closest distance: %s km, estimated latency: %s ms." % (str(ob_distance), str(estimated_RTT_ms)))
            # record = str(ob.id) + "," + str(daytime) + "," + str(ob_distance) + "," + str(estimated_RTT_ms) + "\n"
            record = str(estimated_RTT_ms) + "\n"
            ob_result_csvfile.write(record)
        # save results to csv files
        ob_result_csvfile.flush()
        ob_result_csvfile.close()

    return distance


if __name__ == '__main__':
    print("StarPerf performance assessment.")
