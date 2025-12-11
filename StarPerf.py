"""

StarPerf 2.0

Python version requirements : Python 3.10

Added implementation of security simulation

"""

def main():
    print("Starting StarPerf...")

    import src.constellation_generation.by_manual.constellation_information as constellation_information
    constellation_information.constellation_information("config/manual_constellation_generation_json_file/Example.json")

    print("Starting XML Constellations Testing...")
    # test the core module functionality of various XML constellations
    import samples.XML_constellation.XML_constellation_test_cases
    samples.XML_constellation.XML_constellation_test_cases.XML_constellation_test_cases()
    print("END.")

    print("Starting TLE Constellations Testing")
    # test the core module functionality of various TLE constellations
    import samples.TLE_constellation.TLE_constellation_test_cases
    samples.TLE_constellation.TLE_constellation_test_cases.TLE_constellation_test_cases()
    print("END.")

    print("Starting Standalone Module Testing...")
    # test each standalone module under "src/standalone_module/" in starperf 2.0
    import samples.standalone_module.standalone_module_test_cases as standalone_module_test_cases
    standalone_module_test_cases.standalone_module_test_cases()
    print("END.")

    print("Starting Tool Scripts Testing...")
    # test each tool script under "kits/" in starperf 2.0
    import samples.kits.kits_test_cases as KITS_TEST_CASES
    KITS_TEST_CASES.kits_test_cases()
    print("END.")

    """
    The visualization results generated here will be located under 
    /StarPerf_Simulator/visualization/CesiumApp. Before you uncomment 
    this section and run the visualization, please make sure to set your 
    own Cesium Token by assigning it to the Cesium.Ion.defaultAccessToken 
    parameter in /StarPerf_Simulator/visualization/html_head_tail/head.html
    
    For the specific steps of rendering the resulting web page, please 
    refer to the Constellation Visualization Instructions in README.md.
    """
    # print("Starting constellation visualization...")
    # # test visualization part in "visualization/" in starperf 2.0
    # import visualization.constellation_visualization as CONS_VIS_TEST_CASES
    # CONS_VIS_TEST_CASES.visualization_example()
    # print("END.")

    """
    This will test the functionality of duration constellation. It is similar to the previously 
    implemented XML Constellation, but supports customizing the simulation time and simulation 
    sampling interval (XML Constellation currently only supports simulation of the entire orbital period)
    """
    print("Start simulation performance and indicators testing")
    import samples.duration_constellation.duration_constellation_cases
    samples.duration_constellation.duration_constellation_cases.constellation_performance()
    print("END.")

    """
    This will take the longest time. On a 4-core Intel Xeon Processor (Icelake) processor, 
    1 second of traffic will be generated every 15 seconds. Therefore, the traffic generation 
    here is set to 10 seconds, although I generated 1000 seconds of traffic in the experiment.
    """
    print("Start benign traffic generation")
    import samples.traffic.traffic_generation_cases
    samples.traffic.traffic_generation_cases.traffic_generation()
    print("END.")

    """
    Energy consumption attacks require longer traffic generation time, because the implementation
    period of the attack is usually measured in months and years. In the example here, I only 
    implemented a simulation of dT=500 for one orbital period, which requires 11s of traffic generation.
    """
    print("Start LEO network security simulation")
    import samples.attack.attack_cases
    samples.attack.attack_cases.attack_cases()
    print("END.")
    


if __name__ == '__main__':
    #main()

    import src.constellation_generation.by_manual.constellation_information as constellation_information

    constellation_information.constellation_information("config/manual_constellation_generation_json_file/Example.json")

    