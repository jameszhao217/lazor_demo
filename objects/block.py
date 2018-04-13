
class Block(object):
   
    def __init__(self,n):
        # n a list of an integer decribing block type
        # 0 available, 1 unavailable, 2 refract,3reflect,4opaque  
        self.num = n
        self.laser_int(n)
        self.continues
        self.reflect
    def laser_int(self,num): #how it interacts with a laser hitting it
        Cont = False #laser does not continues in direction
        Reflect = False # laser does not reflect
        if num in ('2','3'):
            Reflect=True
        if num in ('2','0','1'):
            Cont = True
        self.reflect = Reflect
        self.continues = Cont
