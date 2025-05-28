"""
Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test StarMelt energy drain attack and get the results

"""

from src.constellation_generation.by_duration.constellation_configuration import constellation_configuration
import src.XML_constellation.constellation_traffic.traffic_plugin_manager as traffic_plugin_manager
import src.XML_constellation.constellation_attack.attack_plugin_manager as attack_plugin_manager
import numpy as np
import os

def energy_drain():
    duration = 5731
    dT = 500
    time_slot = (int)(duration / dT)
    cons_name = 'Starlink'
    bot_nums = [50, 100, 200, 300, 400, 500]
    constellation = constellation_configuration(duration, dT, cons_name, shell_index=1)

    Traffic = traffic_plugin_manager.traffic_plugin_manager()
    for t in range(1, time_slot + 1):
        Traffic.execute_traffic_policy(constellation, t)

    Attack = attack_plugin_manager.attack_plugin_manager()
    Attack.set_attack_model("positive_grid_energy_drain")

    for bot_num in bot_nums:
        for t in range(1, time_slot + 1):
            Attack.execute_energy_drain_attack(constellation, t, 30, bot_num, 40)
            print("Complete energy drain attack at timeslot " + str(t) + " with bot num " + str(bot_num))

        attack_laser_energy = [0] * 1584
        attack_radio_energy = [0] * 1584
        ori_laser_energy = [0] * 1584
        ori_radio_energy = [0] * 1584
        addbase_attack_radio_energy = [0] * 1584
        addbase_attack_laser_energy = [0] * 1584
        addbase_ori_radio_energy = [0] * 1584
        addbase_ori_laser_energy = [0] * 1584

        for t in range(1, time_slot + 1):
            path = os.path.join("data", f"{cons_name}_energy_drain", f"energy_{bot_num}", str(t))
            attack_laser = np.loadtxt(os.path.join(path, 'attack_laser_energy.txt'))
            attack_laser = list(map(int, attack_laser))
            attack_radio = np.loadtxt(os.path.join(path, 'attack_radio_energy.txt'))
            attack_radio = list(map(int, attack_radio))
            attack_all_radio_energy = np.loadtxt(os.path.join(path, 'attack_all_radio_energy.txt'))
            attack_all_radio_energy = list(map(int, attack_all_radio_energy))
            attack_all_laser_energy = np.loadtxt(os.path.join(path, 'attack_all_laser_energy.txt'))
            attack_all_laser_energy = list(map(int, attack_all_laser_energy))
            ori_laser = np.loadtxt(os.path.join(path, 'ori_laser_energy.txt'))
            ori_laser = list(map(int, ori_laser))
            ori_radio = np.loadtxt(os.path.join(path, 'ori_radio_energy.txt'))
            ori_radio = list(map(int, ori_radio))
            ori_all_radio_energy = np.loadtxt(os.path.join(path, 'ori_all_radio_energy.txt'))
            ori_all_radio_energy = list(map(int, ori_all_radio_energy))
            ori_all_laser_energy = np.loadtxt(os.path.join(path, 'ori_all_laser_energy.txt'))
            ori_all_laser_energy = list(map(int, ori_all_laser_energy))

            for sat in range(1584):
                attack_laser_energy[sat] += attack_laser[sat]
                attack_radio_energy[sat] += attack_radio[sat]
                ori_laser_energy[sat] += ori_laser[sat]
                ori_radio_energy[sat] += ori_radio[sat]
                addbase_attack_radio_energy[sat] += attack_all_radio_energy[sat]
                addbase_attack_laser_energy[sat] += attack_all_laser_energy[sat]
                addbase_ori_radio_energy[sat] += ori_all_radio_energy[sat]
                addbase_ori_laser_energy[sat] += ori_all_laser_energy[sat]

        path = os.path.join("data", f"{cons_name}_energy_drain", f"energy_{bot_num}")
        ori_radio_energy = np.array(ori_radio_energy)
        np.savetxt(os.path.join(path, 'all_ori_radio_energy.txt'), ori_radio_energy, fmt='%.3f')
        ori_laser_energy = np.array(ori_laser_energy)
        np.savetxt(os.path.join(path, 'all_ori_laser_energy.txt'), ori_laser_energy, fmt='%.3f')
        attack_radio_energy = np.array(attack_radio_energy)
        np.savetxt(os.path.join(path, 'all_attack_radio_energy.txt'), attack_radio_energy, fmt='%.3f')
        attack_laser_energy = np.array(attack_laser_energy)
        np.savetxt(os.path.join(path, 'all_attack_laser_energy.txt'), attack_laser_energy, fmt='%.3f')
        addbase_attack_radio_energy = np.array(addbase_attack_radio_energy)
        np.savetxt(os.path.join(path, 'addbase_attack_radio_energy.txt'), addbase_attack_radio_energy, fmt='%.3f')
        addbase_attack_laser_energy = np.array(addbase_attack_laser_energy)
        np.savetxt(os.path.join(path, 'addbase_attack_laser_energy.txt'), addbase_attack_laser_energy, fmt='%.3f')
        addbase_ori_radio_energy = np.array(addbase_ori_radio_energy)
        np.savetxt(os.path.join(path, 'addbase_ori_radio_energy.txt'), addbase_ori_radio_energy, fmt='%.3f')
        addbase_ori_laser_energy = np.array(addbase_ori_laser_energy)
        np.savetxt(os.path.join(path, 'addbase_ori_laser_energy.txt'), addbase_ori_laser_energy, fmt='%.3f')

