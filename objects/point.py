import numpy as np
class Point(object):
    
    def __init__(self, coordinates):
        # stores point coordinates
        self.coord1 = coordinates
    def check_intersection(self,test1):
        # checks for laser intersection of coordinates
        if self.coord1[0] == test1[0] and self.coord1[1] == test1[1]:
            return True
        else:
            return False

    # MORE
    # Difficulty 1
