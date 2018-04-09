
class Block(object):
    '''
    A generic block for lazor.  We make this extendable so that it can be
    defined as either:

        (a) Reflecting block - Only reflects the laser
        (b) Opaque block - Absorbs the laser
        (c) See-Through block - Both reflects and lets light pass
    '''
    def __init__(self,n):
        self.num = n
        self.laser_int(n)
        self.reflect
        self.refract
    def laser_int(self,num): #how it interacts with a laser hitting it
        Reflect = False
        Refract = False
        if num in (2,3):
            Reflect=True
            if num == 2:
                Refract = True
        self.reflect = Reflect
        self.refract = Refract
            
block = Block(2)  

