'''

Author : yunanhou

Date : 2023/12/03

Function : This script defines a manager class for the connection methods between satellites in the constellation.
           This is an open interface that can easily access any connection method, such as motif, +Grid, etc. If you
           want to add a new connection mode in the future, you only need to write functions according to the interface
           specification document.

Requirements : All connection modes of this project are stored in the connection_plugin folder. Each py file contains a
               function. A function is the definition of a connection mode. The function name is the same as the file
               name.

'''
import importlib
import os


class connectivity_mode_plugin_manager:
    def __init__(self):
        # the connection mode plug-in dictionary stores all the connection mode plug-ins in this project. The key of
        # the dictionary is the function name of the connection mode, and the value is the function corresponding to
        # the connection mode.
        self.plugins = {}

        # the following code block is used to traverse the
        # src/TLE_constellation/constellation_connectivity/connectivity_plugin folder,
        # which stores the py files of all connection modes.

        # traverse this folder to obtain the names of all connection mode plug-ins and store them in the self.plugins
        # collection.

        package_name = "src.TLE_constellation.constellation_connectivity.connectivity_plugin"
        plugins_path = package_name.replace(".", os.path.sep)  # the path where the plug-in is stored
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        # set the connection mode used by the current connection mode plug-in manager. The default connection mode is
        # "n_nearest"
        self.current_connection_mode = "n_nearest"



    # the function of this function is to clear all ISLs in the incoming satellite constellation.
    def clear_ISL(self, constellation):
        for shell in constellation.shells:
            for orbit in shell.orbits:
                for satellite in orbit.satellites:
                    satellite.ISL.clear()  # clear satellite ISL



    # Function : switch the connection mode
    # Parameters :
    # plugin_name : the name of the new connection mode
    def set_connection_mode(self, plugin_name):
        self.current_connection_mode = plugin_name  # set the current connection mode to the specified mode
        #print("The current constellation connection mode has been switched to " + plugin_name)



    # Function : execute constellation connection mode
    # Parameters:
    # constellation : the constellation to establish connection
    # dT : the time interval
    # n : each satellite can establish up to n ISLs
    def execute_connection_policy(self , constellation , dT , n = 4):
        self.clear_ISL(constellation)  # clear all existing ISLs
        function = self.plugins[self.current_connection_mode]
        function(constellation, dT , n)  # go to execute the corresponding connection mode function
