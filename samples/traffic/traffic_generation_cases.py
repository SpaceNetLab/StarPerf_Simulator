"""

Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test the functionality of the traffic generation plugin.
           The generated traffic will be under 'data/'

"""

import src.XML_constellation.constellation_traffic.traffic_plugin_manager as traffic_plugin_manager
from src.constellation_generation.by_duration.constellation_configuration import constellation_configuration

def traffic_generation():
    duration = 10
    dT = 1
    cons_name = 'Starlink'
    constellation = constellation_configuration(duration, dT, cons_name, shell_index=1)

    Traffic = traffic_plugin_manager.traffic_plugin_manager()
    for t in range(1, duration + 1):
        Traffic.execute_traffic_policy(constellation, t)

    print("Traffic generation is completed for " + str(duration) + " s.")
    print()


if __name__ == '__main__':
    traffic_generation()
