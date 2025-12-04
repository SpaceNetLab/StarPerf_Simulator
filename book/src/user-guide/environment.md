# Environment & Dependencies

Before we begin, we first introduce the operating environment of StarPerf 2.0 and its dependent libraries so that you can install StarPerf 2.0 correctly.

## Python Version

StarPerf 2.0 is developed based on Python 3.10, so we recommend that your **Python version is 3.10**.

## Third-Party Libraries

In addition to the Python 3.10 standard library, StarPerf 2.0 uses the following open source Python third-party libraries:

**Table 1: Third-party Python libraries and versions**

|      Library       | Version |
| :----------------: |:-------:|
|         h3         | 4.0.0b2 |
|        h5py        | 3.10.0  |
|       numpy        | 1.24.4  |
|      openpyxl      |  3.1.2  |
| importlib-metadata |  6.8.0  |
|      skyfield      |  1.46   |
|        sgp4        |  2.22   |
|       pandas       |  2.1.0  |
|     poliastro      | 0.17.0  |
|      astropy       |  5.3.3  |
|      networkx      |   3.1   |
|      requests      | 2.31.0  |
|      jenkspy       |  0.4.0  |
|     pyecharts      |  2.0.4  |
| global_land_mask   |  1.0.0  |

## Installation

The third-party Python libraries in the above table and their corresponding version numbers are all listed in `docs/third-party_libraries_list.txt` in the form of `LibraryName==LibraryVersion` (such as `numpy==1.24.4`).

You can execute the following command in the root directory of the StarPerf 2.0 project to install all third-party Python libraries at once:

```bash
pip install -r docs/third-party_libraries_list.txt
```

## System Dependencies

Finally, StarPerf 2.0 does not depend on any non-Python environment, so you do not need to install any third-party orbit analysis/calculation tools (STK, etc.).

---

**Navigation:**
- [Previous: Introduction](introduction.md)
- [Next: Architecture](architecture.md)
