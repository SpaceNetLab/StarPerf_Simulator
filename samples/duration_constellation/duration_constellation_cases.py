"""
Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test constellation performance

"""

def constellation_performance():
    print("Calculate the time to simulate the first layer of multiple constellations")
    import samples.duration_constellation.simulation_performance.single_shell as SINGLE_SHELL
    SINGLE_SHELL.single_shell_performance()
    print("Simulation time cal is completed.")
    print()

    print("Calculate the delay between multiple samples")
    import samples.duration_constellation.network_performance.delay as DELAY
    DELAY.delay()
    print("Delay cal is completed.")
    print()

    print("Calculate the bandwidth between multiple samples")
    import samples.duration_constellation.network_performance.bandwidth as BANDWIDTH
    BANDWIDTH.bandwidth()
    print("Bandwidth cal is completed.")
    print()



if __name__ == '__main__':
    constellation_performance()

