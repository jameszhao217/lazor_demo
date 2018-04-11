
class Point:
    '''
    The Point.  This object desribes the points for which we want the laser
    light to intersect.
    '''
    def __init__(self, pos):
        '''
        Difficulty 1

        DONT FORGET TO COMMENT!
        '''
        self.position = pos
    def check_intersection(self,pos):
        if self.position == pos:
            return True
        else:
            return False

    # MORE
    # Difficulty 1
