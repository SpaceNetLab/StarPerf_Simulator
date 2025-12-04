# Constellation Evaluation

Constellation performance evaluation is generally divided into two categories: with ISL and without ISL. The former is used in +Grid and other modes and includes four evaluation indicators: bandwidth, betweenness, coverage and delay. The latter is used in bent-pipe mode and includes three evaluation indicators: bandwidth, coverage and delay.

## Overview

The evaluation module provides comprehensive performance metrics for satellite constellations. Different metrics are available depending on whether the constellation operates with Inter-Satellite Links (ISLs) or in bent-pipe mode.

## Evaluation Modes

### Performance Evaluation with ISL

In this section, we take the +Grid connection mode as an example to evaluate the constellation performance.

#### Bandwidth

First, given a shell in a constellation, as well as two ground station objects source and destination, pass in a parameter λ, and then calculate the bandwidth between the source and destination. The calculation of the bandwidth value refers to the total bandwidth of all disjoint paths from the source to the destination whose delay time does not exceed λ times the shortest delay time. λ is a floating point number not less than 1 (that is, the minimum value of λ is 1).

**Table: bandwidth function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| constellation_name | str | - | the name of the constellation, such as "Starlink" |
| source | user | - | the source of the communication pair |
| target | user | - | the destination of the communication pair |
| sh | shell | - | a shell in the constellation |
| λ | float | - | the maximum multiple of the minimum delay time allowed from source to target. The smaller the λ value, the fewer the number of paths from source to target. When λ=1, only one path meets the requirements (i.e. the shortest path). |
| isl_capacity | float | Gbps | the capacity of a single ISL, such as 5Gbps |
| dT | int | second | how often a timeslot is recorded |

Calculate the bandwidth between source and target in each timeslot, and finally average it to be the final bandwidth between source and target, and return this final calculation result.

#### Betweenness

Betweenness is a metric that describes the centrality in a graph based on shortest paths, and it is widely used in telecommunications networks, e.g., a node with higher betweenness centrality would have more traffic passing through that node. Moreover, a node with a high betweenness centrality may also be a potential bottleneck node, since the failure of this node will affect all flows relying on it. In this function we will evaluate the betweenness of each satellite in the constellation.

Specifically, the betweenness of a satellite sat is calculated as:

$$
betweenness(sat) = \sum_{s \ne d \ne sat} \frac{p_{sd}(sat)}{p_{sd}}
$$

where $p_{sd}$ is the total number of the shortest paths from source $s$ to destination $d$, and $p_{sd}(sat)$ is the number of those paths that pass through $sat$.

**Table: betweenness function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :----------------: | :------------: | :------------: | :-----------------------------------------------: |
| constellation_name | str | - | the name of the constellation, such as "Starlink" |
| sh | shell | - | a shell in the constellation |
| t | int | - | a certain time slot (timeslot) |

After the calculation is completed, a list will eventually be returned. Each element in the list is of type float, representing the betweenness of each satellite.

#### Coverage

Calculation method: Divide the longitude of the earth's surface every $\alpha$ and the latitude every $\alpha$, thus obtaining $\frac{180}{\alpha} \times \frac{360}{\alpha}$ fragments. Each fragment represents a certain area of the earth's surface. The default value of α is 10°.

**Table: coverage function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| constellation_name | str | - | the name of the constellation, such as "Starlink" |
| dT | int | second | how often a timeslot is recorded |
| sh | shell | - | a shell in the constellation |
| tile_size(α) | float | degree | the size of the square block on the earth's surface, the default is to cut every 10°, that is, each block occupies 10° longitude and 10° latitude. |
| maximum_depression | float | degree | the maximum depression angle of the satellite, the default value is 56.5° |
| minimum_elevation | float | degree | the minimum elevation angle of the ground observation point, the default value is 25° |

This function calculates the coverage of each timeslot, and finally stores the coverage of each timeslot into a list variable and returns it.

#### Delay

This function is used to calculate the delay time of two communication endpoints, that is, the total time of sending a packet from the source to the destination, and the total time of sending a packet from the destination to the source (RTT time).

**Table: delay function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :----------------: | :------------: | :------------: | :-----------------------------------------------: |
| constellation_name | str | - | the name of the constellation, such as "Starlink" |
| source | user | - | source endpoint of the communication pair |
| target | user | - | destination endpoint of the communication pair |
| dT | int | second | how often a timeslot is recorded |
| sh | shell | - | a shell in the constellation |

This function calculates the delay time of each timeslot, and finally stores the delay time of each timeslot into a list variable and returns it.

### Performance Evaluation without ISL

In this section, we evaluate the performance of constellations without ISL, i.e. the performance of constellations in bent-pipe operating mode.

#### Bandwidth

Calculation method: When the bent-pipe mode communicates between two ends (denoted as end A and end B), end A selects a satellite in the sky as a relay (denoted as satellite 1) according to a certain strategy, and end B selects a satellite in the sky as a relay according to a certain strategy (denoted as satellite 2). Assume that there are $n$ GSs within the visible range of satellite 1, and the bandwidth of each GS is $P$; there are $m$ GSs within the visible range of satellite 2, and the bandwidth of each GS is $P$. Therefore, the bandwidth of satellite 1 → satellite 2 can be expressed as $n \times P$, and the bandwidth of satellite 2 → satellite 1 can be expressed as $m \times P$. Since the communication is bidirectional, the communication bandwidth between A and B is $\min\{n \times P, m \times P\}$. The above calculation is performed for each timeslot within the satellite orbit period. Finally, the average of all timeslot values can be used as the bent-pipe bandwidth for communication between A and B.

**Table: bandwidth function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :-----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| source | user | - | the source of the communication pair |
| target | user | - | the destination of the communication pair |
| dT | int | second | how often a timeslot is recorded |
| sh | shell | - | a shell in the constellation |
| ground_station_file | str | - | constellation ground station file path (the path is calculated from the root directory of the project) |
| minimum_elevation | float | degree | the minimum elevation angle of the ground users |
| GS_capacity | float | Gbps | the GS capacity of each ground station, such as 10 Gbps |

Calculate the bandwidth between source and target in each timeslot, and finally average it to be the final bandwidth between source and target, and return this final calculation result.

#### Coverage

Calculation method: In bent-pipe mode, the coverage of the constellation is not only related to the satellite itself, but also to the GS. If a user is in an area where a satellite can be seen overhead, but there is no GS within the visible range of the satellite, then the area where the user is located is said to be not covered by bent-pipe.

Specifically, the coverage rate in bent-pipe mode can be calculated as follows: First, divide the earth's surface into several tiles, for example, every 10° interval according to the longitude and latitude, so that you will get 18×36 tiles. Then select a point (latitude and longitude) in each tile as the user's position, take the user as the perspective, calculate all satellites visible to the user (note the set of these satellites as S), traverse all satellites in the S set, as long as at least one satellite in the S set has a GS in its visible field of view, the tile is considered to be covered. Perform this operation on all tiles, and finally divide the number of covered tiles by the total number of tiles, which is the coverage rate of the constellation under the current timeslot. Perform the above operation on all timeslots to obtain the constellation coverage under each timeslot, and finally average the value and return it as the final constellation coverage.

**Table: coverage function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :-----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| dT | int | second | how often a timeslot is recorded |
| sh | shell | - | a shell in the constellation |
| ground_station_file | str | - | constellation ground station file path (the path is calculated from the root directory of the project) |
| minimum_elevation | float | degree | the minimum elevation angle of the ground users |
| tile_size | float | degree | the size of the square block on the earth's surface, the default is to cut every 10°, that is, each block occupies 10° longitude and 10° latitude. |

This function calculates the coverage of each timeslot, and finally stores the coverage of each timeslot into a list variable and returns it.

#### Delay

Calculation method: When the bent-pipe mode communicates between two terminals (denoted as terminal A and terminal B), the process is: terminal A → satellite 1 → ground station A → POP point 1 → terminal B, or terminal B → Satellite 2 → Ground station B → POP point 2 → Terminal A. Therefore, if you want to calculate the delay between terminal A and terminal B in bent-pipe mode, you can calculate the delay between terminal A → satellite 1 → ground station A → POP point 1 → POP point 2 → ground station B → satellite 2 → terminal B → satellite 2 → ground station B → POP point 2 → POP point 1 → ground station A → satellite 1 → terminal A, use this delay time to represent the bent-pipe delay between terminal A and terminal B. Among them, when calculating the delay between POP point 1 → POP point 2 or POP point 2 → POP point 1, it is expressed by dividing the great circle distance on the earth's surface by a certain speed.

**Table: delay function attributes list**

| Parameter Name | Parameter Type | Parameter Unit | Parameter Meaning |
| :-----------------: | :------------: | :------------: | :----------------------------------------------------------: |
| source | user | - | the source of the communication pair |
| target | user | - | the destination of the communication pair |
| dT | int | second | how often a timeslot is recorded |
| sh | shell | - | a shell in the constellation |
| ground_station_file | str | - | constellation ground station file path (the path is calculated from the root directory of the project) |
| POP_file | str | - | satellite constellation ground POP point data file |
| α | float | - | the great circle distance coefficient between the source and target points |
| β | float | - | the communication speed between source and target. The speed of light in vacuum is c, but the speed of communication between source and target may not be c. Therefore, the speed of light c multiplied by the speed coefficient β represents the final communication speed from source to target. |
| minimum_elevation | float | degree | the minimum elevation angle of the ground users |

This function calculates the delay time of each timeslot, and finally stores the delay time of each timeslot into a list variable and returns it.

## Use Cases

The evaluation module is essential for:

1. **Performance Comparison**: Comparing different constellation designs or configurations
2. **Bottleneck Identification**: Finding potential performance bottlenecks using betweenness
3. **Coverage Analysis**: Ensuring adequate service coverage for target regions
4. **Quality of Service**: Validating delay and bandwidth requirements are met
5. **Design Optimization**: Iterating on constellation parameters to improve metrics

## Integration with Other Modules

The evaluation module works in conjunction with:

- **Connectivity Module**: Requires established ISL topology for ISL-based metrics
- **Beam Placement Module**: Affects coverage calculations
- **Routing Module**: Influences delay and bandwidth calculations
- **Traffic Module**: Provides realistic load for capacity analysis

## Navigation

- [Back to Core Modules Overview](../overview.md)
- [Previous: Connectivity](../connectivity/overview.md)
- [Beam Placement](../beam-placement/overview.md)
