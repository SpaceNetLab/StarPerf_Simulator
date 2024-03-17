'''

Author : yunanhou

Date : 2023/12/09

Function : Generate and initialize constellation using TLE data

'''
import src.constellation_generation.by_TLE.get_satellite_position as GET_SATELLITE_POSITION
import src.TLE_constellation.constellation_entity.constellation as CONSTELLATION
import src.constellation_generation.by_TLE.download_TLE_data as DOWNLOAD_TLE_DATA
import src.constellation_generation.by_TLE.satellite_to_shell_mapping as SATELLITE_TO_SHELL_MAPPING
import src.constellation_generation.by_TLE.satellite_to_orbit_mapping as SATELLITE_TO_ORBIT_MAPPING
from datetime import datetime, timedelta
import os
import h5py

# Parameters:
# dT : the timeslot, and the timeslot t is calculated from 1
# constellation_name : the name of the constellation to be generated, used to read the TLE data file
def constellation_configuration(dT , constellation_name):
    # download TLE data for the current day
    DOWNLOAD_TLE_DATA.download_TLE_data(constellation_name)
    # establish the correspondence between satellites and shells
    shells = SATELLITE_TO_SHELL_MAPPING.satellite_to_shell_mapping(constellation_name)
    # establish the correspondence between satellites and orbits
    SATELLITE_TO_ORBIT_MAPPING.satellite_to_orbit_mapping(shells)

    # at this point in execution, the mapping relationship between shell, orbit and satellite has been established in
    # shells, that is, the constellation initialization function has been completed
    constellation = CONSTELLATION.constellation(constellation_name , len(shells) , shells)

    # calculate and save the longitude, latitude and altitude information of different satellites according to shell
    # and timeslot

    # ensure the data/TLE_constellation/ directory exists
    data_directory = "data/TLE_constellation/"
    # This will create the directory if it does not exist
    os.makedirs(data_directory, exist_ok=True)
    # determine whether the .h5 file of the delay and satellite position data of the current constellation exists. If
    # it exists, delete the file and create an empty .h5 file. If it does not exist, directly create an empty .h5 file.
    file_path = "data/TLE_constellation/" + constellation_name + ".h5"
    if os.path.exists(file_path):
        # if the .h5 file exists, delete the file
        os.remove(file_path)
    # create new empty .h5 file
    with h5py.File(file_path, 'w') as file:
        # create position group
        position = file.create_group('position')
        # create multiple shell subgroups within the position group. For example, the shell1 subgroup represents the
        # first layer of shells, the shell2 subgroup represents the second layer of shells, etc.
        for count in range(1, constellation.number_of_shells + 1, 1):
            position.create_group('shell' + str(count))

    for count in range(1, constellation.number_of_shells + 1, 1):
        # taking dT as the time interval, calculate the longitude, latitude and altitude of each satellite
        orbit_period = constellation.shells[count-1].orbit_cycle
        moments = []
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(seconds=orbit_period)
        while start_datetime < end_datetime:
            moments.append((start_datetime.year, start_datetime.month, start_datetime.day,
                            start_datetime.hour, start_datetime.minute, start_datetime.second))
            start_datetime += timedelta(seconds=dT)
        moments.append((end_datetime.year, end_datetime.month, end_datetime.day,
                        end_datetime.hour, end_datetime.minute, end_datetime.second))

        # the id number of satellite
        satellite_id = 1
        for satellite in constellation.shells[count-1].satellites:
            satellite.id = satellite_id
            satellite_id = satellite_id + 1
            TLE_2LE = []
            TLE_2LE.append(satellite.tle_2le[0])
            TLE_2LE.append(satellite.tle_2le[1])
            for moment in moments:
                longitude_latitude_altitude = GET_SATELLITE_POSITION.get_satellite_position(
                    TLE_2LE, moment[0], moment[1], moment[2], moment[3], moment[4], moment[5])
                satellite.longitude.append(longitude_latitude_altitude[0][0])
                satellite.latitude.append(longitude_latitude_altitude[0][1])
                satellite.altitude.append(longitude_latitude_altitude[0][2])

        for tt in range(1, len(moments)+1, 1):
            satellite_position = []
            for sat in constellation.shells[count-1].satellites:
                satellite_position.append(
                    [str(sat.longitude[tt - 1]), str(sat.latitude[tt - 1]), str(sat.altitude[tt - 1])])
            with h5py.File(file_path, 'a') as file:
                # access the existing first-level subgroup position group
                position = file['position']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = position['shell' + str(count)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(tt), data=satellite_position)

    return constellation
