

def visualization_test_cases():
    print("\t\t\033[31mTest(01/04) : 可视化Starlink\033[0m")
    import visualization.samples.Starlink as Starlink
    Starlink.Starlink()
    print("\t\tTest(01/04)结束")

    print("\t\t\033[31mTest(02/04) : 可视化Telesat\033[0m")
    import visualization.samples.Telesat as Telesat
    Telesat.Telesat()
    print("\t\tTest(02/04)结束")

    print("\t\t\033[31mTest(03/04) : 可视化OneWeb\033[0m")
    import visualization.samples.OneWeb as OneWeb
    OneWeb.OneWeb()
    print("\t\tTest(03/04)结束")

    print("\t\t\033[31mTest(04/04) : 可视化Boeing\033[0m")
    import visualization.samples.Boeing as Boeing
    Boeing.Boeing()
    print("\t\tTest(04/04)结束")