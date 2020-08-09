# -*- coding: UTF-8 -*-
import sp_utils
import json

config_folder = "etc/"
constellation_config_file = "constellation.config"
ground_station_config_file = "gstation.config"
network_policy_config_file = "route.config"


class constellation_config:
    def __init__(self):
        self.id = 0
        self.name = "Default Constellation"
        self.inclination = []
        self.altitude = []
        self.num_satellite = 0
        self.phase_shift = []
        self.orbit_num = []
        self.satellite_num = []
        self.link_band = []
        self.link_type = []


#call the default configurations if no config files are specified.
def default_init_config_files():
    starlink_constellation = {
        "id": "0",
        "name": "starlink",
        "inclination": 53,
        "altitude": 550,
        "num_satellite": 1584,
        "phase_shift": 1,
        "orbit_num": 24,
        "satellite_num": 66,
        "link_band": "Ka",
    }
    oneweb_constellation = {
        "id": "1",
        "name": "starlink",
        "inclination": 89.7,
        "altitude": 1200,
        "num_satellite": 720,
        "phase_shift": 0,
        "orbit_num": 18,
        "satellite_num": 40,
        "link_band": "Ka",
    }
    telesat_polar_constellation = {
        "id": "2",
        "name": "telasat(polar)",
        "inclination": 99.5,
        "altitude": 1000,
        "num_satellite": 72,
        "phase_shift": 0,
        "orbit_num": 6,
        "satellite_num": 12,
        "link_band": "Ka",
    }
    telesat_inclined_constellation = {
        "id": "3",
        "name": "telasat(inclined)",
        "inclination": 37.4,
        "altitude": 1200,
        "num_satellite": 50,
        "phase_shift": 0,
        "orbit_num": 5,
        "satellite_num": 10,
        "link_band": "Ka",
    }
    json_data = {"constellation": [starlink_constellation, oneweb_constellation, telesat_polar_constellation, telesat_inclined_constellation]}

    config_file_name = "etc/constellation.json"
    sp_utils.sp_create_file_if_not_exit(config_file_name)
    config_file = open(config_file_name, "w+")
    json.dump(json_data, config_file)
    return

def init_config_files():
    default_init_config_files()
    return

if __name__ == '__main__':
    init_config_files()
