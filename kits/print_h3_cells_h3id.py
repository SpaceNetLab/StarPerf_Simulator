'''

Author : yunanhou

Date : 2023/11/21

Function : This script is used to view the h3id of all cells with the specified resolution in
           "data/h3_cells_id_res0-4.h5"

'''
import h5py
import numpy as np

# Parameter :
# resolution : the resolution of cells is an integer. Currently, the supported value range is 0/1/2/3/4
def print_h3_cells_h3id(resolution):
    with h5py.File('data/h3_cells_id_res0-4.h5', 'r') as file:
        cells = np.array(file['res' + str(resolution) + '_cells']).tolist()
    for item in cells:
        print("\t\t\t" , item)