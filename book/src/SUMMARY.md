# Summary

[Introduction](./README.md)

# Getting Started

- [Overview](./getting-started/overview.md)
- [Installation](./getting-started/installation.md)
- [Quick Start](./getting-started/quick-start.md)

# User Guide

- [Introduction](./user-guide/introduction.md)
- [Environment & Dependencies](./user-guide/environment.md)
- [Architecture](./user-guide/architecture.md)
- [Configuration Module](./user-guide/configuration.md)
  - [H5 File Format](./user-guide/config/h5-format.md)
  - [TLE Constellation](./user-guide/config/tle-constellation.md)
  - [XML Constellation](./user-guide/config/xml-constellation.md)
  - [Ground Stations](./user-guide/config/ground-stations.md)
  - [POPs](./user-guide/config/pops.md)
- [Data Storage Module](./user-guide/data-storage.md)
- [Auxiliary Scripts](./user-guide/auxiliary-scripts.md)

# Core Modules

- [Kernel Module Overview](./core-modules/overview.md)

## Constellation Generation

- [Overview](./core-modules/constellation-generation/overview.md)
- [XML-based Generation](./core-modules/constellation-generation/xml-based.md)
  - [constellation_configuration.py](./core-modules/constellation-generation/xml-constellation-config.md)
  - [orbit_configuration.py](./core-modules/constellation-generation/xml-orbit-config.md)
  - [Case Study](./core-modules/constellation-generation/xml-case-study.md)
- [TLE-based Generation](./core-modules/constellation-generation/tle-based.md)
  - [download_TLE_data.py](./core-modules/constellation-generation/tle-download.md)
  - [satellite_to_shell_mapping.py](./core-modules/constellation-generation/tle-shell-mapping.md)
  - [satellite_to_orbit_mapping.py](./core-modules/constellation-generation/tle-orbit-mapping.md)
  - [get_satellite_position.py](./core-modules/constellation-generation/tle-position.md)
  - [constellation_configuration.py](./core-modules/constellation-generation/tle-constellation-config.md)
  - [Case Study](./core-modules/constellation-generation/tle-case-study.md)
- [Duration-based Generation](./core-modules/constellation-generation/duration-based.md)

## Standalone Modules

- [Satellite Visibility Time](./core-modules/standalone-modules/satellite-visibility.md)

## Beam Placement

- [Overview](./core-modules/beam-placement/overview.md)
- [Plugin Specification](./core-modules/beam-placement/plugins.md)
- [Framework](./core-modules/beam-placement/framework.md)
- [Case Study](./core-modules/beam-placement/case-study.md)

## Connectivity

- [Overview](./core-modules/connectivity/overview.md)
- [Plugin Specification](./core-modules/connectivity/plugins.md)
- [Framework](./core-modules/connectivity/framework.md)
- [Case Study](./core-modules/connectivity/case-study.md)

## Performance Evaluation

- [Overview](./core-modules/evaluation/overview.md)
- [With ISL](./core-modules/evaluation/with-isl.md)
  - [Bandwidth](./core-modules/evaluation/isl-bandwidth.md)
  - [Betweenness](./core-modules/evaluation/isl-betweenness.md)
  - [Coverage](./core-modules/evaluation/isl-coverage.md)
  - [Delay](./core-modules/evaluation/isl-delay.md)
- [Without ISL (Bent-pipe)](./core-modules/evaluation/without-isl.md)
  - [Bandwidth](./core-modules/evaluation/bentpipe-bandwidth.md)
  - [Coverage](./core-modules/evaluation/bentpipe-coverage.md)
  - [Delay](./core-modules/evaluation/bentpipe-delay.md)

## Entity Classes

- [Overview](./core-modules/entity/overview.md)

## Routing

- [Overview](./core-modules/routing/overview.md)
- [Plugin Specification](./core-modules/routing/plugins.md)
- [Framework](./core-modules/routing/framework.md)

## High Survivability

- [Overview](./core-modules/survivability/overview.md)
- [Plugin Specification](./core-modules/survivability/plugins.md)
- [Framework](./core-modules/survivability/framework.md)

# Visualization

- [Constellation Visualization](./visualization/constellation.md)
- [Setup Instructions](./visualization/setup.md)

# Examples

- [Overview](./examples/overview.md)
- [XML Constellation Example](./examples/xml-constellation.md)
- [TLE Constellation Example](./examples/tle-constellation.md)
- [Beam Placement Example](./examples/beam-placement.md)
- [Connectivity Example](./examples/connectivity.md)
- [Performance Evaluation Example](./examples/evaluation.md)

# API Reference

- [Introduction](./api-reference/introduction.md)
- [Plugin Interfaces](./api-reference/plugin-interfaces.md)
- [Entity Classes](./api-reference/entities.md)
- [Utility Functions](./api-reference/utilities.md)

# Contributing

- [How to Contribute](./contributing/how-to-contribute.md)
- [Writing Plugins](./contributing/writing-plugins.md)
- [Code Style Guide](./contributing/code-style.md)

# About

- [License](./about/license.md)
- [Contact](./about/contact.md)
- [Contributors](./about/contributors.md)
