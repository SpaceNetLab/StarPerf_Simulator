import sp_cal_bandwidth
import sp_cal_betweenness
import sp_cal_coverage
import sp_cal_dij_delay


def get_parameters(path):
    f = open(path, "r")
    line = f.readline()
    line = line.strip('\n')
    values = line.split(',')
    parameter = [[0 for i in range(len(values))] for i in range(6)]
    row = 0
    while line:
        line = line.strip('\n')
        values = line.split(',')
        for i in range(len(values)):
            if row != 0:
                parameter[row][i] = (float)(values[i])
            else:
                parameter[row][i] = values[i]
        row += 1
        line = f.readline()
    f.close()
    return parameter

def perform_benchmark():
    path = 'parameter.txt'
    constellation_parameter = get_parameters(path)
    sp_cal_dij_delay.dij_delay(constellation_parameter, error_rate=0, dT=1)
    sp_cal_bandwidth.bandwidth(constellation_parameter,dT=60)
    sp_cal_coverage.coverage(constellation_parameter)
    sp_cal_betweenness.betweenness(constellation_parameter)

if __name__ == '__main__':
    perform_benchmark()
