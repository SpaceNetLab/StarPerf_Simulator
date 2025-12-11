"""

Author : yunanhou

Date : 2025/12/11

Function : Generate constellations from JSON files

"""

import os
import json
import h5py


def constellation_information(constellation_json_file):
    """
    Read constellation information from a JSON file and generate an .h5 structure.

    JSON format example：
    {
        "Shells": [
            {
                "timeslots": [
                    {
                        "position": [
                            { "latitude": 56.5, "longitude": -20.1, "altitude": 550 },
                            { "latitude": 57.5, "longitude": -23.1, "altitude": 545 }
                        ],
                        "links": [
                            { "sat1": 0, "sat2": 1 }
                        ]
                    },
                    ...
                ]
            }
        ]
    }
    """

    # 1. read JSON file
    with open(constellation_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)


    shells_data = data["Shells"]
    number_of_shells = len(shells_data)

    # 2. The constellation name is derived from the JSON filename
    constellation_name = os.path.splitext(os.path.basename(constellation_json_file))[0]

    # 3. .h5 file path
    file_path = os.path.join("data", "Manual_constellation", f"{constellation_name}.h5")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # If old files exist, delete them.
    if os.path.exists(file_path):
        os.remove(file_path)

    # 4. Create an empty .h5 file and a position/shellX structure.
    with h5py.File(file_path, "w") as h5f:
        position_group = h5f.create_group("position")
        for shell_idx in range(1, number_of_shells + 1):
            position_group.create_group(f"shell{shell_idx}")


    # 6. Iterate through each shell layer and write the timeslot dataset.
    for shell_idx, shell_obj in enumerate(shells_data, start=1):
        timeslots = shell_obj.get("timeslots", [])
        number_of_timeslots = len(timeslots)

        shell_info = {
            "shell_id": shell_idx,
            "number_of_timeslots": number_of_timeslots,
            "number_of_satellites": None,
            "timeslots": []
        }

        for t_idx, ts in enumerate(timeslots, start=1):
            positions = ts.get("position", [])
            links = ts.get("links", [])

            if shell_info["number_of_satellites"] is None:
                shell_info["number_of_satellites"] = len(positions)

            # Construct a two-dimensional array to be written to the .h5 file: [[lon, lat, alt], ...]
            satellite_position = []
            for sat in positions:
                lat = sat.get("latitude")
                lon = sat.get("longitude")
                alt = sat.get("altitude")
                satellite_position.append([str(lon), str(lat), str(alt)])

            # Write the current timeslot dataset to h5
            with h5py.File(file_path, "a") as h5f:
                position_group = h5f["position"]
                current_shell_group = position_group[f"shell{shell_idx}"]
                current_shell_group.create_dataset(f"timeslot{t_idx}", data=satellite_position)


