# Constellation Connectivity

This section is also composed of "framework" and "plug-ins". The "framework" part is the "connectivity mode plugin manager". The "plug-ins" part is the connection method between satellites, such as +Grid.

## Overview

The connectivity module determines how Inter-Satellite Links (ISLs) are established between satellites in the constellation. Different connectivity patterns affect network topology, routing efficiency, and overall performance.

## Architecture

The connectivity module consists of:

1. **Framework**: `connectivity_mode_plugin_manager.py` - manages all connectivity mode plugins
2. **Plugins**: Various ISL establishment modes (e.g., `positive_Grid.py`, `bent_pipe.py`)

## Plug-ins

All plug-ins under this module are ISL establishment modes, and one plug-in represents a mode. We implement the +Grid mode and bent-pipe mode by default, and you can write other ISL establishment mode plug-ins by yourself according to the interface specifications.

### Interface Specifications

The interface specifications for connectivity plugins are as follows:

- **Requirement 1**: The storage location of the plug-in is (starting from the root of StarPerf 2.0): `src/TLE_constellation/constellation_connectivity/connectivity_plugin/` (for TLE constellation) or `src/XML_constellation/constellation_connectivity/connectivity_plugin/` (for XML constellation).

- **Requirement 2**: Each plug-in is a ".py" file, and all source code for the plug-in must be located in this script file.

- **Requirement 3**: The launch entry for a plug-in is a function with the same name as the plug-in.

- **Requirement 4**: The startup function parameter requirements are as follows:

**Table: ISL establishment mode plug-ins startup function parameter list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :------------: | :------------: | :------------: | :----------------------------------------------------------: |
| constellation | constellation | - | the constellation to establish ISL |
| dT | int | second | indicates how often the beam is scheduled, and this value must be less than the orbital period of the satellite |

- **Requirement 5**: The startup function has no return value.

- **Requirement 6**: After establishing the ISL, write the constellation delay matrix into a .h5 file. The Group name is: "delay", and the Dataset name is: "timeslot+\<number>" (such as "timeslot1", "timeslot2"), and the .h5 file storage path: `data/TLE_constellation/` (for TLE constellation) or `data/XML_constellation/` (for XML constellation).

## Framework

This part of the framework consists of 1 py script: `connectivity_mode_plugin_manager.py`. A connectivity mode plugin manager is defined in this script to manage all plug-ins under this module.

The so-called connectivity mode plugin manager actually defines a class named `connectivity_mode_plugin_manager`. The attributes and methods contained in this class and their functions and meanings are shown in the tables below.

### Attributes

**Table: connectivity mode plugin manager attributes list**

| Attribute Name | Attribute Type | Attribute Meaning |
| :---------------------: | :------------: | :----------------------------------------------------------: |
| plugins | dict | a dictionary composed of all plug-ins. The "key" is the plug-in name, which is a string type, and the "value" is the plug-in startup function in the corresponding plug-in, which is a function |
| current_connection_mode | str | plug-in name used by the current connectivity mode plugin manager |

### Methods

**Table: connectivity mode plugin manager methods list**

| Method Name | Parameter List<br />(name : type : unit) | Return Values | Method Function |
| :-----------------------: | :----------------------------------------------------------: | :-----------: | :----------------------------------------------------------: |
| \_\_init\_\_ | - | - | initialize an instance of the connectivity mode plugin manager |
| set_connection_mode | (plugin_name : str : -) | - | set the value of current_connection_mode to plugin_name |
| execute_connection_policy | (constellation : constellation : - , <br />dT : int : second) | - | according to the value of the current_connection_mode attribute, the startup function of the corresponding plug-in is called to execute the ISL establishment. |

## Operating Mechanism

The operating mechanism of this framework is:

1. First instantiate a connectivity mode plugin manager object. This object contains two attributes: `plugins` and `current_connection_mode`.
   - `plugins` is a dictionary type attribute used to store various connectivity mode plugins
   - `current_connection_mode` is a string type used to represent the connectivity mode plugin used by the current manager

2. During the instantiation of the manager object, the system automatically reads all connectivity mode plugins and stores them in the `plugins`. The key of `plugins` is the name of the plugin, and the value of `plugins` is the startup function of the plugin.

3. After reading all plug-ins, the system sets the value of `current_connection_mode` to "positive_Grid", indicating that the "positive_Grid" plug-in is used as the default connectivity mode plugin.

4. If you want to execute the connectivity mode, you only need to call the `execute_connection_policy` method of the manager object. This method will automatically call the startup function of the plug-in indicated by `current_connection_mode`.

5. If you need to switch the connectivity mode plug-in, just call the `set_connection_mode` method and pass in the plug-in name you need as a parameter.

6. After you write your own connectivity mode plug-in according to the interface specifications introduced earlier, you only need to set `current_connection_mode` as your plug-in name, and the system will automatically recognize your plug-in and execute it.

## Connectivity Modes

### +Grid Mode

The +Grid connectivity pattern establishes ISLs in a grid-like pattern, connecting satellites both within the same orbital plane and across adjacent orbital planes. This creates a mesh network topology that enables flexible routing.

### Bent-pipe Mode

In bent-pipe mode, satellites act as simple relays between ground stations without ISLs. All traffic must pass through ground stations, simplifying satellite design but limiting coverage and requiring more ground infrastructure.

## Case Study

Now, we take "positive_Grid" as an example to explain the operation of the constellation connectivity module.

### Step 1: Instantiate the Manager

```python
# initialize the connectivity mode plugin manager
connectionModePluginManager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
```

### Step 2: Set the Connectivity Mode Plugin

```python
connectionModePluginManager.current_connection_mode = "positive_Grid"
```

**Note**: The connectivity mode plugin manager already sets the `current_connection_mode` value to "positive_Grid" when initialized, so this step can be omitted here. But if you want to use other connectivity mode plugins, this step cannot be omitted.

### Step 3: Execute the Connection Policy

```python
connectionModePluginManager.execute_connection_policy(constellation=bent_pipe_constellation, dT=dT)
```

### Results

After execution, the constellation delay matrix will be written to the appropriate .h5 file, and the ISL topology will be established according to the selected connectivity pattern.

The complete code of the above process can be found at: `samples/XML_constellation/positive_Grid/*` and `samples/TLE_constellation/positive_Grid/*`.

## Creating Custom Connectivity Modes

To create your own connectivity mode:

1. Create a new Python file in the `connectivity_plugin/` directory
2. Implement a function with the same name as the file
3. Follow the parameter and return value specifications outlined above
4. Ensure the delay matrix is properly written to the .h5 file
5. The plugin will be automatically discovered and loaded by the manager

## Considerations for Connectivity Design

When designing or selecting a connectivity mode, consider:

- **Link Budget**: Can satellites maintain reliable ISLs at the required distances?
- **Pointing Complexity**: How many simultaneous links can each satellite maintain?
- **Handover Frequency**: How often do ISLs need to be reconfigured?
- **Routing Efficiency**: Does the topology support efficient path finding?
- **Fault Tolerance**: Can the network maintain connectivity if satellites fail?

## Navigation

- [Back to Core Modules Overview](../overview.md)
- [Previous: Beam Placement](../beam-placement/overview.md)
- [Next: Evaluation Overview](../evaluation/overview.md)
