'''

Author: yunanhou

Date : 2023/12/25

Function : This script is used to test each tool script under "src/standalone_module/" in starperf 2.0

'''






def standalone_module_test_cases():
    print("\t\t\033[31mTest(01/04) : calculate the length of time a user can see a satellite\033[0m")
    # calculate the length of time a user can see a satellite
    import src.standalone_module.satellite_visibility_time as SATELLITE_VISIBILITY_TIME
    θ = 25 # the lowest elevation angle at which the user can see the satellite (unit: degrees)
    h = 550 # the height of a satellite's orbit above the earth's surface, in kilometers
    visibility_time = SATELLITE_VISIBILITY_TIME.satellite_visibility_time(θ , h)
    print("\t\t\tWhen the lowest elevation angle at which a user can see a satellite is " + str(θ) + \
          "° and the satellite orbit height is " + str(h) + " km, the user can see a satellite for " + \
          str(round(visibility_time,2)) + " s.")

    print("\t\t\033[31mTest(02/04) : calculate satellite orbital period\033[0m")
    # calculate satellite orbital period
    import src.standalone_module.satellite_orbital_period as SATELLITE_ORBITAL_PERIOD
    h = 550 # the height of a satellite's orbit above the earth's surface, in kilometers
    orbital_period = SATELLITE_ORBITAL_PERIOD.satellite_orbital_period(h)
    print("\t\t\tWhen the satellite orbit height is " + str(h) + " km, the satellite orbital period is " + \
          str(round(orbital_period,2)) + " s.")

    print("\t\t\033[31mTest(03/04) : calculate satellite redundancy\033[0m")
    import src.standalone_module.satellite_redundancy as satellite_redundancy
    satellite_redundancy.satellite_redundancy(1, "OneWeb", 1000,
                                              "XML")

    print("\t\t\033[31mTest(04/04) : calculate polar constellation coverage ratios\033[0m")
    import src.standalone_module.polar_constellation_coverage as POLAR_CONSTELLATION_COVERAGE
    POLAR_CONSTELLATION_COVERAGE.start("Polar", 25)


if __name__ == '__main__':
    standalone_module_test_cases()