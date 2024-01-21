'''

Author : yunanhou

Date : 2023/12/03

Function : This script is used to simulate the constellation working in +Grid mode

In +grid mode, one satellite will establish 4 ISLs, which is equivalent to n=4 in the "n-nearest" connection mode.
Therefore, +Gird can be regarded as an "n-nearest" connection with n=4.

'''
import src.TLE_constellation.constellation_connectivity.connectivity_plugin.n_nearest as N_NEAREST


# Parameters:
# constellation : the constellation to establish +Grid connection
# dT : the time interval
# n : each satellite can establish up to n ISLs
def positive_Grid(constellation , dT , n=4):
    N_NEAREST.n_nearest(constellation , dT , n)
