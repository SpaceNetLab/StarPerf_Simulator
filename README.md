# StarPerf: A Network Performance Simulator for Emerging Mega-Constellations

"Newspace" mega-constellations, such as StarLink and OneWeb are gaining tremendous popularity, with the promising potential to provide high-capacity and low-latency communication globally. However, very little is known about the architecture and performance of such emerging systems, the workload they have to face, as well as the impact of topological options on the attainable network performance.

Therefore, we have developed and implemented StarPerf, a mega-constellation performance simulation platform that enables constellation manufacturers and content providers to estimate and understand the achievable performance under a variety of constellation options. The proposed platform integrates four key techniques: (1) **performance simulation for mega-constellation**, which captures the impact of the inherent high mobility in satellite networks and profiles the area-to-area attainable network performance; (2) **constellation scaling**, which synthesizes various topological options by scaling the space resource (e.g. number of satellite, link availability and capacity), and enables exploration on multiple operating conditions that can not be easily reproduced; (3) **constellation visualization**, which leverages Cesium to render mainstream LEO constellations in a highly interactive and realistic 3D environment; (4) **security simulation for LEO satellite networks**, which is based on attack modeling and numerical simulation. We have added traffic plugins and communication energy consumption plugins to StarPerf, and used it to reproduce the link flooding attack proposed in [Time-varying Bottleneck Links in LEO Satellite Networks: Identification, Exploits, and Countermeasures](https://www.ndss-symposium.org/ndss-paper/time-varying-bottleneck-links-in-leo-satellite-networks-identification-exploits-and-countermeasures/)(NDSS 25) and the energy drain attack proposed in [Energy Drain Attack in Satellite Internet Constellations](https://ieeexplore.ieee.org/document/10188709)(IWQoS 23).

This page introduces the basic usage of our StarPerf tool. If you have any questions on StarPerf, please do not hesitate to contact us. (Email: [houyn24@mails.tsinghua.edu.cn](mailto:houyn24@mails.tsinghua.edu.cn), [ZhifengHan.mail@gmail.com](mailto:Zhifenghan.mail@gmail.com), [zeqilai@tsinghua.edu.cn](mailto:zeqilai@tsinghua.edu.cn), [lijh19@mails.tsinghua.edu.cn](mailto:lijh19@mails.tsinghua.edu.cn))

Happy benchmarking your constellation!

# Prerequisites

In the original version of StarPerf, it is mainly built upon Python. In addition, it also leverages third-party orbit analysis/computation tool to help the computation for the trajectory of satellites (e.g. [AGI Systems Tool Kit (STK)](https://www.agi.com/products/stk) or [GMAT](https://opensource.gsfc.nasa.gov/projects/GMAT/index.php) is recommended). The original version of StarPerf uses STK, and its environment requirements are:

- Python2.7 or above.
- Matlab 2013b or above.
- STK version 11 or above.
- STK Integration license, or the [free trial version](https://licensing.agi.com/stk/) with the matlab connector module installed.

Now, we have made a major upgrade to StarPerf, extending its usability and enriching its functionality, and we call it "StarPerf 2.0". Accordingly, the initial version is called "StarPerf 1.0".

Compared with StarPerf 1.0, StarPerf 2.0 is fully implemented in Python and no longer depends on any third-party orbit analysis or computation tools. You only need to ensure that **Python 3.10** or above is installed on your system.

# Installation

We recommend using [uv](https://github.com/astral-sh/uv), a fast Python package and project manager, to manage dependencies and virtual environments for this project.

**(1) Install uv:**

MacOS/Linux:

```bash
# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Alternative for MacOS
brew install uv
```

Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, please refer to [official uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

**(2) Installing Dependencies:**

Once you have cloned the repository, you can install all required dependencies using the following `uv` command:

```bash
cd StarPerf_Simulator/
uv sync
```

This will automatically create a virtual environment and install all necessary libraries.

# StarPerf Overview and Processing Flow

You can directly run our simulation example using the following command:

```bash
uv run python StarPerf.py
```

Of course, you can also write your own simulation scripts. For specific guidelines and important notes, please refer to [interface\_convention](./docs/interface_convention.pdf).

# Constellation Visualization Instructions

We have extended the visualization of mainstream LEO constellations based on Cesium. Below are the detailed usage instructions:

1. Make sure to obtain your personal Cesium Token from the official Cesium website and set it by assigning it to the `Cesium.Ion.defaultAccessToken` parameter in `/StarPerf_Simulator/visualization/html_head_tail/head.html`.

2. Download and install `Node.js` and add it to your system’s environment variables. After that, install `http-server`. Note that it is recommended to use `Node.js` version newer than v13, otherwise you may encounter issues installing `http-server` due to an outdated Node.js version.

3. Uncomment the constellation visualization section in `StarPerf.py` and run this part of the code.

4. Start a local server by running the following command in the terminal. 

```bash
cd ./visualization/CesiumAPP
http-server -p 8081
```

5. Open the constellation visualization webpage by entering `http://127.0.0.1:8081/<filename>` in your browser. Here, `<filename>` refers to the name of the webpage file generated by our visualization code under `/StarPerf_Simulator/visualization/CesiumApp`.

# Contributors Are More Than Welcome

Wanna join the construction of "NewSpace" constellations and networks? Awesome! This project follows the [Github contribution work flow.](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/github-flow) Submissions can fork and use a Github pull request to get merged into this code base.

Ways to help are listed as follows.

### Bug Reports

If you come across a bug in using StarPerf, you are more than welcome to file a bug report to our mail box.

### Contribute More Constellation Designs

As emerging mega-constellations are still evolving rapidly and constellations such as Starlink and OneWeb are still under heavy development, we welcome all who are interested in this research topic to contribute their innovative designs, documents, insights, comments and suggestions.

### Write Test Cases

Currently this project has not been "thoroughly" tested. You are more than welcome to build any test cases for this project.

# License

The StarPerf 1.0 and StarPerf 2.0 projects are under [BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause) license.
