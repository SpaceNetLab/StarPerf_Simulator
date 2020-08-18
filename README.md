
# StarPerf: A Network Performance Simulator for Emerging Mega-Constellations

``Newspace'' mega-constellations, such as StarLink and OneWeb are gaining tremendous popularity, with the promising potential to provide high-capacity and low-latency communication globally. However, very little is known about the architecture and performance of such emerging systems, the workload they have to face, as well as the impact of topological options on the attainable network performance.

Therefore, we have developed and implemented StarPerf, a mega-constellation performance simulation platform that enables constellation manufacturers and content providers to estimate and understand the achievable performance under a variety of constellation options. The proposed platform integrates two key techniques: (1) performance simulation for mega-constellation, which captures the impact of the inherent high mobility in satellite networks and profiles the area-to-area attainable network performance; (2) constellation scaling, which synthesizes various topological options by scaling the space resource (e.g. number of satellite, link availability and capacity), and enables exploration on multiple operating conditions that can not be easily reproduced. 

This page introduces the basic usage of our StarPerf tool. If you have any questions on StarPerf, please do not hesitate to contact us. (Email: <zeqilai@tsinghua.edu.cn>, <lijh19@mails.tsinghua.edu.cn>)

Happy benchmarking your constellation!

# Prerequisites

StarPerf is mainly built upon Python. In addition, StarPerf also leverages third-party orbit analysis/computation tool to help the computation for the trajectory of satellites (e.g. [AGI Systems Tool Kit (STK)](https://www.agi.com/products/stk) or [GMAT](https://opensource.gsfc.nasa.gov/projects/GMAT/index.php) is recommended). The current implementation uses STK. Before running the tool, please make sure you have already installed those dependencies on your machine. 

- Python2.7 or above.
- Matlab 2013b or above.
- STK version 11 or above.
- STK Integration license, or the [free trial version](https://licensing.agi.com/stk/) with the matlab connector module installed.

For more details of the setup on STK and matlab, please check [here](https://help.agi.com/stk/11.0.1/Content/install/MATLABsetup.htm). We have tested our tool with Python3 + Matlab2013b + STK11 installed, on Windows 10.

# StarPerf overview and processing flow

![image](https://github.com/SpaceNetLab/StarPerf_Simulator/blob/master/doc/process_flow.jpeg)

Summarily, the implementation of StarPerf integrates two parts: (i) generating a satellite network topology by the specific constellation configuration (e.g., how many satellites and how many orbits ...); (ii) evaluating the network performance of the generated satellite network.

The first step is done by codes in `matlab_code/*.m`, which are based on third-party orbit computation tools (e.g. STK). The constellation configuration files are located in `etc/` folder.
`parameter.xlsx` that describes the orbital design will be loaded to construct a simulated network.

For your convenience, we have prepared several configuration preset for three state-of-the-art constellations in `etc/`. You can use the preset by rename the file, e.g. remove the suffix of `parameter-StarLink.xlsx`. 

Once step 1 finished, temporary files describing the satellite network will be generated at `matlab_code/YOUR_CONSTELLATION_NAME`.

In addition, since generating the network topology may take too much time on some machines, we also prepare the pre-computed file for Starlink, OneWeb and TeleSat constellation respectively by a [Dropbox shared link.](https://www.dropbox.com/sh/ncxf84a1m9uznm2/AABwrzHdKX6ZXsEb6FV6L3foa?dl=0) For simplicity, you can just download these files and skip the topology generation step by placing the uncompressed files in the `matlab_code/` folder.

The second step, is executed by the python codes in the root folder. This step evaluate the network performance (e.g. latency, throughput ...) of the generated network.

# Configuring your constellations

Leveraging StarPerf to construct a satellite network over a specific constellation design follows the following steps. Here we show an example of using StarPerf to simulate and benchmark Starlink.

First, modify the constellation design options, including parameters such as the number of orbit, number of satellites. The configuration file is located at:

``` matlab_code/parameter.xlsx```

The configuration file looks like this:


| Parameter   | Value  |
| :----  | :----  |
| Name         | Starlink|
| Inclination  | 53°     |
| Altitude     | 550km |
| # of orbit   | 24 |
| satellites per orbit  | 66 |

Second, run the matlab part of StarPerf to build a simulated satellite network based on STK tools. In this step, open the STK tool and Matlab. and run `matlab_code/build_constellation.m`. This step has to run on Windows, as the current version of STK works on Windows only.

This step may take several minutes depending the capability of your machine. Have a break.

Once this step is finished, constellation information like the position (latitude and longitude) of satellites in different time slots, is located in a folder named by your constellation. In this example, these data can be found in `matlab_code/Starlink`. Temporary calculation results are stored in `*.mat` format.

Also, finally in the STK tool you can find the constellation specified by your configuration file. Some thing like this.

![image](https://github.com/SpaceNetLab/StarPerf_Simulator/blob/master/doc/stalink.jpeg)

Finally, run StarPerf to conduct evaluation on the simulated satellite network. This step can be done by calling `starperf.py`. 

```python starperf.py```

Results like coverage, latency can be obtained in `*.csv` format once the calculation is done.




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

The StarPerf project is under [BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause) license.





