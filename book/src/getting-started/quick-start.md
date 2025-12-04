# Quick Start

This guide will help you run your first StarPerf simulation in just a few minutes.

## Running the Example Simulation

The easiest way to get started is to run the provided example:

```bash
uv run python StarPerf.py
```

This command will execute a default simulation configured in `StarPerf.py`.

## Understanding StarPerf.py

The `StarPerf.py` file serves as the entry point for simulations. It typically includes:

1. **Configuration**: Set simulation parameters
2. **Constellation Generation**: Create or load constellation data
3. **Performance Evaluation**: Run analysis on the constellation
4. **Results Output**: Save and visualize results

## Your First Custom Simulation

Let's create a simple custom simulation script. Create a new file called `my_simulation.py`:

```python
# Import required modules
from src.constellation_generation.by_XML import constellation_configuration

# Define simulation parameters
dT = 5730  # Timestamp interval in seconds
constellation_name = "Starlink"  # Name of constellation

# Generate constellation
print("Generating constellation...")
constellation = constellation_configuration.constellation_configuration(
    dT=dT,
    constellation_name=constellation_name
)

# Print basic information
print(f"\nConstellation: {constellation_name}")
print(f"Number of shells: {len(constellation.shells)}")
print(f"Total satellites: {sum(len(shell.satellites) for shell in constellation.shells)}")
print("\nSimulation complete!")
```

Run your simulation:

```bash
uv run python my_simulation.py
```

### Step-by-Step Breakdown

(1) Define Parameters

```python
dT = 5730  # How often to record timestamps
constellation_name = "Starlink"
h3_resolution = 2  # Geospatial resolution
minimum_elevation = 25  # Minimum elevation angle (degrees)
```

(2) Generate Constellation

Choose between XML or TLE-based generation:

**XML-based (theoretical constellation):**

```python
from src.constellation_generation.by_XML import constellation_configuration

constellation = constellation_configuration.constellation_configuration(
    dT=dT,
    constellation_name=constellation_name
)
```

**TLE-based (real constellation):**

```python
from src.constellation_generation.by_TLE import constellation_configuration

constellation = constellation_configuration.constellation_configuration(
    dT=dT,
    constellation_name=constellation_name
)
```

(3) Configure Connectivity

```python
from src.XML_constellation.constellation_connectivity import connectivity_mode_plugin_manager

# Initialize connectivity manager
conn_manager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()

# Set connection mode (e.g., +Grid)
conn_manager.set_connection_mode("positive_Grid")

# Execute connectivity policy
conn_manager.execute_connection_policy(
    constellation=constellation,
    dT=dT
)
```

(4) Evaluate Performance

```python
from src.XML_constellation.constellation_evaluation import evaluation

# Calculate coverage
coverage_results = evaluation.coverage(
    constellation_name=constellation_name,
    dT=dT,
    sh=constellation.shells[0],
    tile_size=10,
    minimum_elevation=25
)

print(f"Average coverage: {sum(coverage_results)/len(coverage_results):.2f}")
```

## Next Steps

Now that you've run your first simulation, explore more:

- **[User Guide](../user-guide/introduction.md)** 
    - Understand the architecture in depth
- **[Core Modules](../core-modules/overview.md)** 
    - Learn about different functional modules
- **[Examples](../examples/overview.md)** 
    - Study detailed example scenarios
- **[API Reference](../api-reference/introduction.md)** 
    - Dive into the programming interfaces

Happy simulating with StarPerf!