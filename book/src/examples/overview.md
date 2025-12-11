# Examples Overview

This section provides practical examples demonstrating how to use StarPerf for various simulation scenarios.

## Available Examples

StarPerf includes comprehensive examples in the `samples/` directory, organized by functionality:

### Constellation Generation Examples

Learn how to create satellite constellations:
- [XML Constellation Example](./xml-constellation.md) - Building theoretical constellations
- [TLE Constellation Example](./tle-constellation.md) - Working with real constellation data

### Functional Module Examples

Explore specific features:
- [Beam Placement Example](./beam-placement.md) - Implementing beam placement algorithms
- [Connectivity Example](./connectivity.md) - Configuring satellite connectivity modes
- [Performance Evaluation Example](./evaluation.md) - Measuring constellation performance

### Advanced Examples

Specialized use cases:
- [Traffic Generation Example](./traffic-generation.md) - Simulating network traffic patterns
- [Attack Simulation Example](./attack-simulation.md) - Modeling security threats

## Example Directory Structure

```
samples/
├── XML_constellation/          # XML-based constellation examples
│   ├── constellation_generation/
│   │   └── constellation_generation_test.py
│   ├── beam_placement/
│   │   └── random_placement.py
│   ├── positive_Grid/
│   │   └── grid_connectivity.py
│   └── evaluation/
│       └── performance_metrics.py
├── TLE_constellation/          # TLE-based constellation examples
│   ├── constellation_generation/
│   │   └── constellation_generation_test.py
│   ├── beam_placement/
│   │   └── random_placement.py
│   └── positive_Grid/
│       └── grid_connectivity.py
├── duration_constellation/     # Duration-based examples
│   └── duration_test.py
├── standalone_module/          # Independent function examples
│   └── standalone_module_test_cases.py
├── traffic/                    # Traffic simulation examples
│   └── traffic_generation_cases.py
└── attack/                     # Attack simulation examples
    └── ICARUS/
        └── single_link.py
```

## Running Examples

All examples can be run using the `uv run` command:

```bash
# XML constellation generation
uv run python samples/XML_constellation/constellation_generation/constellation_generation_test.py

# TLE constellation generation
uv run python samples/TLE_constellation/constellation_generation/constellation_generation_test.py

# Beam placement
uv run python samples/XML_constellation/beam_placement/random_placement.py

# Traffic generation
uv run python samples/traffic/traffic_generation_cases.py
```

## Common Patterns

### Basic Simulation Pattern

Most examples follow this structure:

```python
# 1. Import required modules
from src.constellation_generation.by_XML import constellation_configuration
from src.XML_constellation.constellation_connectivity import connectivity_mode_plugin_manager
from src.XML_constellation.constellation_evaluation import evaluation

# 2. Define parameters
dT = 5730
constellation_name = "Starlink"

# 3. Generate constellation
constellation = constellation_configuration.constellation_configuration(
    dT=dT,
    constellation_name=constellation_name
)

# 4. Configure connectivity
conn_manager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
conn_manager.set_connection_mode("positive_Grid")
conn_manager.execute_connection_policy(constellation=constellation, dT=dT)

# 5. Evaluate performance
results = evaluation.coverage(
    constellation_name=constellation_name,
    dT=dT,
    sh=constellation.shells[0]
)

# 6. Process and display results
print(f"Average coverage: {sum(results)/len(results):.2f}")
```

### Plugin Usage Pattern

When using plugins (beam placement, connectivity, routing):

```python
# 1. Initialize plugin manager
manager = plugin_manager_class()

# 2. Set desired plugin
manager.set_policy("plugin_name")

# 3. Execute plugin with parameters
result = manager.execute_policy(
    constellation=constellation,
    # ... other parameters
)

# 4. Process results
# ... work with returned data
```

## Example Workflows

### Workflow 1: Basic Constellation Analysis

```python
# Generate constellation → Configure connectivity → Evaluate performance

from src.constellation_generation.by_XML import constellation_configuration
from src.XML_constellation.constellation_connectivity import connectivity_mode_plugin_manager
from src.XML_constellation.constellation_evaluation import evaluation

# Generate
constellation = constellation_configuration.constellation_configuration(
    dT=5730,
    constellation_name="Starlink"
)

# Connect
conn_mgr = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
conn_mgr.execute_connection_policy(constellation=constellation, dT=5730)

# Evaluate
coverage = evaluation.coverage(
    constellation_name="Starlink",
    dT=5730,
    sh=constellation.shells[0]
)
```

### Workflow 2: Comparative Analysis

```python
# Compare multiple constellations or configurations

constellations = ["Starlink", "OneWeb", "Telesat"]
results = {}

for const_name in constellations:
    constellation = constellation_configuration.constellation_configuration(
        dT=5730,
        constellation_name=const_name
    )

    coverage = evaluation.coverage(
        constellation_name=const_name,
        dT=5730,
        sh=constellation.shells[0]
    )

    results[const_name] = {
        'avg_coverage': sum(coverage) / len(coverage),
        'num_satellites': sum(len(sh.satellites) for sh in constellation.shells)
    }

# Display comparison
for name, data in results.items():
    print(f"{name}: {data['num_satellites']} satellites, {data['avg_coverage']:.2f} coverage")
```

### Workflow 3: Time-Series Analysis

```python
# Analyze performance over time

import matplotlib.pyplot as plt

# Generate constellation
constellation = constellation_configuration.constellation_configuration(
    dT=1000,  # Record every 1000 seconds
    constellation_name="Starlink"
)

# Configure connectivity
conn_mgr.execute_connection_policy(constellation=constellation, dT=1000)

# Calculate coverage for each timeslot
coverage_over_time = evaluation.coverage(
    constellation_name="Starlink",
    dT=1000,
    sh=constellation.shells[0]
)

# Plot results
plt.plot(coverage_over_time)
plt.xlabel('Timeslot')
plt.ylabel('Coverage (%)')
plt.title('Starlink Coverage Over Time')
plt.savefig('coverage_analysis.png')
```

## Customizing Examples

### Modifying Parameters

Key parameters you can adjust:

```python
# Time parameters
dT = 1000              # Timestamp interval (seconds)
duration = 86400       # Simulation duration (seconds)

# Spatial parameters
h3_resolution = 2      # Grid resolution (0-4)
minimum_elevation = 25 # Minimum elevation angle (degrees)
tile_size = 10         # Coverage tile size (degrees)

# Constellation parameters
constellation_name = "Starlink"
shell_index = 0        # Which shell to analyze

# Connectivity parameters
isl_capacity = 5.0     # ISL bandwidth (Gbps)
connection_mode = "positive_Grid"

# Beam parameters
antenna_count_per_satellite = 8
beam_placement_policy = "random_placement"
```

### Adding Custom Logic

You can extend examples with custom analysis:

```python
# Custom metric calculation
def calculate_custom_metric(constellation, dT):
    """Calculate a custom performance metric"""
    # Your custom logic here
    metric_values = []

    for timeslot in range(num_timeslots):
        # Compute metric for this timeslot
        value = compute_metric(constellation, timeslot)
        metric_values.append(value)

    return metric_values

# Use in your simulation
results = calculate_custom_metric(constellation, dT)
print(f"Custom metric average: {sum(results)/len(results):.2f}")
```

## Tips for Using Examples

1. **Start Simple**: Begin with basic constellation generation examples
2. **Read the Code**: Examples include comments explaining each step
3. **Modify Parameters**: Experiment with different configurations
4. **Compare Results**: Run multiple examples to understand differences
5. **Check Output**: Look in `data/` directory for generated files
6. **Use Visualization**: Combine with visualization to see results visually

## Common Issues and Solutions

### Issue: Example Fails to Run

**Solution**: Ensure all dependencies are installed:
```bash
uv sync
```

### Issue: Missing Configuration Files

**Solution**: Verify configuration files exist:
```bash
ls config/XML_constellation/
ls config/TLE_constellation/
```

### Issue: Out of Memory

**Solution**: For large constellations, increase dT or reduce simulation duration:
```python
dT = 5730  # Larger interval = fewer timeslots = less memory
```

## Next Steps

Dive into specific examples:
- [XML Constellation Example](./xml-constellation.md) - Start here for beginners
- [TLE Constellation Example](./tle-constellation.md) - Work with real data
- [Performance Evaluation Example](./evaluation.md) - Analyze results

Or explore:
- [Core Modules](../core-modules/overview.md) - Understand the underlying systems
- [API Reference](../api-reference/introduction.md) - Detailed interface documentation
