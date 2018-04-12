import numpy as np
class Point(object):
    '''
    The Point.  This object desribes the points for which we want the laser
    light to intersect.
    '''
    def __init__(self, coordinates):
        '''
        Difficulty 1

        DONT FORGET TO COMMENT!
        '''
        self.coord1 = coordinates
    def check_intersection(self,test1):
        if self.coord1[0] == test1[0] and self.coord1[1] == test1[1]:
            return True
        else:
            return False

    # MORE
    # Difficulty 1
