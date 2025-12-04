# Duration-based Constellation Generation

This method also constructs the constellation based on an XML file and makes slight modifications to the previously described `constellation_generation/by_duration/constellation_configuration.py` and `constellation_generation/by_duration/orbit_configuration.py` source codes, enabling satellite network simulation with both the simulation duration and sampling interval specified simultaneously.

## constellation_configuration.py

The startup function of this script is `constellation_generation/by_duration/constellation_configuration`.

### Function Parameters

**Table: constellation_configuration**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| duration | int | second | Total network simulation time. In previous XML and TLE simulations, this value was fixed to the satellite orbit period. |
| dT | int | second | indicates how often timestamps are recorded, and this value must be less than the orbital period of the satellite |
| constellation_name | str | - | the name of the constellation, the value of this parameter must have the same name as the subfolder in "config/TLE_constellation/". The configuration file of the constellation named by that name is stored in a subfolder with the same name. |
| shell_index | int | - | The constellation shell required for simulation. Currently, this function only supports single-layer satellite network simulation. |

### Key Differences from XML-based Generation

The main difference from the standard XML-based generation is the addition of the `duration` parameter, which allows you to:

- Specify a custom simulation timeframe rather than being limited to the satellite's orbital period
- Generate constellation data for exactly the time duration needed for your simulation
- Support time-constrained simulations where you don't need a full orbital period

For a detailed explanation of the underlying mechanism, please refer to the [XML-based Generation](xml-based.md) section, as this method is a fine-tuned version based on it.

## Case Study

You can use the following example to construct a constellation for a specified simulation time.

### Step 1: Set Parameters

Set the parameters according to the instructions given in the table above:

```python
duration = 100
dT = 1
cons_name = "Starlink"
shell_index = 1
```

### Step 2: Call the Generation Function

Call the `constellation_configuration` function to build the constellation topology:

```python
constellation = constellation_configuration(duration, dT, cons_name, shell_index=1)
```

### Step 3: Use the Constellation

After the above two steps, you have obtained a constellation configured for the specified duration. This constellation object can now be used with other StarPerf modules for:

- Traffic generation
- Performance evaluation
- Energy consumption modeling
- Attack simulation

## Use Cases

Duration-based generation is particularly useful for:

1. **Short-term simulations**: When you only need to analyze network behavior over a specific time window
2. **Resource-constrained environments**: When storage or computation limits prevent generating data for a full orbital period
3. **Targeted analysis**: When studying specific events or time periods in satellite network operation
4. **Rapid prototyping**: When you need quick results for initial testing or validation

## Navigation

- [Back to Constellation Generation Overview](overview.md)
- [Previous: TLE-based Generation](tle-based.md)
- [XML-based Generation](xml-based.md)
