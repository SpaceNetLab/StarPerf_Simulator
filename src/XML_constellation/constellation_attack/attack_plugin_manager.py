"""

Author : zhifenghan

Date : 2025/05/09

Function : This class manages attack plugins for constellation simulations. It dynamically loads
           attack modules/plugins from the specified directory, registers them, and provides methods
           to execute different types of attacks on constellation networks including Icarus attacks,
           single link attacks, and energy drain attacks.

"""

import os
import importlib

class attack_plugin_manager:
    def __init__(self):
        # Store all attack plugins in this dictionary
        self.plugins = {}
        # Traverse this folder to obtain all traffic model plugins
        package_name = "src.XML_constellation.constellation_attack.attack_plugin"
        plugins_path = package_name.replace(".", os.path.sep)
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        
        # Defualt to the positive_grid_icarus model
        self.current_attack_model = "positive_grid_icarus"

    # Switcch the traffic generation model
    def set_attack_model(self, plugin_name):
        if plugin_name in self.plugins:
            self.current_attack_model = plugin_name
        else:
            raise ValueError(f"Plugin {plugin_name} not found!")
        # print("The current constellation traffic model has been switched to " + plugin_name)
    
    # Execute the corresponding traffic generation policy
    def execute_icarus_attack(self, constellation, time_slot, 
                               link_utilization_ratio=0.9, 
                               target_affected_traffic=300000, traffic_thre=20,
                               GSL_capacity=4096, unit_traffic=20,
                               given_bot_number=3000):
        
        function = self.plugins[self.current_attack_model]

        return function(constellation, time_slot,
                        link_utilization_ratio, target_affected_traffic, 
                        traffic_thre, GSL_capacity, 
                        unit_traffic, given_bot_number)
    
    def execute_single_link_attack(self, constellation, time_slot, src_lat=48.8667, 
                                   src_lon=2.4167, dst_lat=40.4168, dst_lon=-3.7038,
                                   link_num=500, rate=40):
        function = self.plugins[self.current_attack_model]

        return function(constellation, time_slot, src_lat, src_lon,
                         dst_lat, dst_lon, link_num, rate)
    
    def execute_energy_drain_attack(self, constellation, time_slot, dT=30, bot_num=500, unit_traffic=20, base_power=1000):
        function = self.plugins[self.current_attack_model]

        return function(constellation, time_slot, dT, bot_num, unit_traffic, base_power)
