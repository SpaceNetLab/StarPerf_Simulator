# StarPerf: A Network Performance Simulator for Emerging Mega-Constellations

"Newspace" mega-constellations, such as StarLink and OneWeb are gaining tremendous popularity, with the promising potential to provide high-capacity and low-latency communication globally. However, very little is known about the architecture and performance of such emerging systems, the workload they have to face, as well as the impact of topological options on the attainable network performance.

Therefore, we have developed and implemented StarPerf, a mega-constellation performance simulation platform that enables constellation manufacturers and content providers to estimate and understand the achievable performance under a variety of constellation options. The proposed platform integrates two key techniques: (1) performance simulation for mega-constellation, which captures the impact of the inherent high mobility in satellite networks and profiles the area-to-area attainable network performance; (2) constellation scaling, which synthesizes various topological options by scaling the space resource (e.g. number of satellite, link availability and capacity), and enables exploration on multiple operating conditions that can not be easily reproduced.

This page introduces the basic usage of our StarPerf tool. If you have any questions on StarPerf, please do not hesitate to contact us. (Email: [zeqilai@tsinghua.edu.cn](mailto:zeqilai@tsinghua.edu.cn), [lijh19@mails.tsinghua.edu.cn](mailto:lijh19@mails.tsinghua.edu.cn), [yunanhou2023@gmail.com](mailto:yunanhou2023@gmail.com))

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

Same as StarPerf 1.0, the implementation of StarPerf 2.0 integrates two parts: (i) generating a satellite network topology by the specific constellation configuration (e.g., how many satellites and how many orbits ...); (ii) evaluating the network performance of the generated satellite network. Based on the existing evaluation in StarPerf 1.0, we have given more evaluation functions in StarPerf 2.0, which can more comprehensively evaluate the satellite network.

The first step is done through the code in "src/constellation_configuration/constellation_configuration.py", which generates a satellite network by reading the constellation information configuration file "config/constellation_configuration/<CONSTELLATION_NAME.xml>". Different from StarPerf 1.0, in StarPerf 2.0, all constellation configuration-related information is located in "config/", and all the above operations are completed independently by Python.

For your convenience, we have prepared a configuration preset for the state-of-the-art constellation StarLink in "config/constellation_configuration/StarLink.xml".

After step 1 is completed, temporary files describing the satellite network will be generated in the "data/" folder. The format of these temporary files is "<CONSTELLATION_NAME>.h5", which stores the delay matrix and satellite position information between satellites. Regarding how specific constellation data information is stored in the h5 file, please view "docs/interface_convention.md".

The second step, is executed by the python codes in the "src/" folder. This step not only allows to evaluate the network performance of the generated network (e.g. latency, throughput, coverage...), but also simulates advanced features such as constellation routing paths, constellation damage, beam placement, etc. More details can be found in "[docs/interface\_convention.md](./interface_convention.md)".

# Configuring your constellations

Leveraging StarPerf 2.0 to construct a satellite network over a specific constellation design follows the following steps. Here we show an example of using StarPerf 2.0 to simulate and benchmark Starlink.

First, read the StarLink configuration information file "config/constellation_configuration/StarLink.xml". The file information structure is as follows:

```xml
<constellation>
    <number_of_shells>4</number_of_shells>
    <shell1>
        <altitude>550</altitude>
        <orbit_cycle>5731</orbit_cycle>
        <inclination>53.0</inclination>
        <phase_shift>1</phase_shift>
        <number_of_orbit>72</number_of_orbit>
        <number_of_satellite_per_orbit>22</number_of_satellite_per_orbit>
    </shell1>
    <shell2>
        <altitude>570</altitude>
        <orbit_cycle>5755</orbit_cycle>
        <inclination>70</inclination>
        <phase_shift>1</phase_shift>
        <number_of_orbit>36</number_of_orbit>
        <number_of_satellite_per_orbit>20</number_of_satellite_per_orbit>
    </shell2>
    <shell3>
        <altitude>560</altitude>
        <orbit_cycle>5743</orbit_cycle>
        <inclination>97.6</inclination>
        <phase_shift>1</phase_shift>
        <number_of_orbit>10</number_of_orbit>
        <number_of_satellite_per_orbit>52</number_of_satellite_per_orbit>
    </shell3>
    <shell4>
        <altitude>540</altitude>
        <orbit_cycle>5718</orbit_cycle>
        <inclination>53.2</inclination>
        <phase_shift>1</phase_shift>
        <number_of_orbit>72</number_of_orbit>
        <number_of_satellite_per_orbit>22</number_of_satellite_per_orbit>
    </shell4>
</constellation>
```

Second, run the scripts in the "src/constellation_configuration" folder to build a simulated satellite network. In StarPerf 1.0, this step may take several minutes depending the capability of your machine. But in StarPerf 2.0, this step is completely based on Python and does not rely on any third-party tools such as MATLAB and STK, so this step will be completed quickly.

Once this step is finished, constellation information (like the position (latitude and longitude) of satellites in different time slots, constellation delay time matrix) will be located in the "data/" directory in a file with the suffix ".h5" named after your constellation. In this example, these data can be found in "data/StarLink.h5".

Finally, run StarPerf to conduct evaluation on the simulated satellite network. This step can be done by calling "StarPerf.py". "StarPerf.py" is the startup script of StarPerf 2.0, which is used to execute the test cases of each module. Among them, the test cases of each module are located in the "samples/" folder.

For information on the implementation principles of Starperf 2.0 and various interface specifications, please refer to "[docs/interface\_convention.md](docs/interface_convention.md)".

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
