'''

Author: yunanhou

Date : 2023/12/16

Function : Constellation damage model plug-in manager, used to manage all constellation damage models. Write a
           constellation damage model plug-in manager to store all damage models as plug-ins, such as satellite
           natural aging damage, solar storm concentrated damage and other models. If users want to implement
           their own damage models, they only need to write the script themselves and put it in the specified
           location. In this way, a unified interface is formed to manage all damage models, and this interface
           is the Constellation Damage Model Plug-in Manager , it treats each damage model as a plug-in, which
           users can implement and use as needed.

'''
import os
import importlib

class damage_model_plugin_manager:
    def __init__(self):
        # constellation damage model plug-in dictionary stores all constellation damage model plug-ins in this project.
        # The key of the dictionary is the function name of the damaged model, and the value is the function
        # corresponding to the damaged model.
        self.plugins = {}

        # traverse this folder to obtain the names of all damaged model plug-ins and store them in the
        # self.plugins dictionary.
        package_name = "src.TLE_constellation.constellation_highsurvivability.damage_model_plugin"
        plugins_path = package_name.replace(".", os.path.sep)  # the path where the plug-in is stored
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        # set the damage mode used by the current damage model plug-in manager. The default is the solar storm
        # concentrated damage model.
        self.current_damage_model = "sunstorm_damaged_satellites"

    # switch the damaged model
    # Parameter meaning: plugin_name is the name of the new damaged model
    def set_damage_model(self, plugin_name):
        self.current_damage_model = plugin_name  # sets the current damage model to the specified model
        print("The current constellation damage model has been switched to " + plugin_name)



    # Function : execute the constellation damage model and start destroying the constellation
    #            according to the specified pattern
    # Parameters:
    # constellation : the constellation that needs to be destroyed and is a constellation class object.
    # sh : the shell that needs to be destroyed by the solar storm and is a shell class object
    # num_of_damaged_satellites : the number of randomly destroyed satellites. If the value is less than 1, it is the
    #                             number of satellites destroyed as a percentage of the total number; if the value is
    #                             greater than 1, it is the number of satellites that need to be destroyed.
    # dT : how often a timeslot is recorded
    # satrt_satellite_id : the id of the most central satellite in a group of satellites to be destroyed. If
    #                      satrt_satellite_id is -1, it means that the id of the center satellite of the destroyed group is
    #                      not specified, but a randomly generated one.
    # Return Value : returns the constellation name after num_of_damaged_satellites satellites have been destroyed
    def execute_damage_model(self , constellation , sh , num_of_damaged_satellites , dT , satrt_satellite_id = -1):
        function = self.plugins[self.current_damage_model]
        constellation_copy = function(constellation , sh , num_of_damaged_satellites , dT , satrt_satellite_id)
        return constellation_copy