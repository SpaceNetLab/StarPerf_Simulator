'''

Author : yunanhou

Date : 2023/08/24

Function : This file defines the constellation class, including the name of the constellation, and some parameters of
           the constellation (such as how many layers of shells there are, how many satellites there are, how many
           orbits there are, etc.)

'''

class constellation:
    def __init__(self , constellation_name , number_of_shells , shells):
        self.constellation_name = constellation_name  # constellation name
        self.number_of_shells = number_of_shells  # the number of shells contained in the constellation
        # which shells are included in the constellation? it is a list type object, which stores shell class objects.
        self.shells = shells