'''

StarPerf 2.0

Python version requirements : Python 3.10

'''

# Entrance of StarPerf



def main():
    print("\033[31mStarting StarPerf...\033[0m")


    print("\t\033[31mStarting XML Constellations Testing...\033[0m")
    # test the core module functionality of various XML constellations
    import samples.XML_constellation.XML_constellation_test_cases
    samples.XML_constellation.XML_constellation_test_cases.XML_constellation_test_cases()
    print("\t\033[31mEND.\033[0m")

    print("\t\033[31mStarting TLE Constellations Testing...\033[0m")
    # test the core module functionality of various TLE constellations
    import samples.TLE_constellation.TLE_constellation_test_cases
    samples.TLE_constellation.TLE_constellation_test_cases.TLE_constellation_test_cases()
    print("\t\033[31mEND.\033[0m")

    print("\t\033[31mStarting Standalone Module Testing...\033[0m")
    # test each standalone module under "src/standalone_module/" in starperf 2.0
    import samples.standalone_module.standalone_module_test_cases as standalone_module_test_cases
    standalone_module_test_cases.standalone_module_test_cases()
    print("\t\033[31mEND.\033[0m")

    print("\t\033[31mStarting Tool Scripts Testing...\033[0m")
    # test each tool script under "kits/" in starperf 2.0
    import samples.kits.kits_test_cases as KITS_TEST_CASES
    KITS_TEST_CASES.kits_test_cases()
    print("\t\033[31mEND.\033[0m")


    print("\033[31mEND.\033[0m")

if __name__ == '__main__':
    main()




