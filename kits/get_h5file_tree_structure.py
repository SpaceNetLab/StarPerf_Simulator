'''

Author : yunanhou

Date : 2023/11/12

Function : recursively read all groups and datasets in the .h5 file to obtain its tree directory structure

'''
import h5py


def print_hdf5_structure(group, indent=0):
    for key in group.keys():
        item = group[key]
        if isinstance(item, h5py.Group):
            print("\t\t\t" , "  " * indent + f"Group: {key}")
            print_hdf5_structure(item, indent + 1)
        elif isinstance(item, h5py.Dataset):
            print("\t\t\t" , "  " * indent + f"Dataset: {key}")



if __name__ == '__main__':
    with h5py.File('../data/XML_constellation/Kuiper.h5', 'r') as file:
        print_hdf5_structure(file)