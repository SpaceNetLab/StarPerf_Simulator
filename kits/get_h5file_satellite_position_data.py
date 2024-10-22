'''

Author : yunanhou

Date : 2023/11/13

Function : read the position matrix data in the h5 file

'''
import h5py
import numpy as np

def get_h5file_satellite_position_data(h5_file_name):
    # read the position matrix data in the h5 file
    with h5py.File(h5_file_name, 'r') as file:
        # access the existing first-level subgroup position group
        position = file['position']
        # access the existing secondary subgroup 'shell'+str(count) subgroup
        current_shell_group = position['shell1']
        # read dataset
        data = np.array(current_shell_group['timeslot1']).tolist()
        data = [element.decode('utf-8') for row in data for element in row]
        data = [data[i:i + 3] for i in range(0, len(data), 3)]
        data = [[float(element) for element in row] for row in data]

    for ele in data:
        print("\t\t\t" , ele)


if __name__ == '__main__':
    get_h5file_satellite_position_data('../../StarAlliance/GRASP_PR_new/ID_1/Boeing.h5')