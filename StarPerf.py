"""
Author : zhifenghan

Date : 2025/05/10

Function : Start network simulation to reproduce the results

"""

def main():
    print("Start simulation performance and performance indicators testing")
    import samples.duration_constellation.duration_constellation_cases
    samples.duration_constellation.duration_constellation_cases.constellation_performance()

    print("Start LEO network security simulation")
    import samples.attack.attack_cases
    samples.attack.attack_cases.attack_cases()

    print("END")


if __name__ == '__main__':
    main()