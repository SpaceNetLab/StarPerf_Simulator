"""
Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test multi link ICARUS attack and get the results

"""


from src.constellation_generation.by_duration.constellation_configuration import constellation_configuration
import src.XML_constellation.constellation_attack.attack_plugin_manager as attack_plugin_manager
import numpy as np
import os

cons_name = 'Starlink'
altitude = 550
orbit_num = 72
sat_per_cycle = 22
inclination = 53
average_gsl_num = 574 # average_gsl_num for starlink

ratios = [0.9, 0.8, 0.7, 0.6, 0.5]
target_affected_traffic = [100000, 200000, 250000, 300000]
traffic_thre = 20  # upmost 20 malicious terminals accessed to a satellite
GSL_capacity = 4096
unit_traffic = 20   # 20Mbps per malicious terminal


def multi_link_attack():
    duration = 10
    dT = 1

    constellation = constellation_configuration(duration, dT, "Starlink")
    attackPluginManage = attack_plugin_manager.attack_plugin_manager()
    attackPluginManage.set_attack_model('positive_grid_icarus')

    for ratio in ratios:
        for traffic in target_affected_traffic:
            for t in range(1, duration+1):
                attackPluginManage.execute_icarus_attack(constellation, t, ratio, traffic)
                print("Finished calculating malicious terminals deployment and generating " + str(traffic) + " Mbps malicious traffic at timeslot " + str(t) + " with ratio " + str(ratio))

    output_path = os.path.join("data", f"{cons_name}_icarus", "results")
    os.makedirs(output_path, exist_ok=True)

    legal_traffic = []
    traffic_data_root = os.path.join("data", f"{cons_name}_link_traffic_data")
    for subdir in os.listdir(traffic_data_root):
        subdir_path = os.path.join(traffic_data_root, subdir)
        if os.path.isdir(subdir_path):
            # background traffic
            downlink_traffic_file_path = os.path.join(subdir_path, 'downlink_traffic.txt')
            if os.path.exists(downlink_traffic_file_path):
                with open(downlink_traffic_file_path, 'r') as file:
                    values = [float(line.strip()) for line in file]
                    total = sum(values)
                    legal_traffic.append(total / 1024)

    output_file = os.path.join("data", f"{cons_name}_icarus", "results", "background_traffic_without_attack.txt")
    with open(output_file, 'w') as file:
        for value in legal_traffic:
            file.write(str(value) + '\n')

    folder_path = os.path.join(
        "data", f"{cons_name}_icarus", "attack_traffic_data_land_only_bot",
        f"0.5-300000-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}"
    )
    icarus_traffic = []
    traffic_ratios = []
    gsl_ratios = []

    time_slot = 0
    for subdir in os.listdir(folder_path):
        subdir_path = os.path.join(folder_path, subdir)
        if os.path.isdir(subdir_path):
            # (Ratio of) reduced traffic by icarus
            icarus_traffic_file_path = os.path.join(subdir_path, 'cumu_affected_traffic_volume_given_bot_num.txt')
            if os.path.exists(icarus_traffic_file_path):
                with open(icarus_traffic_file_path, 'r') as file:
                    values = [float(line.strip()) for line in file]
                    total = sum(values)
                    icarus_traffic.append(total / 1024)
                    traffic_ratios.append(icarus_traffic[-1] / legal_traffic[time_slot])
            # (Ratio of) attacked GSLs by icarus
            attack_gsl_file_path = os.path.join(subdir_path, 'attack_gsl_given_bot_num.txt')
            if os.path.exists(attack_gsl_file_path):
                with open(attack_gsl_file_path, 'r') as file:
                    values = [float(line.strip()) for line in file]
                    if values != []:
                        gsl_ratios.append((len(values)) / average_gsl_num)
                    else:
                        gsl_ratios.append(0)
        time_slot += 1

    output_file = os.path.join("data", f"{cons_name}_icarus", "results", "ratio_of_reduced_background_traffic_by_icarus.txt")
    with open(output_file, 'w') as file:
        for value in traffic_ratios:
            file.write(str(value) + '\n')
    output_file = os.path.join("data", f"{cons_name}_icarus", "results", "ratio_of_attacked_GSLs_by_icarus.txt")
    with open(output_file, 'w') as file:
        for value in gsl_ratios:
            file.write(str(value) + '\n')
    actual_throughput_icarus = [a - b for a, b in zip(legal_traffic, icarus_traffic)]
    output_file = os.path.join("data", f"{cons_name}_icarus", "results", "actual_throughput_icarus.txt")
    with open(output_file, 'w') as file:
        for value in actual_throughput_icarus:
            file.write(str(value) + '\n')

    for traffic in target_affected_traffic:
        botnet_size_for_icarus = []
        for ratio in ratios:
            icarus_folder_path = os.path.join(
                "data", f"{cons_name}_icarus", "attack_traffic_data_land_only_bot",
                f"{ratio}-{traffic}-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}"
            )
            # icarus bot_num
            icarus_bot_size = []
            for subdir in os.listdir(icarus_folder_path):
                subdir_path = os.path.join(icarus_folder_path, subdir)
                if os.path.isdir(subdir_path):
                    icarus_botnum_file_path = os.path.join(subdir_path, 'bot_num.txt')
                    if os.path.exists(icarus_botnum_file_path):
                        with open(icarus_botnum_file_path, 'r') as file:
                            values = [float(line.strip()) for line in file]
                            if values[0] > 0:
                                icarus_bot_size.append(values[0])
            botnet_size_for_icarus.append(int(sum(icarus_bot_size) / len(icarus_bot_size)))

        output_file = os.path.join("data", f"{cons_name}_icarus", "results", f"{traffic}_botnet_size_for_icarus.txt")
        with open(output_file, 'w') as file:
            for i in range(len(ratios)):
                file.write(str(round(1 - ratios[i], 1)) + ": " + str(botnet_size_for_icarus[i]) + '\n')

        number_blocks_icarus = []
        for index, ratio in enumerate(ratios):
            icarus_folder_path = os.path.join(
                "data", f"{cons_name}_icarus", "attack_traffic_data_land_only_bot",
                f"{ratio}-{traffic}-{traffic_thre}-{sat_per_cycle}-{GSL_capacity}-{unit_traffic}"
            )
            # icarus block_num
            icarus_block_num = []
            for subdir in os.listdir(icarus_folder_path):
                subdir_path = os.path.join(icarus_folder_path, subdir)
                if os.path.isdir(subdir_path):
                    icarus_block_num_file_path = os.path.join(subdir_path, 'block_num.txt')
                    if os.path.exists(icarus_block_num_file_path):
                        with open(icarus_block_num_file_path, 'r') as file:
                            values = [float(line.strip()) for line in file]
                            icarus_block_num.append(values[0])
            number_blocks_icarus.append(int(sum(icarus_block_num) / len(icarus_block_num)))

        output_file = os.path.join("data", f"{cons_name}_icarus", "results", f"{target_affected_traffic[2]}_number_blocks_icarus.txt")
        with open(output_file, 'w') as file:
            for i in range(len(ratios)):
                file.write(str(round(1 - ratios[i], 1)) + ": " + str(number_blocks_icarus[i]) + '\n')



if __name__ == '__main__':
    multi_link_attack()

