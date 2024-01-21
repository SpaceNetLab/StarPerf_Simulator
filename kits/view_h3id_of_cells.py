'''

Author : yunanhou

Date : 2023/11/25

Function : View the h3id of h3 cells


'''
import h5py
import numpy as np


def view_h3id_of_cells():
    # read the delay matrix data in the h5 file
    with h5py.File('data/h3_cells_id_res0-4.h5', 'r') as file:
        # read dataset
        res0_cells = np.array(file['res0_cells']).tolist()
        print('\t\t\tresolution = 0 cells : ')
        print("\t\t\t" , res0_cells)

        print('\t\t\tresolution = 1 cells : ')
        res1_cells = np.array(file['res1_cells']).tolist()
        print("\t\t\t" , res1_cells)

        print('\t\t\tresolution = 2 cells : ')
        res2_cells = np.array(file['res2_cells']).tolist()
        print("\t\t\t" , res2_cells)

        print('\t\t\tresolution = 3 cells : ')
        res3_cells = np.array(file['res3_cells']).tolist()
        print("\t\t\t" , res3_cells)

        print('\t\t\tresolution = 4 cells : ')
        res4_cells = np.array(file['res4_cells']).tolist()
        print("\t\t\t" , res4_cells)
