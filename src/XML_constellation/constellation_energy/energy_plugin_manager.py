"""
Author : zhifenghan

Date : 2025/05/09

Function : This class manages energy consumption modeling plugins for satellite constellation simulations.
           It dynamically loads different energy consumption models, provides an interface to switch between
           them, and executes the selected energy calculation policy with configurable communication
           parameters to accurately model satellite power consumption.

"""

import os
import importlib

class energy_plugin_manager:
    def __init__(self):
        self.plugins = {}
        package_name = "src.XML_constellation.constellation_energy.energy_plugin"
        plugins_path = package_name.replace(".", os.path.sep)
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # remove the file extension ".py"
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function

        self.current_energy_model = "communication_link"


    def set_energy_model(self, plugin_name):
        if plugin_name in self.plugins:
            self.current_energy_model = plugin_name
        else:
            raise ValueError(f"Plugin {plugin_name} not found!")
    
    
    def execute_energy_policy(self, constellation, time_slot, gsl_transmitter_idle=40, isl_transmitter_idle=10,
                        gsl_transmitter_active=200, isl_transmitter_active=50, gsl_transmitter_w=0.01,
                        isl_transmitter_w=0.0025, gsl_receiver_idle=40, isl_receiver_idle=10,
                        gsl_receiver_active=100, isl_receiver_active=25, gsl_receiver_w=0.008,
                        isl_receiver_w=0.002, tail_energy_time=2):
        
        function = self.plugins[self.current_energy_model]

        return function(constellation, time_slot, gsl_transmitter_idle, isl_transmitter_idle,
                        gsl_transmitter_active, isl_transmitter_active, gsl_transmitter_w,
                        isl_transmitter_w, gsl_receiver_idle, isl_receiver_idle,
                        gsl_receiver_active, isl_receiver_active, gsl_receiver_w,
                        isl_receiver_w, tail_energy_time)