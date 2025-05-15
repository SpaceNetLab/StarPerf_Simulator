"""
Author : zhifenghan

Date : 2025/05/10

Function : Start network simulation to reproduce the results

"""

def main():
    print("Start simulation performance and indicators testing")
    import samples.duration_constellation.duration_constellation_cases
    samples.duration_constellation.duration_constellation_cases.constellation_performance()

    """
    This will take the longest time. On a 4-core Intel Xeon Processor (Icelake) processor, 
    1 second of traffic will be generated every 15 seconds. Therefore, the traffic generation 
    here is set to 10 seconds, although I generated 1000 seconds of traffic in the experiment.
    """
    print("Start benign traffic generation")
    import samples.traffic.traffic_generation_cases
    samples.traffic.traffic_generation_cases.traffic_generation()

    """
    Energy consumption attacks require longer traffic generation time (11s)
    """
    print("Start LEO network security simulation")
    import samples.attack.attack_cases
    samples.attack.attack_cases.attack_cases()

    print("END")


if __name__ == '__main__':
    main()
    