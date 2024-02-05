'''

Author : yunanhou

Date : 2023/08/24

Function : This file defines the inter-satellite link class ISL, which is the base class for all ISLs in this project.
           ISL is responsible for connecting two satellites and has no directionality, so there is no need to
           distinguish between source and destination satellites.

'''


class ISL:
    def __init__(self , satellite1 , satellite2 , data_rate=5, frequency_band =5, capacity =5):
        self.satellite1 = satellite1.id # the id of the first satellite, int type
        self.satellite2 = satellite2.id # the id of the second satellite, int type
        # the distance between the two satellites connected by ISL, the unit is kilometers km. This parameter is of
        # list type because it needs to store the distances of different timeslots.
        self.distance = []
        # the delay between the two satellites connected by ISL, in seconds, this parameter is of list type because it
        # needs to store the delay time of different timeslots.
        self.delay = []
        # data transfer rate (Gbps)
        self.data_rate = data_rate
        # laser band
        self.frequency_band = frequency_band
        # the capacity of ISL
        self.capacity = capacity
