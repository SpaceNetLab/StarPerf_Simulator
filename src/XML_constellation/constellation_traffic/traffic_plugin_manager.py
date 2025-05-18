"""
Author : zhifenghan

Date : 2025/05/09

Function : This class manages traffic generation plugins for satellite constellation simulations.
           It dynamically loads traffic model plugins, provides an interface to switch between
           different traffic models, and executes the selected traffic generation policy on
           the constellation network.
"""

import os
import importlib

class traffic_plugin_manager:
    def __init__(self):
        # Store all traffic generation plugins in this dictionary
        self.plugins = {}
        # Traverse this folder to obtain all traffic model plugins
        package_name = "src.XML_constellation.constellation_traffic.traffic_plugin"
        plugins_path = package_name.replace(".", os.path.sep)
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        
        # Defualt to the positive_grid_traffic model
        self.current_traffic_model = "positive_grid_traffic"

    # Switcch the traffic generation model
    def set_traffic_model(self, plugin_name):
        if plugin_name in self.plugins:
            self.current_traffic_model = plugin_name
        else:
            raise ValueError(f"Plugin {plugin_name} not found!")
        # print("The current constellation traffic model has been switched to " + plugin_name)
    
    # Execute the corresponding traffic generation policy
    def execute_traffic_policy(self, constellation, time_slot, 
                               minimum_elevation=25, isl_capacity=20480,
                               uplink_capacity=4096, downlink_capacity=4096,
                               link_utilization_ratio=0.9, flow_size=0.5):
        
        function = self.plugins[self.current_traffic_model]
        
        return function(constellation, time_slot,  
                        minimum_elevation, isl_capacity,
                        uplink_capacity, downlink_capacity,
                        link_utilization_ratio, flow_size)
