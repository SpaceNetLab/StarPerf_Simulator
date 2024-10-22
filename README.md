# StarPerf: A Network Performance Simulator for Emerging Mega-Constellations

"Newspace" mega-constellations, such as StarLink and OneWeb are gaining tremendous popularity, with the promising potential to provide high-capacity and low-latency communication globally. However, very little is known about the architecture and performance of such emerging systems, the workload they have to face, as well as the impact of topological options on the attainable network performance.

Therefore, we have developed and implemented StarPerf, a mega-constellation performance simulation platform that enables constellation manufacturers and content providers to estimate and understand the achievable performance under a variety of constellation options. The proposed platform integrates two key techniques: (1) performance simulation for mega-constellation, which captures the impact of the inherent high mobility in satellite networks and profiles the area-to-area attainable network performance; (2) constellation scaling, which synthesizes various topological options by scaling the space resource (e.g. number of satellite, link availability and capacity), and enables exploration on multiple operating conditions that can not be easily reproduced.

This page introduces the basic usage of our StarPerf tool. If you have any questions on StarPerf, please do not hesitate to contact us. (Email: [houyn24@mails.tsinghua.edu.cn](mailto:houyn24@mails.tsinghua.edu.cn), [zeqilai@tsinghua.edu.cn](mailto:zeqilai@tsinghua.edu.cn), [lijh19@mails.tsinghua.edu.cn](mailto:lijh19@mails.tsinghua.edu.cn))

Happy benchmarking your constellation!

# Prerequisites

In the original version of StarPerf, it is mainly built upon Python. In addition, it also leverages third-party orbit analysis/computation tool to help the computation for the trajectory of satellites (e.g. [AGI Systems Tool Kit (STK)](https://www.agi.com/products/stk) or [GMAT](https://opensource.gsfc.nasa.gov/projects/GMAT/index.php) is recommended). The original version of StarPerf uses STK, and its environment requirements are:

- Python2.7 or above.
- Matlab 2013b or above.
- STK version 11 or above.
- STK Integration license, or the [free trial version](https://licensing.agi.com/stk/) with the matlab connector module installed.

Now, we have made a major upgrade to StarPerf, extending its usability and enriching its functionality, and we call it "StarPerf 2.0". Accordingly, the initial version is called "StarPerf 1.0".

Compared with StarPerf 1.0, StarPerf 2.0 is completely based on Python and does not require any third-party orbit analysis/computation tools. Therefore, just make sure you have a Python3.10 or above environment installed on your computer and the following Python libraries installed to ensure the system is running properly:

- h3==4.0.0b2
- h5py==3.10.0
- numpy==1.24.4
- openpyxl==3.1.2
- importlib-metadata==6.8.0
- skyfield==1.46
- sgp4==2.22
- pandas==2.1.0
- poliastro==0.17.0
- astropy==5.3.3
- networkx==3.1
- requests==2.31.0
- jenkspy==0.4.0
- pyecharts==2.0.4

# StarPerf overview and processing flow

see [interface\_convention](./docs/interface_convention.pdf).

# Contributors are more than welcome

Wanna to join the construction of "NewSpace" constellations and networks? Awesome! This project follows the [Github contribution work flow.](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/github-flow) Submissions can fork and use a Github pull request to get merged into this code base.

Ways to help are listed as follows.

### Bug reports

If you come across a bug in using StarPerf, you are more than welcome to file a bug report to our mail box.

### Contribute more constellation designs

As emerging mega-constellations are still evolving rapidly and constellations such as Starlink and OneWeb are still under heavy development, we welcome all who are interested in this research topic to contribute their innovative designs, documents, insights, comments and suggestions.

### Write test cases

Currently this project has not be ''thoroughly''' tested. You are more than welcome to build any test cases for this project.

# License

The StarPerf 1.0 and StarPerf 2.0 projects are under [BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause) license.
