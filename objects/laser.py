from point import Point
import numpy as np

class Laser:

    def __init__(self, Board, Target_P):    
        self.board = Board           # import Board matrix
        self.lenx = 2 * len(Board[0])
        self.leny = 2 * len(Board)
        self.target_P = Target_P

    def laser_rflc(self, in_laser, side_bar):
        if side_bar:
            ref_laser = np.array([[-in_laser[0][0], in_laser[0][1]]])
        else:
            ref_laser = np.array([[in_laser[0][0], -in_laser[0][1]]])
        return ref_laser

    def laser_move(self, laser):
        p_laser, d_laser = np.array([[laser[0], laser[1]]]), np.array([[laser[2], laser[3]]])
        Next_p = p_laser + d_laser
        # print(Next_p)
        for i, P in enumerate(self.target_P):
            if P[0].check_intersection(Next_p[0]):
                self.target_P = np.delete(self.target_P, i, 0)

        # if Next_p[0][0] >= self.lenx or Next_p[0][0] <= 0 or Next_p[0][1] >= self.leny or Next_p[0][1] <= 0:
            # return Next_p, D_laser, False
        try:
            if Next_p[0][0] % 2 == 0: # check whether the bar is at sides
                check_block = self.board[int((Next_p[0][1] - 1) / 2)][int((Next_p[0][0] + d_laser[0][0] - 1) / 2)]
                side_bar = True
            else:
                check_block = self.board[int((Next_p[0][1] - d_laser[0][1] - 1) / 2)][int((Next_p[0][0] - 1) / 2)]
                side_bar = False            
        except IndexError:
            return Next_p, d_laser, False

        if check_block.reflect:
            if check_block.continues:
                # print('refract')
                return np.vstack([Next_p, Next_p]), np.vstack([d_laser, self.laser_rflc(d_laser, side_bar)]), True # Refractive
            else:
                # print('reflect')
                return Next_p, self.laser_rflc(d_laser, side_bar), True # Reflective
        else:
            if check_block.continues:
                return Next_p, d_laser, True  # Space
            else:
                return Next_p, d_laser, False # Opaque

    def laser_run(self, lasers): # finish a board
        i = 0
        laser_route = lasers
        while i < len(lasers):
            # print(len(lasers))     
            laser_cont = True
            laser = np.array([lasers[i]])
            while laser_cont:
                P_laser, D_laser, laser_cont = self.laser_move(laser[0])
                # print(laser_cont)
                # print(P_laser, D_laser)
                laser = np.hstack((P_laser, D_laser))
                # print(laser)
                Repeat_laser = np.equal(laser, laser_route)
                for j, Repeat_check in enumerate(Repeat_laser):
                    if Repeat_check.all():
                        laser = np.delete(laser, j, 0)
                if len(laser) == 2:
                    np.vstack([lasers, laser[1]])
                # print(len(self.target_P))

            i += 1
        if len(self.target_P) == 0:
            return True
        return False