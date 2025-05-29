"""

Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test the implemented indicator delay.
           TThe generated traffic will be under 'data/constellation_test/'

"""

import src.XML_constellation.constellation_entity.user as USER
import src.constellation_generation.by_XML.constellation_configuration as constellation_configuration
import src.XML_constellation.constellation_connectivity.connectivity_mode_plugin_manager as connectivity_mode_plugin_manager
import src.XML_constellation.constellation_evaluation.exists_ISL.delay as DELAY
import numpy as np
import os


def delay():
    dT = 1000
    constellation_name = "Starlink"
    London = USER.user(51.5, -0.1, "London")
    Washington = USER.user(38.9, -77.0, "NewYork")
    Istanbul = USER.user(41.0, 28.9, "Istanbul")
    Nairobi = USER.user(-1.3, 36.8, "Nairobi")
    Mumbai = USER.user(19.1, 72.9, "Mumbai")
    Wellington = USER.user(-41.3, 174.8, "Wellington")
    Singapore = USER.user(1.3, 103.8, "Singapore")
    LosAngeles = USER.user(34.1, -118.2, "LosAngeles")

    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT=dT,
                                                                            constellation_name=constellation_name)

    # initialize the connectivity mode plugin manager
    connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()

    # execute the connectivity mode and build ISLs between satellites
    connectionModePluginManager.execute_connection_policy(constellation=constellation, dT=dT)

    path = os.path.join("data", "constellation_test", constellation_name)
    os.makedirs(path, exist_ok=True)
    delay = DELAY.delay(constellation.constellation_name, London, Washington, dT, constellation.shells[0])
    delay = np.array(delay)
    output_file = os.path.join(path, 'London_Washington.txt')
    np.savetxt(output_file, delay, fmt='%.3f')
    print("The average delay time from ", London.user_name, " to ", Washington.user_name, " is ", np.mean(delay),
          " s")

    delay = DELAY.delay(constellation.constellation_name, Istanbul, Nairobi, dT, constellation.shells[0])
    delay = np.array(delay)
    output_file = os.path.join(path, 'Istanbul_Nairobi.txt')
    np.savetxt(output_file, delay, fmt='%.3f')
    print("The average delay time from ", Istanbul.user_name, " to ", Nairobi.user_name, " is ", np.mean(delay),
          " s")

    delay = DELAY.delay(constellation.constellation_name, Mumbai, Wellington, dT, constellation.shells[0])
    delay = np.array(delay)
    output_file = os.path.join(path, 'Mumbai_Wellington.txt')
    np.savetxt(output_file, delay, fmt='%.3f')
    print("The average delay time from ", Mumbai.user_name, " to ", Wellington.user_name, " is ", np.mean(delay),
          " s")

    # delay = DELAY.delay(constellation.constellation_name, Singapore, LosAngeles, dT, constellation.shells[0])
    # delay = np.array(delay)
    # np.savetxt(path + '/Singapore_LosAngeles.txt', delay, fmt='%.3f')

    print(f"The delay has been saved in {path}")


if __name__ == '__main__':
    delay()

