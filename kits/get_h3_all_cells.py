'''

Author : yunanhou

Date : 2023/11/12

Function : This script is used to obtain the cells at resolution 0-4 of the python h3 library, and save the
           h3ids of cells with different resolutions into the same .h5 file. The path of the file is:
           data/h3_cells_id_res0-4.h5

'''
import h3
import h5py


def get_h3_all_cells():
    # create an hdf5 file (if the file does not exist, it will be created; if it exists, it will be overwritten)
    with h5py.File('data/h3_cells_id_res0-4.h5', 'w') as file:
        # a list collection composed of h3ids of all cells with resolution 0
        res0_cells = list(h3.get_res0_cells())
        # write res0_cells to file
        file.create_dataset('res0_cells', data=res0_cells)
        # a list collection composed of h3ids of all cells with resolution 1
        res1_cells = []
        for res0_cell in res0_cells:
            res1_cells = res1_cells + list(h3.cell_to_children(res0_cell))
        # write res1_cells to file
        file.create_dataset('res1_cells', data=res1_cells)
        # a list collection composed of h3ids of all cells with resolution 2
        res2_cells = []
        for res1_cell in res1_cells:
            res2_cells = res2_cells + list(h3.cell_to_children(res1_cell))
        # write res2_cells to file
        file.create_dataset('res2_cells', data=res2_cells)
        # a list collection composed of h3ids of all cells with resolution 3
        res3_cells = []
        for res2_cell in res2_cells:
            res3_cells = res3_cells + list(h3.cell_to_children(res2_cell))
        # write res3_cells to file
        file.create_dataset('res3_cells', data=res3_cells)
        # a list collection composed of h3ids of all cells with resolution 4
        res4_cells = []
        for res3_cell in res3_cells:
            res4_cells = res4_cells + list(h3.cell_to_children(res3_cell))
        # write res4_cells to file
        file.create_dataset('res4_cells', data=res4_cells)