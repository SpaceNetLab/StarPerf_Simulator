'''

Author : yunanhou

Date : 2023/12/03

Function : Analog constellation ring connection mode


Ring connection: Only intra-track ISL is established, and there is no inter-track ISL. When two communicating
                 parties communicate, the source first sends data to a satellite in an orbit (marked as orbit1),
                 and then the data is transmitted between ISLs in orbit1. When the data can be seen on at least
                 one ground station on the satellite in orbit1, the satellite sends the data to the ground station
                 (denoted as GS1), and GS1 then accesses the ground network through a POP point (denoted as POP1).
                 The destination will also go through such a process when sending data to the source. There will
                 also be an orbit (denoted as orbit2), a ground station (denoted as GS2) and a POP point (denoted
                 as POP2). Then the data transfer path is: source→orbit1→GS1→POP1→POP2→GS2→orbit2→destination.

                 When the satellite cannot see any ground station, the data will continue to be transmitted between
                 ISLs in the orbit, and keep going in circles until the satellite can see the ground station due to
                 the offset of the sub-satellite point. sent to the ground station.

'''

def ring():
    pass