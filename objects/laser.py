from point import Point
import numpy as np

class Laser:

    def __init__(self, Board, Target_P):    
        self.board = Board      
        self.lenx = 2 * len(Board[0])
        self.leny = 2 * len(Board)
        self.target_P = Target_P

    # Find the direction of reflected laser  
    def laser_rflc(self, in_laser, side_bar):
        if side_bar:
            ref_laser = np.array([[-in_laser[0][0], in_laser[0][1]]])
        else:
            ref_laser = np.array([[in_laser[0][0], -in_laser[0][1]]])
        return ref_laser

    # One step laser move  
    def laser_move(self, laser):
        p_laser, d_laser = np.array([[laser[0], laser[1]]]), np.array([[laser[2], laser[3]]])
        Next_p = p_laser + d_laser

        # Delete the point in the set of target point, if it is reached
        for i, P in enumerate(self.target_P):
            if P[0].check_intersection(Next_p[0]):
                self.target_P = np.delete(self.target_P, i, 0)
        if Next_p[0][0] >= self.lenx or Next_p[0][0] <= 0 or Next_p[0][1] >= self.leny or Next_p[0][1] <= 0:
            return Next_p, d_laser, False
        
        # 1. Find the dominating block of next move
        # 2. Check wether the incident laser is from sides or from (top and bottom)
        if Next_p[0][0] % 2 == 0: 
            check_block = self.board[int((Next_p[0][1] - 1) / 2)][int((Next_p[0][0] + d_laser[0][0] - 1) / 2)]
            side_bar = True
        else:
            check_block = self.board[int((Next_p[0][1] + d_laser[0][1] - 1) / 2)][int((Next_p[0][0] - 1) / 2)]
            side_bar = False            

        if check_block.reflect:
            if check_block.continues:
                # Add the reflected laser as a new incident laser
                return np.vstack([Next_p, Next_p]), np.vstack([d_laser, self.laser_rflc(d_laser, side_bar)]), True # Refractive
            else:
                return Next_p, self.laser_rflc(d_laser, side_bar), True # Reflective
        else:
            if check_block.continues:
                return Next_p, d_laser, True # Space
            else:
                return Next_p, d_laser, False # Opaque

    # Loop through all incident lasers of a board
    def laser_run(self, lasers):
        i = 0
        laser_route = 0

        # Each refractive block can generate 3 new laser light (reflected),
        # i < 10 is a reasonable number to solve most boards. It can also 
        # be changed if the number of refractive blocks increases. 
        while i < len(lasers) and i < 10:
            laser_cont = True
            laser = np.array([lasers[i]])

            p_laser, d_laser = np.array([[laser[0][0], laser[0][1]]]), np.array([[laser[0][2], laser[0][3]]])
            post_p = p_laser - d_laser
            next_p = p_laser + d_laser

            if next_p[0][0] >= self.lenx or next_p[0][0] <= 0 or next_p[0][1] >= self.leny or next_p[0][1] <= 0:
                laser_cont = False
                i += 1 
                continue

            if p_laser[0][0] % 2 == 0: 
                first_block = self.board[int((p_laser[0][1] - 1) / 2)][int((p_laser[0][0] + d_laser[0][0] - 1) / 2)]
                side_bar = True
            else:
                first_block = self.board[int((p_laser[0][1] + d_laser[0][1] - 1) / 2)][int((p_laser[0][0] - 1) / 2)]
                side_bar = False           

            # Before the first step, how the first block influence incident light
            if first_block.reflect:
                if first_block.continues:
                    lasers = np.vstack([lasers, np.hstack([p_laser, self.laser_rflc(d_laser, side_bar)])]) # Refractive
                else:
                    laser = np.hstack([p_laser, self.laser_rflc(d_laser, side_bar)]) # Reflective
            else:
                if not first_block.continues:
                    laser_cont = False # Opaque

            # Loop through all steps of a laser light
            while laser_cont:
                P_laser, D_laser, laser_cont = self.laser_move(laser[0])
                laser = np.hstack((P_laser, D_laser))
                # Set a reasonable number to prevent infinite loop
                laser_route += 1
                if laser_route >= 100:
                    laser_cont = False
                    break
                if len(laser) == 2:
                    lasers = np.vstack([lasers, laser[1]])
            i += 1
        # Check if all targets have been reached
        if len(self.target_P) == 0:
            return True
        return False