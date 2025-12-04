# Data Storage Module: data/

This module stores various data when StarPerf 2.0 is running, which can be divided into three categories:

## Preloaded Data

The data that StarPerf 2.0 must read when running certain functions, such as the data of Uber h3 library cells, which is located in `data/h3_cells_id_res0-4.h5`.

## Intermediate Data

StarPerf 2.0 needs to temporarily store some data when running certain functions, such as:
- The delay matrix of the constellation
- Satellite position data
- Other temporary computation results

These data are stored in:
- `data/TLE_constellation/<constellation_name>.h5` (such as `data/TLE_constellation/Starlink.h5`)
- `data/XML_constellation/<constellation_name>.h5` (such as `data/XML_constellation/Starlink.h5`)

## Result Data

The final results produced after StarPerf 2.0 runs, such as:
- Output drawings in PDF format
- Analysis reports
- Performance metrics
- Other simulation results

---

**Navigation:**
- [Previous: Configuration](configuration.md)
- [Next: Auxiliary Scripts](auxiliary-scripts.md)
