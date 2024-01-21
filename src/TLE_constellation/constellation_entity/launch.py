'''

Author : yunanhou

Date : 2023/11/30

Function : This file defines the launch class, which is used to describe satellite-related information in a rocket
           launch, including three attributes: cospar_id, Altitude and Inclination.

           cospar_id is International Designator, is an international identifier assigned to artificial objects in
           space. For example, "2019-074" means the 74th launch mission in 2019. Multiple satellites may be included
           in a single launch. The identifier of each satellite is to add uppercase English letters after cospar_id,
           such as "2019-074C", "2022-136H", etc.

           The two attributes altitude and inclination respectively represent the orbital altitude and orbital
           inclination of the satellite to be launched.

'''


class launch:
    def __init__(self, cospar_id , altitude , inclination):
        self.cospar_id = cospar_id # str
        self.altitude = altitude # float
        self.inclination = inclination # float