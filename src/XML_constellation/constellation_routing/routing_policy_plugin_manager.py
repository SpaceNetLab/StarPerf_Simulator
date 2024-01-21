'''

Author : yunanhou

Date : 2023/11/15

Function : Constellation routing policy plug-in manager is used to manage all constellation routing policy models.
           Write a constellation routing policy plug-in manager to store all routing strategies as plug-ins, such as
           shortest path routing, least hop routing and other models. If users want to implement their own routing
           model, they only need to write the script themselves and put it in the specified location. In this way,
           a unified interface is formed to manage all routing policy models, and this interface is the management of
           the constellation routing model plug-in. The router treats each routing model as a plug-in, which users can
           implement and use as needed. Each routing strategy is plug-in-based, defining a unified interface for
           routing strategies and implementing three methods: shortest path routing, second-shortest path routing and
           least hop routing. If you want to simulate other routing strategies in the future, you only need to write
           your own script according to the interface specifications. All constellation routing policy model plug-ins
           are located in the src/constellation_routing/routing_policy_plugin directory. To implement a new
           constellation routing policy model, users only need to write their own kits according to the agreed
           interface specifications and put them in this path.

'''
import os
import importlib


class routing_policy_plugin_manager:
    def __init__(self):
        # constellation routing policy model plug-in dictionary stores all constellation routing model plug-ins in this
        # project. The key of the dictionary is the function name of the routing model, and the value is the function
        # corresponding to the routing model.
        self.plugins = {}
        # the following code block is used to traverse the src/constellation_routing/routing_policy_plugin folder, which
        # stores the py files of all routing models.


        # traverse this folder to obtain the names of all routing model plug-ins and store them in the self.plugins
        # collection.
        package_name = "src.XML_constellation.constellation_routing.routing_policy_plugin"
        plugins_path = package_name.replace(".", os.path.sep) # the path where the plug-in is stored
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        # set the routing mode used by the current routing policy model plug-in manager. The shortest path routing model
        # is used by default.
        self.current_routing_policy = "shortest_path"

    # switch routing policy
    # Parameters:
    # plugin_name : the name of the new routing policy
    def set_routing_policy(self, plugin_name):
        self.current_routing_policy = plugin_name  # set the current routing policy to the specified model
        #print("\t\t\tThe current constellation routing policy has been switched to " + plugin_name)


    # Function : implement corresponding routing policies
    # Parameters:
    # constellation_name : the name of the constellation, and the parameter type is a string, such as "Starlink"
    # source : the source ground station
    # target : the target ground station
    # t : a certain time slot (timeslot)
    # sh : a shell class object, representing a shell in the constellation
    def execute_routing_policy(self , constellation_name , source , target , sh , t=1):
        function = self.plugins[self.current_routing_policy]
        target_routing_path = function(constellation_name , source , target , sh , t)
        return target_routing_path