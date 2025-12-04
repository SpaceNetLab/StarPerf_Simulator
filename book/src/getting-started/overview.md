# Overview

StarPerf is a comprehensive platform designed to simulate and analyze the network performance of mega-constellation satellite networks such as Starlink and OneWeb.

## What's New in StarPerf 2.0

StarPerf 2.0 represents a major upgrade from version 1.0 with significant improvements:

### Key Improvements

- **No External Dependencies**: 
    - Fully implemented in Python, no longer requires STK, MATLAB, or other third-party orbit analysis tools
- **Modern Python**:
    - Built on Python 3.10+ with modern libraries
- **Framework + Plugin Architecture**:
    - Highly extensible and modular design allowing easy customization
- **Enhanced Functionality**: 
    - Richer features including traffic plugins, energy consumption simulation, and attack modeling

### Architecture Philosophy

The platform follows a **"framework + plugin"** architecture:

- **Framework**: Provides the core functionality and unified programming interfaces (APIs)
- **Plugins**: Implement specific features (beam placement, routing strategies, damage models, etc.)
- **Decoupled Design**: Plugins and framework are independent, enabling high extensibility

## Constellation Configuration Methods

Pre-configured examples include:

- **Starlink**: SpaceX's mega-constellation
- **OneWeb**: Low-earth orbit communications constellation
- **Telesat**: LEO satellite constellation
- **Boeing**: Custom constellation configurations

StarPerf 2.0 supports two ways to build constellations:

### 1. XML-based Configuration

Build theoretical Walker-δ constellations using XML configuration files. This method is ideal for:

- Exploring constellation design parameters
- Studying hypothetical configurations
- Quick prototyping

### 2. TLE-based Configuration

Build real constellations using Two-Line Element (TLE) data. This method is perfect for:

- Analyzing existing constellations (Starlink, OneWeb, etc.)
- Working with real orbital data
- Comparing simulation with reality

## Core Capabilities

### Performance Simulation

- Area-to-area network performance profiling
- High mobility impact analysis
- Multi-timeslot evaluation

### Constellation Scaling

- Adjust number of satellites
- Modify link availability and capacity
- Explore multiple operating conditions

### Visualization

- 3D interactive constellation rendering using Cesium
- Satellite trajectory visualization
- Ground station coverage display

### Security Simulation

- Attack modeling (link flooding, energy drain, etc.)
- Traffic generation and analysis
- Energy consumption profiling
