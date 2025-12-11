# Constellation Generation

This module is used to generate and initialize satellite constellations. StarPerf 2.0 supports multiple ways of generating constellations:

1. **XML-based Generation**: Use XML documents to build Walker-δ or polar constellations
2. **TLE-based Generation**: Use TLE (Two-Line Element) data to build real constellations
3. **Duration-based Generation**: Build constellations with specified simulation duration and sampling interval

## Overview

The constellation generation module is part of the framework that implements constellation generation and constellation initialization. It provides the foundational capabilities for creating satellite network topologies that can be used with various evaluation and simulation modules.

## Generation Methods

### XML-based Constellation Generation

This method uses XML configuration files to define constellation parameters such as:
- Orbital altitude and inclination
- Number of orbits and satellites per orbit
- Phase shift parameters
- Shell configurations

See [XML-based Generation](xml-based.md) for detailed information.

### TLE-based Constellation Generation

This method uses real satellite data from TLE files to build constellations based on actual satellite positions. The process includes:
- Downloading TLE data from sources like CelesTrak
- Mapping satellites to shells based on launch information
- Determining satellite-to-orbit relationships
- Calculating satellite positions over time

See [TLE-based Generation](tle-based.md) for detailed information.

### Duration-based Constellation Generation

This method builds constellations with both simulation duration and sampling interval specified simultaneously. It's based on XML configuration but allows for custom simulation timeframes rather than being limited to orbital periods.

See [Duration-based Generation](duration-based.md) for detailed information.

## Common Output

All generation methods produce:
- A constellation object with shell, orbit, and satellite information
- Position data for each satellite at each timestamp
- Data stored in HDF5 (.h5) format under the `data/` directory

## Navigation

- [Back to Core Modules Overview](../overview.md)
- [XML-based Generation](xml-based.md)
- [TLE-based Generation](tle-based.md)
- [Duration-based Generation](duration-based.md)
