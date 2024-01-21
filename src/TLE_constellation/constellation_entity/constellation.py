'''

Author : yunanhou

Date : 2023/12/09

Function : This file defines the constellation class.

'''


class constellation:
    def __init__(self , constellation_name , number_of_shells , shells):
        self.constellation_name = constellation_name  # constellation name
        self.number_of_shells = number_of_shells  # the number of shells contained in the constellation
        # which shells are included in the constellation? it is a list type object, which stores shell class objects.
        self.shells = shells
