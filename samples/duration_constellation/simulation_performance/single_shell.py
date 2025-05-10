"""

Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test the time required for a single-layer satellite under multiple simulation durations.
           The generated results will be located under "data/constellation_test/".

"""

from src.constellation_generation.by_duration.constellation_configuration import constellation_configuration
import time
import numpy as np
import os

def single_shell_performance():
    # starlink : 5731、5755、5743、5718
    # kuiper : 5830、5805、5780
    # telesat : 6557、6298
    # OneWeb : 6556
    # simulation test time range : 100~5000, sampling interval=350, 15 time slots

    duration = list(range(100, 5001, 350))
    dT = 5
    starlink_times = []
    kuiper_times = []
    telesat_times = []
    oneweb_times = []
    for single_dur in duration:
        start_time = time.time()
        starlink_cons = constellation_configuration(single_dur, dT, "Starlink")
        end_time = time.time()
        starlink_times.append(end_time - start_time)
        print(end_time - start_time)

        start_time = time.time()
        kuiper_cons = constellation_configuration(single_dur, dT, "Kuiper")
        end_time = time.time()
        kuiper_times.append(end_time - start_time)
        print(end_time - start_time)

        start_time = time.time()
        telesat_cons = constellation_configuration(single_dur, dT, "Telesat")
        end_time = time.time()
        telesat_times.append(end_time - start_time)
        print(end_time - start_time)

        start_time = time.time()
        oneweb_cons = constellation_configuration(single_dur, dT, "OneWeb")
        end_time = time.time()
        oneweb_times.append(end_time - start_time)
        print(end_time - start_time)

    path = "data/constellation_test/"
    os.system('mkdir -p ' + path)

    starlink_times = np.array(starlink_times)
    np.savetxt(path + 'starlink_times.txt', starlink_times)
    kuiper_times = np.array(kuiper_times)
    np.savetxt(path + 'kuiper_times.txt', kuiper_times)
    telesat_times = np.array(telesat_times)
    np.savetxt(path + 'telesat_times.txt', telesat_times)
    oneweb_times = np.array(oneweb_times)
    np.savetxt(path + 'oneweb.txt', oneweb_times)



if __name__ == '__main__':
    single_shell_performance()
