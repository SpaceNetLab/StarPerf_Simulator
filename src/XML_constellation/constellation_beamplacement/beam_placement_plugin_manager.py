'''

Author : yunanhou

Date : 2023/11/15

Function : Constellation beam placement plug-in manager, used to manage all constellation beam placement strategy models

           Write a constellation beam placement plug-in manager and store all beam placement strategies as plug-ins.
           If users want to implement their own beam placement algorithms, they only need to write the script themselves
           and put it in the specified location. This will form a unified An interface is used to manage all beam
           placement strategies, and this interface is the constellation beam placement plug-in manager. It treats each
           beam placement strategy as a plug-in, which can be implemented and used by users as needed.


           Each beam placement strategy is plug-in and a unified interface for beam placement strategies is defined.
           If you want to simulate other beam placement strategies later, you only need to write your own script
           according to the interface specifications.


           To implement a new constellation beam
           placement model, users only need to write their own script according to the agreed interface specifications
           and put it in this path.


           The so-called interface specification refers to: All beam placement plug-ins use the h3 library to divide the
           earth's surface into several cells according to a certain resolution, and then for the constellation
           satellites in the sky, each satellite is equipped with several antennas, and then the satellites are equipped
           with several antennas according to what This scheduling algorithm is used to allocate beams to the ground.
           This scheduling algorithm is the so-called "plug-in". At the same time, since satellites are constantly
           moving, the above scheduling algorithm should be rescheduled every once in a while (for example, Starlink is
           scheduled every 15 seconds).

'''
import os
import importlib


class beam_placement_plugin_manager:
    def __init__(self):
        # constellation beam placement model plug-in dictionary stores all constellation beam placement model plug-ins
        # in this project. The key of the dictionary is the function name of the beam placement model, and the value is
        # the function corresponding to the beam placement model.
        self.plugins = {}

        # traverse this folder to obtain the names of all beam placement model plug-ins and store them in the
        # self.plugins dictionary.
        package_name = "src.XML_constellation.constellation_beamplacement.beam_placement_plugin"
        plugins_path = package_name.replace(".", os.path.sep) # the path where the plug-in is stored
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        # set the beam placement mode used by the current beam placement model plug-in manager.
        # The default is a random placement model.
        self.current_beamplacement_policy = "random_placement"

    # switch the beam placement strategy, parameter meaning: plugin_name is the name of the new beam placement strategy
    def set_beamplacement_policy(self, plugin_name):
        # set the current routing policy to the specified model
        self.current_beamplacement_policy = plugin_name
        print("The current constellation beam placement strategy has been switched to : " + plugin_name)



    # Function: execute the corresponding beam allocation strategy
    # Parameters:
    # sh : sh is a shell class object, representing a layer of shell in the constellation
    # h3_resolution : the resolution of cells divided by h3 library. The currently supported resolutions are: 0/1/2/3/4
    # antenna_count_per_satellite : the number of antennas each satellite is equipped with. This parameter determines how
    #                               many spot beams a satellite can emit.
    # dT : the beam scheduling time interval. For example, dT=15s means that the beam is scheduled every 15s.
    # minimum_elevation : the minimum elevation angle at which a satellite can be seen from a point on the ground
    # There are two return values :
    # Return value 1: The set of all cells that can be covered by the beam in each timeslot. This is a two-dimensional
    #                 list. Each element in it is a one-dimensional list, representing the set of all covered cells in
    #                 a certain timeslot.
    # Return value 2: Cells, a collection of all cells
    def execute_beamplacement_policy(self, sh , h3_resolution , antenna_count_per_satellite , dT , minimum_elevation):
        function = self.plugins[self.current_beamplacement_policy]
        covered_cells_per_timeslot , Cells = function(sh , h3_resolution , antenna_count_per_satellite , dT , minimum_elevation)
        return covered_cells_per_timeslot , Cells

