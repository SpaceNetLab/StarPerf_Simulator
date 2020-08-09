# -*- coding: UTF-8 -*-
import sp_utils
import copy
import ctypes

data_folder_path = "constellation_data/"
constellation_lla_location = [];
# constellation_name = 'StarLink';
constellation_name = 'OneWeb';


# describing the lla location information for a specific satellite
class sp_lla_trace:
    def __init__(self):
        self.id = 0
        self.time = 0
        self.latitude = 0
        self.longitude = 0
        self.attitude = 0
        self.speed = 0


def write_satellite_lla_to_csv(LLA_data_per_satellite_list, id):
    csv_file_name = constellation_name.lower() + "/by_satellite/satellite_" + str(id) + ".csv";
    sp_utils.sp_create_file_if_not_exit(csv_file_name);
    f = open(csv_file_name, "w+")
    for lla_sample in LLA_data_per_satellite_list:
        line = str(lla_sample.id) + "," + str(lla_sample.time) + "," + str(lla_sample.latitude) \
               + "," + str(lla_sample.longitude) + "," + str(lla_sample.attitude) + "," + str(lla_sample.speed) + "\n";
        f.write(line);
    f.flush();
    f.close();


def write_satellite_lla_by_time(ts, lla_sample_list):
    csv_file_name = constellation_name.lower() + "/by_slots/" + str(ts) + ".csv";
    sp_utils.sp_create_file_if_not_exit(csv_file_name);
    f = open(csv_file_name, "w+");
    for lla_sample in lla_sample_list:
        line = str(lla_sample.id) + "," + str(lla_sample.time) + "," + str(lla_sample.latitude) \
               + "," + str(lla_sample.longitude) + "," + str(lla_sample.attitude) + "," + str(lla_sample.speed) + "\n";
        f.write(line);
    f.flush();
    f.close();


def parse_constellation_from_tle():
    return


def parse_constellation_from_lla():
    lla_data_filename = data_folder_path + constellation_name + '-Current-Constellation-LLA.txt';
    satellite_trace_grouped_by_time = {};
    months = sp_utils.sp_month_map();
    id = 0;
    with open(lla_data_filename, errors='ignore') as file:
        lla_data_list = [];
        lla_data_per_satellite_list = [];
        for line in file:
            # LLA location data of each satellite starts with a line with "Time (UTCG)"
            if ("Time (UTCG)" in line):
                # save LLA data already parsed, and start a new list for next satellite
                if (len(lla_data_per_satellite_list)):
                    print("Save %s samples for satellite %s" % (str(len(lla_data_per_satellite_list)), str(id)));
                    lla_data_list.append(copy.deepcopy(lla_data_per_satellite_list));
                    write_satellite_lla_to_csv(lla_data_per_satellite_list, id);
                lla_data_per_satellite_list.clear();
                id = id + 1;
                continue;
            #      Time (UTCG)          Lat (deg)    Lon (deg)     Alt (km)     Lat Rate (deg/sec)    Lon Rate (deg/sec)    Alt Rate (km/sec)
            # 7 Jul 2020 19:00:00.000      -52.162      166.811    570.070856             -0.013114              0.095196             0.005696
            line = line.split();
            if (len(line) == 10):
                sample = sp_lla_trace();
                sample.time = line[2] + "-" + str(months[line[1]]) + "-" + line[0] + "-" + line[3]
                sample.time = sample.time.replace(":", "-");
                sample.time = sample.time.replace(".000", "");
                sample.latitude = line[4];
                sample.longitude = line[5];
                sample.attitude = line[6];
                sample.id = id;
                lla_data_per_satellite_list.append(copy.deepcopy(sample));

                # append satellite LLA location to a certain time slot.
                if (sample.time not in satellite_trace_grouped_by_time.keys()):
                    satellite_trace_grouped_by_time[sample.time] = [];
                satellite_trace_grouped_by_time[sample.time].append(copy.deepcopy(sample));

        # save the last satellite.
        if (len(lla_data_per_satellite_list)):
            print("Save %s samples in for satellite %s" % (str(len(lla_data_per_satellite_list)), str(id)));
            lla_data_list.append(copy.deepcopy(lla_data_per_satellite_list));
            write_satellite_lla_to_csv(lla_data_per_satellite_list, id);
        lla_data_per_satellite_list.clear();
        print("Extract LLA location of %s satellites in total." % str(id));

        # save LLA location trace grouped by time slots
        all_time_slots = satellite_trace_grouped_by_time.keys();
        print("Save LLA location by time slot.");
        for time_slot in all_time_slots:
            write_satellite_lla_by_time(time_slot, satellite_trace_grouped_by_time[time_slot]);
            print("Saving LLA location in %s." % time_slot);
        print("LLA location saved to files.");


def sp_parse_constellation():
    parse_constellation_from_lla()


if __name__ == '__main__':
    sp_parse_constellation()
