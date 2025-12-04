# API Reference Introduction

This section provides detailed documentation of StarPerf's programming interfaces, helping you understand and extend the platform.

## Overview

StarPerf 2.0 follows a **"Framework + Plugin"** architecture, where:

- **Framework**: Provides core functionality and standardized APIs
- **Plugins**: Implement specific features using the framework's APIs

This design enables high extensibility while maintaining consistency across the platform.

## API Categories

### 1. Entity Classes

Core data structures representing constellation components:
- `Constellation` - Complete satellite network
- `Shell` - Orbital shell within a constellation
- `Orbit` - Circular path containing satellites
- `Satellite` - Individual spacecraft
- `GroundStation` - Ground infrastructure
- `User` - Communication endpoint
- `POP` - Point of presence

[Learn more →](./entities.md)

### 2. Plugin Interfaces

Standardized interfaces for extending functionality:
- **Beam Placement Plugins** - Satellite beam scheduling algorithms
- **Connectivity Plugins** - Inter-satellite link establishment
- **Routing Plugins** - Path selection strategies
- **Survivability Plugins** - Damage and failure modeling

[Learn more →](./plugin-interfaces.md)

### 3. Utility Functions

Helper functions for common operations:
- Position calculations
- Distance computations
- Coverage analysis
- Data I/O operations

[Learn more →](./utilities.md)

## API Design Principles

### 1. Consistency

All plugins follow the same patterns:
```python
# Every plugin has:
# 1. Standard location in src/[constellation_type]/[module]/[category]_plugin/
# 2. Entry function with same name as file
# 3. Standardized parameter list
# 4. Well-defined return values
```

### 2. Type Safety

Functions use clear type hints:
```python
def constellation_configuration(
    dT: int,
    constellation_name: str
) -> Constellation:
    """
    Generate constellation from XML configuration.

    Args:
        dT: Timestamp interval in seconds
        constellation_name: Name of constellation

    Returns:
        Constellation object
    """
    pass
```

### 3. Documentation

Every function includes:
- Purpose description
- Parameter specifications (name, type, unit, meaning)
- Return value description
- Usage examples

### 4. Extensibility

Clear interfaces enable custom implementations:
```python
# Write your own plugin following the interface:
def my_custom_routing(constellation: Constellation, dT: int) -> None:
    """
    Custom routing strategy.

    Must follow routing plugin interface specifications.
    """
    # Your implementation here
    pass
```

## Common API Patterns

### Pattern 1: Manager-Based Plugin Execution

Most plugins use a manager for execution:

```python
# 1. Import manager
from src.XML_constellation.constellation_connectivity import connectivity_mode_plugin_manager

# 2. Instantiate manager
manager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()

# 3. Set plugin
manager.set_connection_mode("positive_Grid")

# 4. Execute
manager.execute_connection_policy(
    constellation=constellation,
    dT=dT
)
```

### Pattern 2: Direct Function Call

Some modules provide direct functions:

```python
# Import function directly
from src.standalone_module import satellite_visibility_time

# Call with parameters
visibility_time = satellite_visibility_time.satellite_visibility_time(
    θ=25,  # Elevation angle
    h=550  # Orbital altitude
)
```

### Pattern 3: Configuration-Based Initialization

Constellation generation uses configuration:

```python
from src.constellation_generation.by_XML import constellation_configuration

# Configuration read from XML file
constellation = constellation_configuration.constellation_configuration(
    dT=5730,
    constellation_name="Starlink"  # Reads config/XML_constellation/Starlink.xml
)
```

## Parameter Units

StarPerf uses consistent units across all APIs:

| Quantity | Unit | Example |
|----------|------|---------|
| Time | seconds | `dT = 1000` |
| Distance | kilometers | `altitude = 550` |
| Angle | degrees | `inclination = 53.0` |
| Bandwidth | Gbps | `isl_capacity = 5.0` |
| Frequency | GHz | `uplink = 2.1` |
| Latitude | degrees | `lat = 47.6` |
| Longitude | degrees | `lon = -122.3` |

## Data Storage Conventions

### HDF5 File Structure

StarPerf uses HDF5 for efficient data storage:

```python
import h5py

# Standard structure:
# constellation.h5
#   ├── position/
#   │   ├── shell1/
#   │   │   ├── timeslot1 (dataset)
#   │   │   └── timeslot2 (dataset)
#   │   └── shell2/
#   └── delay/
#       ├── shell1/
#       └── shell2/
```

### File Paths

```python
# XML constellation data
data_path = f"data/XML_constellation/{constellation_name}.h5"

# TLE constellation data
data_path = f"data/TLE_constellation/{constellation_name}.h5"

# Configuration files
config_path = f"config/XML_constellation/{constellation_name}.xml"
config_path = f"config/TLE_constellation/{constellation_name}/tle.h5"
```

## Error Handling

StarPerf uses standard Python exceptions:

```python
try:
    constellation = constellation_configuration.constellation_configuration(
        dT=5730,
        constellation_name="NonExistent"
    )
except FileNotFoundError as e:
    print(f"Configuration file not found: {e}")
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

## Best Practices

### 1. Use Type Hints

```python
from typing import List, Dict, Optional

def analyze_coverage(
    constellation: Constellation,
    resolution: int = 2
) -> List[float]:
    """Return coverage values for each timeslot."""
    pass
```

### 2. Validate Parameters

```python
def set_resolution(resolution: int) -> None:
    """Set H3 resolution (must be 0-4)."""
    if not 0 <= resolution <= 4:
        raise ValueError(f"Resolution must be 0-4, got {resolution}")
    # ...
```

### 3. Document Units

```python
def calculate_delay(
    distance_km: float,
    speed_of_light_kmps: float = 299792.458
) -> float:
    """
    Calculate propagation delay.

    Args:
        distance_km: Distance in kilometers
        speed_of_light_kmps: Speed of light in km/s

    Returns:
        Delay in seconds
    """
    return distance_km / speed_of_light_kmps
```

### 4. Use Descriptive Names

```python
# Good
satellite_altitude_km = 550
minimum_elevation_angle_deg = 25

# Avoid
h = 550
e = 25
```

## Quick Reference

### Constellation Generation

```python
# XML-based
from src.constellation_generation.by_XML import constellation_configuration
constellation = constellation_configuration.constellation_configuration(dT, constellation_name)

# TLE-based
from src.constellation_generation.by_TLE import constellation_configuration
constellation = constellation_configuration.constellation_configuration(dT, constellation_name)
```

### Connectivity

```python
from src.XML_constellation.constellation_connectivity import connectivity_mode_plugin_manager
manager = connectivity_mode_plugin_manager.connectivity_mode_plugin_manager()
manager.execute_connection_policy(constellation, dT)
```

### Evaluation

```python
from src.XML_constellation.constellation_evaluation import evaluation

# Coverage
coverage = evaluation.coverage(constellation_name, dT, sh, tile_size, minimum_elevation)

# Delay
delay = evaluation.delay(constellation_name, source, target, dT, sh)

# Bandwidth
bandwidth = evaluation.bandwidth(constellation_name, source, target, sh, λ, isl_capacity, dT)
```

## Next Steps

Explore detailed API documentation:
- [Entity Classes](./entities.md) - Core data structures
- [Plugin Interfaces](./plugin-interfaces.md) - Extension points
- [Utility Functions](./utilities.md) - Helper functions

Or see APIs in action:
- [Examples](../examples/overview.md) - Practical usage examples
- [Core Modules](../core-modules/overview.md) - Module documentation
