'''

Author : yunanhou

Date : 2023/11/13

Function : read the delay matrix data in the h5 file

'''
import h5py
import numpy as np


def get_h5file_satellite_delay_data():
    # read the delay matrix data in the h5 file
    with h5py.File('data/XML_constellation/Starlink.h5', 'r') as file:
        # access the existing first-level subgroup delay group
        delay = file['delay']
        # access the existing secondary subgroup 'shell'+str(count) subgroup
        current_shell_group = delay['shell1']
        # read dataset
        delay_matrix = np.array(current_shell_group['timeslot1']).tolist()

    print(delay_matrix)


if __name__ == '__main__':
    get_h5file_satellite_delay_data()