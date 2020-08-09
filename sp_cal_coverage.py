import math
import matplotlib.pyplot as plt
import numpy
import scipy.io as scio
import xlrd


def coverage(parameter):
    constellation_num = len(parameter[0])
    constellation_name = parameter[0]
    satellite_num = [int(x) for x in parameter[1]]
    cycle = [int(x) for x in parameter[2]]
    depression = parameter[3]
    elevation = parameter[4]
    central_angle = [0 for i in range(constellation_num)]
    for i in range(constellation_num):
        # central_angle[i] = 180 - 90 - elevation[i]
        central_angle[i] = 180 - 2 * (depression[i] + elevation[i])
    satellite_in_latitude = [[0 for i in range(18)] for i in range(constellation_num)]
    satellite_in_longitude = [[0 for i in range(36)] for i in range(constellation_num)]
    for constellation_index in range(constellation_num):
        path = constellation_name[constellation_index] + '\\position.mat'
        data = scio.loadmat(path)
        position = data['position']
        for satellite_no in range(satellite_num[constellation_index]):
            for time in range(cycle[constellation_index]):
                latitude = position[satellite_no][0][0][time]
                longitude = position[satellite_no][0][1][time]
                latitude_lower_boundary = int(math.floor((latitude - central_angle[constellation_index] / 2) / 10))
                latitude_upper_boundary = int(math.floor((latitude + central_angle[constellation_index] / 2) / 10))
                if latitude_lower_boundary < -9:
                    latitude_lower_boundary = -9
                if latitude_upper_boundary > 8:
                    latitude_upper_boundary = 8
                for k in range(latitude_lower_boundary, latitude_upper_boundary + 1):
                    satellite_in_latitude[constellation_index][k + 9] += 1
                longitude_lower_boundary = int(math.floor((longitude - central_angle[constellation_index] / 2) / 10))
                longitude_upper_boundary = int(math.floor((longitude + central_angle[constellation_index] / 2) / 10))
                if longitude_lower_boundary < -18:
                    longitude_lower_boundary = int(
                        math.floor((180 - (-180 - longitude + central_angle[constellation_index] / 2)) / 10))
                if longitude_upper_boundary > 17:
                    longitude_upper_boundary = int(
                        math.floor((-180 + longitude + central_angle[constellation_index] / 2 - 180) / 10))
                if longitude_lower_boundary > 0 and longitude_upper_boundary < 0:
                    for k in range(longitude_lower_boundary, 18):
                        satellite_in_longitude[constellation_index][k + 18] += 1
                    for k in range(-18, longitude_upper_boundary + 1):
                        satellite_in_longitude[constellation_index][k + 18] += 1
                else:
                    for k in range(longitude_lower_boundary, longitude_upper_boundary + 1):
                        satellite_in_longitude[constellation_index][k + 18] += 1
    print(satellite_in_latitude)
    print(satellite_in_longitude)
    
    for constellation_index in range(constellation_num):
        satellite_in_latitude[constellation_index] = [x / float(cycle[constellation_index]) for x in
                                                      satellite_in_latitude[constellation_index]]
        satellite_in_longitude[constellation_index] = [x / float(cycle[constellation_index]) for x in
                                                       satellite_in_longitude[constellation_index]]

    numpy.savetxt('lat.csv', satellite_in_latitude, fmt='%f')
    numpy.savetxt('long.csv', satellite_in_longitude, fmt='%f')

    data = xlrd.open_workbook('global_population.xlsx')
    table = data.sheets()[0]
    latitude = table.col_values(0)[1::]
    population = table.col_values(1)[1::]
    population_in_latitude_zone = [0 for i in range(18)]
    for i in range(len(latitude)):
        population_in_latitude_zone[int(math.floor(latitude[i] / 10)) + 9] += population[i]
    satellite_for_person = [[0 for i in range(18)] for i in range(constellation_num)]

    for constellation_index in range(constellation_num):
        for i in range(18):
            if population_in_latitude_zone[i] != 0:
                satellite_for_person[constellation_index][i] = satellite_in_latitude[constellation_index][i] / \
                                                               population_in_latitude_zone[i]
    numpy.savetxt('sat_per_million_lat.csv', satellite_for_person, fmt='%f')

    table = data.sheets()[1]
    longitude = table.col_values(0)[1::]
    population = table.col_values(1)[1::]
    population_in_longitude_zone = [0 for i in range(36)]
    for i in range(len(longitude)):
        population_in_longitude_zone[int(math.floor(longitude[i] / 10)) + 18] += population[i]
    satellite_for_person = [[0 for i in range(36)] for i in range(constellation_num)]

    for constellation_index in range(constellation_num):
        for i in range(36):
            if population_in_longitude_zone[i] != 0:
                satellite_for_person[constellation_index][i] = satellite_in_longitude[constellation_index][i] / \
                                                               population_in_longitude_zone[i]
    numpy.savetxt('sat_per_million_long.csv', satellite_for_person, fmt='%f')
