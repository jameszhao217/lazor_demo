# 0: available space
# 1: unavailable space
# 2: refractive block
# 3: reflective block
# 4: opaque block
# 5: outbound
 

block_fail = [[0., 2., 4., 0.],
        [3., 2., 4., 0.],
        [0., 1., 3., 0.],
        [0., 0., 0., 0.]]

block_success = [[0., 2., 4., 0.],
         [3., 2., 1., 0.],
         [0., 1., 3., 0.],
         [0., 0., 0., 0.]]

# board_fail = [[5., 5., 5., 5., 5., 5., 5., 5., 5.],
#               [5., 0., 2., 2., 4., 4., 4., 0., 5.],
#               [5., 3., 0., 2., 0., 4., 0., 0., 5.],
#               [5., 3., 3., 2., 4., 4., 4., 0., 5.],
#               [5., 3., 0., 2., 0., 4., 0., 0., 5.],
#               [5., 0., 1., 1., 3., 3., 3., 0., 5.],
#               [5., 0., 0., 1., 0., 3., 0., 0., 5.],
#               [5., 0., 0., 0., 0., 0., 0., 0., 5.],
#               [5., 5., 5., 5., 5., 5., 5., 5., 5.]]

# board_succ = [[5., 5., 5., 5., 5., 5., 5., 5., 5.],
#               [5., 0., 2., 2., 4., 4., 4., 0., 5.],
#               [5., 3., 0., 2., 0., 4., 0., 0., 5.],
#               [5., 3., 3., 2., 2., 0., 0., 0., 5.],
#               [5., 3., 0., 2., 0., 3., 0., 0., 5.],
#               [5., 0., 1., 1., 3., 3., 3., 0., 5.],
#               [5., 0., 0., 1., 0., 3., 0., 0., 5.],
#               [5., 0., 0., 0., 0., 0., 0., 0., 5.],
#               [5., 5., 5., 5., 5., 5., 5., 5., 5.]]

lazer = [(1, 9, 1, -1)]

class Laser:
  '''
  The Laser.  We need to store both the starting position and direction of
  the laser.
  '''
  def __init__(self, Board, laser, Target_P):
    '''
    Difficulty 1

    DONT FORGET TO COMMENT!
    '''
    # MORE
    # Difficulty 4        
    self.board = Board           # import Board matrix
    self.lenx, self.leny = 2 * len(Board[0]), 2 * len(Board)
    self.P_laser = [(laser_P[0], laser_P[1]) for laser_P in laser]    # import laser starting point
    self.D_laser = [(laser_D[2], laser_D[3]) for laser_D in laser]    # import laser starting direction
    self.target_P = Target_P

  def laser_rflc(side_bar):
    if side_bar:
      D_laser = tuple(x * y for x, y in zip(D_laser, (-1., 1.)))
    else:
      D_laser = tuple(x * y for x, y in zip(D_laser, (1., -1.)))  
    return D_laser


  def laser_move(self, P_laser, D_laser):
    Next_x, Next_y = tuple(x + y for x, y in zip(P_laser, D_laser))

    if Next_x >= self.lenx or Next_x <= 0 or Next_y >= self.leny or Next_y <= 0:
      return [(Next_x, Next_y) + D_laser], False

    if Next_x % 2 == 0: # check whether the bar is at sides 
      check_block = self.board[(Next_x + D_laser[0] + 1) / 2][(Next_y + 1) / 2]
      side_bar = True
    else:
      check_block = self.board[(Next_x + 1) / 2][(Next_y + D_laser[1] + 1) / 2]
      side_bar = False

    if check_block == 0 or 1: # Available and unavailable spaces
      return [(Next_x, Next_y) + D_laser], True
    elif check_block == 2:    # Refractive block
      return [(Next_x, Next_y) + D_laser, (Next_x, Next_y) + laser_rflc(side_bar)], True
    elif check_block == 3:    # Reflective block
      return [(Next_x, Next_y) + laser_rflc(side_bar)], True             
    elif check_block == 4:    # Opaque block (else?)
      return [(Next_x, Next_y) + D_laser], False                   

  def laser_ray(self, P, D, laser_route): # finish a laser ray
    laser_cont = True
    while laser_cont:
      Next_laser, laser_cont = laser_move(P, D)
      for i in Next_laser:

      # laser_route += Next_laser[0]
      # if len(Next_laser) == 2:
      #     self.P_laser += Next_laser[1]
      # for i in Next_laser:
      #     if i in laser_route:
      #         laser_cont = False
    return laser_route

  def laser_board(self, P_laser_all, D_laser_all): # run laser on board and decide if it has passed all desiered points
    # for i in range(len(self.P_laser)):





  # 1. create matrix 
  # 2. find all points laser travel through 
  # 3. check if all desired points has been covered (Maybe should be in Game.py)



