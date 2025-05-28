"""

Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test the implemented indicator bandwidth.
           TThe generated traffic will be under 'data/constellation_test/'

"""


import src.XML_constellation.constellation_entity.user as USER
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_evaluation.exists_ISL.bandwidth as BANDWIDTH
import numpy as np
import os


def bandwidth():
    dT = 1000
    constellation_name = "Starlink"
    London = USER.user(51.5, -0.1, "London")
    Washington = USER.user(38.9, -77.0, "NewYork")
    Istanbul = USER.user(41.0, 28.9, "Istanbul")
    Nairobi = USER.user(-1.3, 36.8, "Nairobi")
    Mumbai = USER.user(19.1, 72.9, "Mumbai")
    Wellington = USER.user(-41.3, 174.8, "Wellington")
#     Singapore = USER.user(1.3, 103.8, "Singapore")
#     LosAngeles = USER.user(34.1, -118.2, "LosAngeles")

    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT=dT,
                                                                            constellation_name=constellation_name)

    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()

    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)

    path = os.path.join("data", "constellation_test", constellation_name)
    os.makedirs(path, exist_ok=True)
    bandwidth = BANDWIDTH.bandwidth(constellation_name, London, Washington, constellation.shells[0], 1.2, 5, dT)
    bandwidth = np.array([bandwidth])
    output_file = os.path.join(path, 'London_Washington_throughput.txt')
    np.savetxt(output_file, bandwidth, fmt='%.3f')
    print("The bandwidth from ", London.user_name, " to ", Washington.user_name, " is ", bandwidth,
          " Mbps")

    bandwidth = BANDWIDTH.bandwidth(constellation_name, Istanbul, Nairobi, constellation.shells[0], 1.2, 5, dT)
    bandwidth = np.array([bandwidth])
    output_file = os.path.join(path, 'Istanbul_Nairobi_throughput.txt')
    np.savetxt(output_file, bandwidth, fmt='%.3f')
    print("The bandwidth from ", Istanbul.user_name, " to ", Nairobi.user_name, " is ", bandwidth,
          " Mbps")

    bandwidth = BANDWIDTH.bandwidth(constellation_name, Mumbai, Wellington, constellation.shells[0], 1.2, 5, dT)
    bandwidth = np.array([bandwidth])
    output_file = os.path.join(path, 'Mumbai_Wellington_throughput.txt')
    np.savetxt(output_file, bandwidth, fmt='%.3f')
    print("The bandwidth from ", Mumbai.user_name, " to ", Wellington.user_name, " is ", bandwidth,
          " Mbps")

    # bandwidth = BANDWIDTH.bandwidth(constellation_name, Singapore, LosAngeles, constellation.shells[0], 1.2, 5, dT)
    # bandwidth = np.array([bandwidth])
    # np.savetxt(path + '/Singapore_LosAngeles_throughput.txt', bandwidth, fmt='%.3f')

    print(f"The bandwidth has been saved in {path}")



if __name__ == '__main__':
    bandwidth()