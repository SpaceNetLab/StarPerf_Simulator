# Introduction

StarPerf 2.0 is a feature-rich, highly open, and easily extensible constellation performance simulation platform.

## Architecture Philosophy

The platform architecture follows a:

**"Framework + Plugin"** model

- **Framework**: Implements various underlying functions and provides unified programming interface APIs
- **Plugins**: Implement specific features based on the framework's APIs
- **Decoupled Design**: Plugins and framework are independent, enabling high openness and easy extensibility

## Constellation Building Methods

StarPerf 2.0 supports two methods to build constellations:

### 1. XML Configuration Files
Build **Walker-δ** constellations using XML configuration files. This method is ideal for:
- Designing theoretical constellations
- Exploring different constellation parameters
- Quick prototyping and testing

### 2. TLE Data
Build **real constellations** (like Starlink) using Two-Line Element (TLE) data. This approach allows:
- Analysis of existing mega-constellations
- Working with actual orbital parameters
- Validation against real-world data

## Available Plugins

StarPerf 2.0 comes with various functional plugins out of the box:

| Plugin Category | Examples |
|----------------|----------|
| **Connectivity** | +Grid connectivity mode |
| **Routing** | Shortest Path Routing |
| **Survivability** | Solar Storm Damage Model |
| **Beam Placement** | Random Placement Algorithm |
| **Traffic** | Traffic generation patterns |
| **Attack Simulation** | Link flooding, Energy drain attacks |

## Custom Plugin Development

You can write your own functional plugins based on the interface APIs provided by the framework to achieve personalized functionality. Each plugin category has well-defined specifications:

- Clear interface requirements
- Standardized parameter lists
- Defined return value formats
- Storage conventions for intermediate data

## Document Structure

This documentation is organized to help you understand and use StarPerf 2.0 effectively:

1. **Environment & Dependencies** - Set up your development environment
2. **Architecture** - Understand the system design
3. **Configuration Module** - Learn how to configure constellations
4. **Data Storage** - Understand data organization
5. **Core Modules** - Explore functional capabilities
6. **API Reference** - Detailed interface specifications

## Key Concepts

Before diving deeper, familiarize yourself with these key concepts:

### Constellation
A complete satellite network consisting of one or more shells.

### Shell
A layer in the constellation with satellites at the same orbital altitude and inclination.

### Orbit
A circular path around Earth containing multiple satellites.

### Satellite
Individual spacecraft in the constellation, equipped with antennas and communication capabilities.

### ISL (Inter-Satellite Link)
Communication links between satellites, enabling direct satellite-to-satellite communication.

### Ground Station (GS)
Ground infrastructure that communicates with satellites, serving as entry/exit points for terrestrial networks.

### POP (Point of Presence)
Network access points where satellite traffic connects to terrestrial infrastructure.

### Timeslot
Discrete time intervals at which constellation state is recorded and analyzed.

### H3 Resolution
Hierarchical geospatial indexing system used to divide Earth's surface into hexagonal cells.

## Getting Help

Throughout this documentation, you'll find:
- 📘 **Notes**: Important information to keep in mind
- ⚠️ **Warnings**: Critical considerations
- 💡 **Tips**: Helpful suggestions
- 📝 **Examples**: Code samples and use cases

If you need assistance:
- Review the [API Reference](../api-reference/introduction.md)
- Check [Examples](../examples/overview.md)
- Contact the development team (see [Contact](../about/contact.md))

## Next Steps

Continue reading to understand:
- [Environment & Dependencies](./environment.md) - Required libraries and versions
- [Architecture](./architecture.md) - System organization and modules
- [Configuration Module](./configuration.md) - How to configure constellations
