import sys
import copy
import itertools
import numpy as np
# import the Point, Block, and Laser objects


class Game(object):
    '''
    The game grid.  Here we read in some user input, assign all our blocks,
    lasers, and points, determine all the possible different combinations
    of boards we could make, and then run through them all to try and find
    the winning one.
    '''

    def __init__(self, fptr):
        '''
        Difficulty 1

        Initialize our game.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            game: *Game*
                This game object.
        '''
        self.fname = fptr
        self.read(fptr)
        
        self.generate_boards()
        self.available_space
        self.boards
        self.board #matrix representing the board (A,B,C,x,o)
        self.num_type_blocks # number of each type of block [A,B,C]
        self.points #points that need to be intersected with the laser
        self.laser #laser coordinates


    # DO SOMETHING HERE SO WE CAN PRINT A REPRESENTATION OF GAME!

    def read(self, fptr):
        '''
        Difficulty 3

        Some function that reads in a file, and generates the internal board.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            None
        '''
        lines = [] # relevant lines
        P = [] #laser points
        lasers = []
        num_blocks = np.zeros((3,1))
        with open(fptr,"r") as f:
           for line in f:
               if line[0] == "#" or line == "\n" or line == "GRID START\n":
                   pass
               else:
                lines.append(line)
        # find size of board create empty matrix rows x collumns
        collumns = []
        rows = 0
        characters = ['x','o','A','B','C']
        #create empty numpy array of the size of the board
        for line in lines:
             if line[0] in characters and line[4] in characters:
               rows+=1
               collumns.append(line.count('o') + line.count('x')+line.count('A')+line.count('B')+line.count('C'))
             else: break
        board = np.empty((rows,max(collumns)),dtype=str)
        print(lines)
        #build board with the ecorrect string
        for i in range(rows):
            a = lines[i]
            for j in range(max(collumns)):
                if a[j*4] in characters:
                    board[i,j] = a[j*4]
                else:
                    print('there is an error with reading in the board')
        for i in range(rows,len(lines)):
            a = lines[i]
            if a[0] == "A":num_blocks[0] = (a[2]) 
            elif a[0] == "B":num_blocks[1] = (a[2])
            elif a[0] == "C":num_blocks[2] = (a[2])
            elif a[0] == "L":lasers.append(a[2::].strip('\n'))
            elif a[0] == "P":P.append(a[2::].strip('\n'))
        laser = np.zeros((len(lasers),4))
        Points = np.zeros((len(P),2))
        for i in range(len(laser)):
            laser[i] = np.fromstring(lasers[i],dtype=int,sep=' ')
        for i in range(len(Points)):
            Points[i] = np.fromstring(P[i],dtype = int,sep=' ')
        self.board = board
        self.num_type_blocks = num_blocks
        self.points = Points
        self.laser = laser
        
        
        
    def generate_boards(self):

        ## Obtain the number of each type of blocks from num_type_blocks
        N_Blocks_A = int(self.num_type_blocks[0])   
        # -----> Numbered 2 for laser.py
        
        N_Blocks_B = int(self.num_type_blocks[1]) # 
        # -----> Numbered 3 for laser.py
        
        N_Blocks_C = int(self.num_type_blocks[2])
        # -----> Numbered 1 for laser.py
        
        ## Dimension of Board
        b_rows = len(self.board)
        b_cols = len(self.board[0])
        print (self.board)

        ## Obtain the number of available spaces from board read above
        count_zeros = 0
        for x in range(0, b_rows):
            for y in range(0,b_cols):
                if self.board[x,y] == 'o':
                    count_zeros = count_zeros+1
        self.available_space = count_zeros
        print(self.available_space)
 
        ## Initialize list "boards" used to store all possible permutations
        boards = []

        def get_partitions(n, k):
            '''
            A robust way of getting all permutations.  Note, this is clearly not the fastest
            way about doing this though.

            **Reference**

             - http://stackoverflow.com/a/34690583
            '''
            for c in itertools.combinations(range(n + k - 1), k - 1):
                yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]

        '''
        Difficulty 3        
        A function to generate all possible board combinations with the
        available blocks.
        First get all possible combinations of blocks on the board (we'll call these boards)
          We know we have self.blocks, and N_blocks = len(self.blocks)
          We also know we have self.available_space
          So, essentially we have to find all the possible ways to put N_blocks into
          self.available_space
        This becomes the "stars and bars" problem; however, we have distinguishable "stars",
        and further we restrict our system so that only one thing can be put in each bin.
        **Returns**
            None
        '''

        # Get the different possible block positions.  Note, due to the function we're using, we
        # skip any instance of multiple "stars in bins".
        
        # TYPE A BLOCKS
        if N_Blocks_A > 0:
            partitions_A = [
                p for p in get_partitions(N_Blocks_A, self.available_space) if max(p) == 1
            ]
            print(len(partitions_A))
            print(partitions_A[5])
            
            for q in range(0, len(partitions_A)):
                q_a = partitions_A[q]
                for qq in range(0,len(q_a)):
                    if q_a[qq] == 1:
                        q_a[qq] = 2
            print(partitions_A[5])
            
            # Assign partitions into boards
            for i in range(0,len(partitions_A)):  #4len(partitions)
                ppp = partitions_A[i]
                board_draft = []
                counter = 0
                for x in range(0, len(self.board)):
                    for y in range(0,len(self.board[0])):
                        if self.board[x,y] == 'o':
                            board_draft.append(ppp[counter])
                            counter = counter + 1
                        else:
                            board_draft.append(self.board[x,y])
                boards.append(board_draft)

        # TYPE B BLOCKS
        if N_Blocks_B > 0: 
            partitions_B = [
                p for p in get_partitions(N_Blocks_B, self.available_space-N_Blocks_A) if max(p) == 1
            ]
      #      print(len(partitions_B))
       #     print(partitions_B[5])
            
            for q in range(0, len(partitions_B)):
                q_b = partitions_B[q]
                for qq in range(0,len(q_b)):
                    if q_b[qq] == 1:
                        q_b[qq] = 3
      #      print(partitions_B[5])

            # Assign partitions into boards
            for i in range(0,len(partitions_B)):
                ppp = partitions_B[i]
                bbb = boards[i]
            #    print(ppp)
           #     print(bbb)
                
                counter2 = 0
                for x in range(0, len(bbb)):
                    if bbb[x] == 0:
                        bbb[x] = ppp[counter2]
                        counter2 = counter2 + 1

        # TYPE C BLOCKS
        if N_Blocks_C > 0:
            partitions_C = [
                p for p in get_partitions(N_Blocks_C, self.available_space-N_Blocks_A-N_Blocks_B) if max(p) == 1
            ]
#            print(len(partitions_C))

            # Assign partitions into boards
            for i in range(0,len(partitions_C)):
                ppp = partitions_C[i]
                bbb = boards[i]
                print(ppp)
                print(bbb)
                
                counter3 = 0
                for x in range(0, len(bbb)):
                    if bbb[x] == 0:
                        bbb[x] = ppp[counter3]
                        counter3 = counter3 + 1


        
        

        print(boards)
        self.boards = boards

        return boards




    def set_board(self, board):
        '''
        Difficulty 2

        A function to assign a potential board so that it can be checked.

        **Parameters**

            board: *list, Block*
                A list of block positions.  Note, this list is filled with
                None, unless a block is at said position, then it is a
                Block object.

        **Returns**

            None
        '''
        # YOUR CODE HERE 
        pass

    def save_board(self):
        '''
        Difficulty 2

        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Returns**

            None
        '''
        # YOUR CODE HERE
        pass

    def run(self):
        '''
        Difficulty 3

        The main code is here.  We call the generate_boards function, then we
        loop through, using set_board to assign a board, "play" the game,
        check if the board is the solution, if so save_board, if not then
        we loop.

        **Returns**

            None
        '''

        # Get all boards
        print("Generating all the boards..."),
        sys.stdout.flush()
        boards = self.generate_boards()
        print("Done")
        sys.stdout.flush() 

        print("Playing boards...") 
        sys.stdout.flush()
        # Loop through the boards, and "play" them
        for b_index, board in enumerate(boards):
            # Set board
            self.set_board(board)

            # MAYBE MORE CODE HERE?

            # LOOP THROUGH LASERS
            for j, laser in enumerate(current_lasers):
              child_laser = None
              child_laser = laser.update(self.board, self.points)

            # MAYBE MORE CODE HERE?
            # some_file.py

            # CHECKS HERE
            
            
            
#read board and dispose of non-pertanent lines


B = Game("diagonal_8.input")


