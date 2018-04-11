
class Block(object):
    '''
    A generic block for lazor.  We make this extendable so that it can be
    defined as either:

        (a) Reflecting block - Only reflects the laser
        (b) Opaque block - Absorbs the laser
        (c) See-Through block - Both reflects and lets light pass
    '''
    def __init__(self,n):
        # n is integer decribing block type
        # 0 available, 1 unavailable, 2 refract,3reflect,4opaque
        
        self.num = n
        self.laser_int(n)
        self.continues
        self.reflect
    def laser_int(self,num): #how it interacts with a laser hitting it
        Cont = False #laser continues in direction
        Reflect = False # laser is reflected
        if num in ('2','3'):
            Reflect=True
        if num in ('2','0','1'):
            Cont = True
        self.reflect = Reflect
        self.continues = Cont
            
A = Block('2')
print(A.reflect)