# Installation

This guide will help you set up StarPerf 2.0 on your system.

## Prerequisites

StarPerf 2.0 requires:
- **Python 3.10** or higher
- Internet connection (for downloading TLE data and dependencies)

### Version Comparison

| Version | Requirements |
|---------|--------------|
| **StarPerf 1.0** | Python 2.7+, MATLAB 2013b+, STK 11+, STK Integration license |
| **StarPerf 2.0** | Python 3.10+ only |

As you can see, StarPerf 2.0 dramatically simplifies the installation process!

## Installation Steps

We recommend using [uv](https://github.com/astral-sh/uv), a fast Python package and project manager, to manage dependencies and virtual environments.

### Step 1: Install uv

Choose the appropriate method for your operating system:

#### MacOS/Linux

```bash
# Method 1: Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Method 2: Using Homebrew (MacOS only)
brew install uv
```

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, refer to the [official uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

### Step 2: Clone the Repository

```bash
git clone https://github.com/SpaceNetLab/StarPerf_Simulator.git
cd StarPerf_Simulator
```

### Step 3: Install Dependencies

Once you have cloned the repository and installed uv, install all required dependencies:

```bash
uv sync
```

This command will:

- Automatically create a virtual environment
- Install all necessary Python libraries
- Set up your development environment

## Required Python Libraries

StarPerf 2.0 depends on the following third-party libraries:

| Library | Version | Purpose |
|---------|---------|---------|
| h3 | 4.0.0b2 | Geospatial indexing |
| h5py | 3.10.0 | HDF5 file handling |
| numpy | 1.24.4 | Numerical computing |
| openpyxl | 3.1.2 | Excel file processing |
| importlib-metadata | 6.8.0 | Package metadata |
| skyfield | 1.46 | Satellite position calculation |
| sgp4 | 2.22 | Orbital propagation |
| pandas | 2.1.0 | Data manipulation |
| poliastro | 0.17.0 | Astrodynamics |
| astropy | 5.3.3 | Astronomy computations |
| networkx | 3.1 | Graph algorithms |
| requests | 2.31.0 | HTTP library |
| jenkspy | 0.4.0 | Natural breaks algorithm |
| pyecharts | 2.0.4 | Visualization |
| global_land_mask | 1.0.0 | Land/ocean detection |

These are automatically installed when running `uv sync`.

## Verify Installation

To verify that StarPerf is installed correctly, run:

```bash
uv run python StarPerf.py
```

If everything is set up correctly, you should see the simulation start smoothly.
