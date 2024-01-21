'''

Author: yunanhou

Date : 2023/12/25

Function : This script is used to test each tool script under "src/standalone_module/" in starperf 2.0

'''






def standalone_module_test_cases():
    print("\t\t\033[31mTest(01/01) : calculate the length of time a user can see a satellite\033[0m")
    # calculate the length of time a user can see a satellite
    import src.standalone_module.satellite_visibility_time as SATELLITE_VISIBILITY_TIME
    θ = 25 # the lowest elevation angle at which the user can see the satellite (unit: degrees)
    h = 550 # the height of a satellite's orbit above the earth's surface, in kilometers
    visibility_time = SATELLITE_VISIBILITY_TIME.satellite_visibility_time(θ , h)
    print("\t\t\tWhen the lowest elevation angle at which a user can see a satellite is " + str(θ) + \
          "° and the satellite orbit height is " + str(h) + " km, the user can see a satellite for " + \
          str(round(visibility_time,2)) + " s.")

