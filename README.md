
# StarPerf: A Network Performance Simulator for Emerging Mega-Constellations

``Newspace'' mega-constellations, such as StarLink and OneWeb are gaining tremendous popularity, with the promising potential to provide high-capacity and low-latency communication globally. However, very little is known about the architecture and performance of such emerging systems, the workload they have to face, as well as the impact of topological options on the attainable network performance.

Therefore, we have developed and implemented StarPerf, a mega-constellation performance simulation platform that enables constellation manufacturers and content providers to estimate and understand the achievable performance under a variety of constellation options. The proposed platform integrates two key techniques: (1) performance simulation for mega-constellation, which captures the impact of the inherent high mobility in satellite networks and profiles the area-to-area attainable network performance; (2) constellation scaling, which synthesizes various topological options by scaling the space resource (e.g. number of satellite, link availability and capacity), and enables exploration on multiple operating conditions that can not be easily reproduced. 

This page introduces the basic usage of our StarPerf tool. If you have any questions on StarPerf, please do not hesitate to contact us. (Email: <zeqilai@tsinghua.edu.cn>, <lijh19@mails.tsinghua.edu.cn>)

Happy benchmarking your constellation!

# Prerequisites

StarPerf is built upon Python, AGI Systems Tool Kit (STK) and Matlab. Before running the tool, please make sure you have already installed those dependencies on your machine. 

- Python2.7 or above.
- Matlab 2013b or above.
- STK version 11 or above.
- STK Integration license.

For more details of the setup on STK and matlab, please check [here](https://help.agi.com/stk/11.0.1/Content/install/MATLABsetup.htm). We have tested our tool with Matlab2013b + STK11 installed, on both MacOS and Win10.

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

Second, run the matlab part of StarPerf to build a simulated satellite network based on STK tools. In this step, open the STK tool and Matlab. and run `matlab_code/build_constellation.m`.

This step may take several minutes depending the capability of your machine. Have a break.

Once this step is finished, constellation information like the position (latitude and longitude) of satellites in different time slots, is located in a folder named by your constellation. In this example, these data can be found in `matlab_code/Starlink`. Temporary calculation results are stored in `*.mat` format.

Also, finally in the STK tool you can find the constellation specified by your configuration file. Some thing like this.

![image](https://github.com/SpaceNetLab/StarPerf_Simulator/blob/master/doc/stalink.jpeg)

Finally, run StarPerf to conduct evaluation on the simulated satellite network. This can be done by calling `starperf.py`.

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





