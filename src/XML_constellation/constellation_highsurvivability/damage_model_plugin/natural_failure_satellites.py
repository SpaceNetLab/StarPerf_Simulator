'''

Author : yunanhou

Date : 2023/11/11

Function : Simulates the natural attenuation and damage of constellation satellites, that is: after a communication
           satellite constellation is launched, the satellites will be naturally damaged and unable to work due to
           various reasons. At this time, without adding new satellites, there will be fewer and fewer satellites in
           the constellation, which will have a certain impact on the service performance of the constellation. This
           script simulates the natural damage of satellites over time by randomly destroying some satellites in the
           constellation (not concentrated destruction), and then observing the performance of the constellation after
           destroying these satellites. For example: at time 1, the third satellite in the 1st orbit is damaged; at
           time 2, the 2nd satellite in the 4th orbit is damaged; at time 3, the 22nd satellite in the 10th orbit is
           damaged, etc. The damage to these satellites is not concentrated. , but the damage time and location are
           random. The function of this script is to simulate the performance of the constellation under the above
           fault model.

'''
import random
import os
import copy
import h5py
import src.XML_constellation.constellation_entity.satellite as SATELLITE
import src.XML_constellation.constellation_entity.orbit as ORBIT
import src.XML_constellation.constellation_entity.shell as SHELL
import src.XML_constellation.constellation_entity.constellation as CONSTELLATION


# Parameters:
# constellation : the constellation that needs to be destroyed by the solar storm and is a constellation class object.
# sh : the shell that needs to be destroyed by the solar storm and is a shell class object
# num_of_damaged_satellites : the number of randomly destroyed satellites. If the value is less than 1, it is the
#                             number of satellites destroyed as a percentage of the total number; if the value is
#                             greater than 1, it is the number of satellites that need to be destroyed.
# dT : how often a timeslot is recorded
# satrt_satellite_id parameter has no effect in this mode
# Return Value : returns the constellation name after num_of_damaged_satellites satellites have been destroyed
def natural_failure_satellites(constellation , sh , num_of_damaged_satellites , dT , satrt_satellite_id):
    # if num_of_damaged_satellites is less than 1, it is the number of satellites destroyed as a percentage of the
    # total number; if num_of_damaged_satellites is greater than 1, it is the number of satellites that need to be
    # destroyed.
    if num_of_damaged_satellites < 1:
        num_of_damaged_satellites = (int)(sh.number_of_satellites * num_of_damaged_satellites)
    # randomly generate num_of_damaged_satellites integers to represent the IDs of satellites that need to be
    # destroyed. The range of these integers is [1,sh.number_of_satellites]
    damaged_satellites = [random.randint(1, sh.number_of_satellites) for _ in range(num_of_damaged_satellites)]

    # deep copy of original constellation
    constellation_copy_name = constellation.constellation_name + "_natural_failure"
    constellation_copy_number_of_shells = constellation.number_of_shells
    constellation_copy_shells = []
    for every_shell_index, every_shell in enumerate(constellation.shells):
        shell_copy_altitude = every_shell.altitude  # height
        shell_copy_number_of_satellites = 0
        shell_copy_number_of_orbits = 0
        shell_copy_inclination = every_shell.inclination  # inclination
        shell_copy_orbit_cycle = every_shell.orbit_cycle  # cycle
        shell_copy_number_of_satellite_per_orbit = None
        shell_copy_phase_shift = every_shell.phase_shift  # phase shift
        shell_copy_orbits = []
        for every_orbit in every_shell.orbits:
            orbit_copy_a = every_orbit.a.value
            orbit_copy_ecc = every_orbit.ecc.value
            orbit_copy_inc = every_orbit.inc.value
            orbit_copy_raan = every_orbit.raan.value
            orbit_copy_argp = every_orbit.argp.value
            orbit_copy_orbit_cycle = every_orbit.orbit_cycle
            orbit_copy_satellite_orbit = every_orbit.satellite_orbit
            orbit_copy_satellites = []
            for every_satellite in every_orbit.satellites:
                if (every_satellite.id in damaged_satellites) and (
                        ("shell" + str(every_shell_index + 1)) == sh.shell_name):
                    continue  # the currently traversed satellite needs to be destroyed, so do nothing.
                else:
                    satellite_copy_longitude = copy.deepcopy(every_satellite.longitude)
                    satellite_copy_latitude = copy.deepcopy(every_satellite.latitude)
                    satellite_copy_altitude = copy.deepcopy(every_satellite.altitude)
                    satellite_copy_ISL = copy.deepcopy(every_satellite.ISL)
                    satellite_copy_nu = every_satellite.nu
                    satellite_copy_id = every_satellite.id
                    satellite_copy_true_satellite = every_satellite.true_satellite
                    satellite_copy = SATELLITE.satellite(nu=satellite_copy_nu, orbit=None,
                                                         true_satellite=satellite_copy_true_satellite)
                    satellite_copy.longitude = satellite_copy_longitude
                    satellite_copy.latitude = satellite_copy_latitude
                    satellite_copy.altitude = satellite_copy_altitude
                    satellite_copy.ISL = satellite_copy_ISL
                    satellite_copy.id = satellite_copy_id
                    orbit_copy_satellites.append(satellite_copy)
            if len(orbit_copy_satellites) == 0:
                continue
            else:
                orbit_copy = ORBIT.orbit(a=orbit_copy_a, ecc=orbit_copy_ecc, inc=orbit_copy_inc, raan=orbit_copy_raan,
                                         argp=orbit_copy_argp)
                orbit_copy.orbit_cycle = orbit_copy_orbit_cycle
                orbit_copy.satellite_orbit = orbit_copy_satellite_orbit
                orbit_copy.satellites = orbit_copy_satellites
                shell_copy_orbits.append(orbit_copy)
                shell_copy_number_of_satellites = shell_copy_number_of_satellites + len(orbit_copy_satellites)
                shell_copy_number_of_orbits = shell_copy_number_of_orbits + 1
        if len(shell_copy_orbits) == 0:
            continue
        else:
            shell_copy = SHELL.shell(altitude=shell_copy_altitude, number_of_satellites=shell_copy_number_of_satellites,
                                     number_of_orbits=shell_copy_number_of_orbits, inclination=shell_copy_inclination,
                                     orbit_cycle=shell_copy_orbit_cycle, number_of_satellite_per_orbit=
                                     shell_copy_number_of_satellite_per_orbit, phase_shift=shell_copy_phase_shift,
                                     shell_name="shell" + str(every_shell_index + 1))
            shell_copy.orbits = shell_copy_orbits
        constellation_copy_shells.append(shell_copy)

    constellation_copy = CONSTELLATION.constellation(constellation_name=constellation_copy_name,
                                                     number_of_shells=constellation_copy_number_of_shells,
                                                     shells=constellation_copy_shells)

    # add ISL connections to the satellites in the constellation_copy constellation. These added ISL connections are
    # the ISLs after deleting the damaged satellites from the original constellation.
    for every_shell in constellation_copy.shells:
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1, every_shell.number_of_orbits + 1, 1):
            for satellite_index in range(1, len(every_shell.orbits[orbit_index - 1].satellites) + 1, 1):
                sat = every_shell.orbits[orbit_index - 1].satellites[satellite_index - 1]
                for isl_index in range(len(sat.ISL) - 1, -1, -1):
                    if (sat.ISL[isl_index].satellite1 in damaged_satellites) or (
                            sat.ISL[isl_index].satellite2 in damaged_satellites):
                        sat.ISL.pop(isl_index)

    # modify the satellite id in the constellation_copy constellation so that it increases continuously starting from 1
    for every_shell in constellation_copy.shells:
        satellite_new_id = 1
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1, every_shell.number_of_orbits + 1, 1):
            for satellite_index in range(1, len(every_shell.orbits[orbit_index - 1].satellites) + 1, 1):
                # satellite original id
                satellite_old_id = every_shell.orbits[orbit_index - 1].satellites[satellite_index - 1].id
                # Satellite new id
                every_shell.orbits[orbit_index - 1].satellites[satellite_index - 1].id = satellite_new_id
                # the satellite ID has been modified, and the ID in ISL also needs to be modified.
                # traverse each orbit layer by layer, orbit_index starts from 1
                for orbit_index_2 in range(1, every_shell.number_of_orbits + 1, 1):
                    for satellite_index_2 in range(1, len(every_shell.orbits[orbit_index_2 - 1].satellites) + 1, 1):
                        sat = every_shell.orbits[orbit_index_2 - 1].satellites[satellite_index_2 - 1]
                        for isl_index in range(len(sat.ISL) - 1, -1, -1):
                            if sat.ISL[isl_index].satellite1 == satellite_old_id:
                                sat.ISL[isl_index].satellite1 = satellite_new_id
                            if sat.ISL[isl_index].satellite2 == satellite_old_id:
                                sat.ISL[isl_index].satellite2 = satellite_new_id
                satellite_new_id = satellite_new_id + 1

    # determine whether the .h5 file of the delay and satellite position data of the current constellation exists.
    # If it exists, delete the file and create an empty .h5 file. If it does not exist, directly create an empty
    # .h5 file.
    copy_file_path = "data/XML_constellation/" + constellation_copy_name + ".h5"
    if os.path.exists(copy_file_path):
        # if the .h5 file exists, delete the file
        os.remove(copy_file_path)
    # create new empty .h5 file
    with h5py.File(copy_file_path, 'w') as file:
        # create position group
        position = file.create_group('position')
        # create multiple shell subgroups within the position group. For example, the shell1 subgroup represents the
        # first layer of shells, the shell2 subgroup represents the second layer of shells, etc.
        for count in range(1, len(constellation.shells) + 1, 1):
            position.create_group('shell' + str(count))
        # create delay group
        delay = file.create_group('delay')
        # create multiple shell subgroups within the delay group. For example, the shell1 subgroup represents the
        # first-level shell, the shell2 subgroup represents the second-level shell, etc.
        for count in range(1, len(constellation.shells) + 1, 1):
            delay.create_group('shell' + str(count))

    for sh2_index, sh2 in enumerate(constellation_copy.shells):
        # the total number of satellites contained in the sh2 layer shell
        number_of_satellites_in_sh2 = sh2.number_of_satellites
        # create the delay matrix of the constellation_copy constellation and write the h5 file
        for t in range(1, (int)(sh2.orbit_cycle / dT) + 2, 1):
            constellation_copy_delay = [[0 for j in range(number_of_satellites_in_sh2 + 1)] for i in
                                        range(number_of_satellites_in_sh2 + 1)]
            # traverse each orbit layer by layer, orbit_index starts from 1
            for orbit_index2 in range(1, sh2.number_of_orbits + 1, 1):
                for satellite_index2 in range(1, len(sh2.orbits[orbit_index2 - 1].satellites) + 1, 1):
                    # get the current satellite object
                    cur_satellite = sh2.orbits[orbit_index2 - 1].satellites[satellite_index2 - 1]
                    for isls in cur_satellite.ISL:
                        sat1 = isls.satellite1
                        sat2 = isls.satellite2
                        if sat1 == cur_satellite.id:
                            other_satellite = sat2
                        else:
                            other_satellite = sat1
                        constellation_copy_delay[cur_satellite.id][other_satellite] = isls.delay[t - 1]

            with h5py.File(copy_file_path, 'a') as file:
                # access the existing first-level subgroup delay group
                delay_group = file['delay']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = delay_group['shell' + str(sh2_index + 1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=constellation_copy_delay)

        # create the satellite position matrix of the constellation_copy constellation and write the h5 file
        for t in range(1, (int)(sh2.orbit_cycle / dT) + 2, 1):

            # this list is used to store the position information of all satellites in the current shell.
            # It is a two-dimensional list. Each element is a one-dimensional list. Each one-dimensional list
            # contains three elements, which respectively represent the longitude, latitude and altitude of a satellite.
            satellite_position = []
            for orbit in sh2.orbits:
                for sat in orbit.satellites:
                    satellite_position.append(
                        [str(sat.longitude[t - 1]), str(sat.latitude[t - 1]), str(sat.altitude[t - 1])])

            with h5py.File(copy_file_path, 'a') as file:
                # access the existing first-level subgroup position group
                position_group = file['position']
                # access the existing secondary subgroup 'shell'+str(count) subgroup
                current_shell_group = position_group['shell' + str(sh2_index + 1)]
                # create a new dataset in the current_shell_group subgroup
                current_shell_group.create_dataset('timeslot' + str(t), data=satellite_position)

    # returns the damaged constellation after generation
    return constellation_copy

