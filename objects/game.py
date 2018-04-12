import sys
import copy
import itertools
import numpy as np
from block import Block
#from laser import Laser
from point import Point

from itertools import permutations


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
        
    def __str__(self):
        a = 'this is the board read in'+'\n'
        b = '\n'.join(self.display_board)
        display=a+b
        return display
        
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
        display_board = []
        rows = 0
        characters = ['x','o','A','B','C']
        #create empty numpy array of the size of the board
        for line in lines:
             if line[0] in characters and line[4] in characters:
               rows+=1
               collumns.append(line.count('o') + line.count('x')+line.count('A')+line.count('B')+line.count('C'))
               display_board.append(line)
             else: break
        board = np.empty((rows,max(collumns)),dtype=str)
        #build board with the correct string
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
        Ps = np.zeros((len(P),2))
        Pts = np.zeros((len(P),1),dtype=Point)
        for i in range(len(laser)):
            laser[i] = np.fromstring(lasers[i],dtype=int,sep=' ')
        for i in range(len(Ps)):
            Ps[i] = np.fromstring(P[i],dtype = int,sep=' ')
            B = Point(Ps[i])
            Pts[i] = B
        self.board = board
        self.num_type_blocks = num_blocks
        self.points = Pts
        self.laser = laser
        self.display_board = display_board   
        
        
    def generate_boards(self):

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

        ### Obtain the number of each type of blocks from num_type_blocks

        N_Blocks_A = int(self.num_type_blocks[0])   
        # -----> Numbered 3 for laser.py
        
        N_Blocks_B = int(self.num_type_blocks[1])
        # -----> Numbered 4 for laser.py
        
        N_Blocks_C = int(self.num_type_blocks[2])
        # -----> Numbered 2 for laser.py
        
        N_Blocks = N_Blocks_A + N_Blocks_B + N_Blocks_C
        # Total Number of Blocks from the input file
        
        ### Dimension of Board
        b_rows = len(self.board)
        b_cols = len(self.board[0])
        self.rows = b_rows
        self.cols = b_cols
 

        ### Obtain the number of available spaces from board read above
        count_zeros = 0
        for x in range(0, b_rows):
            for y in range(0,b_cols):
                if self.board[x,y] == 'o':
                    count_zeros = count_zeros+1
        self.available_space = count_zeros

        ### Initialize list "boards" used to store all possible permutations
        boards = []

        ### Function used to get all permuations
        def get_partitions(n, k):
            '''
            A robust way of getting all permutations.  Note, this is clearly not the fastest
            way about doing this though.

            **Reference**

             - http://stackoverflow.com/a/34690583
            '''
            for c in itertools.combinations(range(n + k - 1), k - 1):
                yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]
        
        ### Get the different possible block positions.  
        # Note, due to the function we're using, we skip any instance of multiple "stars in bins".
        partitions = [
            p for p in get_partitions(N_Blocks, self.available_space) if max(p) == 1
        ]
        self.partitions = partitions

        ###################################################################
        ### Now we have the partitions, we just need to make our boards ###
        ###################################################################
        
        ### Make a list of all types of block
        list_block = ''
        for i in range(0, N_Blocks_A):
            list_block = list_block + '3' #list_block.append(200 + i)
        for i in range(0, N_Blocks_B):
            list_block = list_block + '4' #list_block.append(300 + i)
        for i in range(0, N_Blocks_C):
            list_block = list_block + '2' # list_block.append(100 + i)           
        
        ### Functions used to produce internal permutations
        def unique_perms(series):
            return {"".join(p) for p in permutations(series)}
        
        ### Obtain the internal permutations at each board partition
        partitions_blocks = sorted(unique_perms(list_block))


        ### Generate the Structure of boards, which will be filled in with 
        # internal permuations at each blocks assignment
        ppp_draft = []
        for i in range(0, len(partitions)): #len(partitions)):
            for j in range(0, len(partitions_blocks)):
                ppp_draft.append(partitions[i])


        ####################################################
        ### Assign Internal Permutations into Partitions ###
        ####################################################

        boards_final = []
        
        pointer = 0
        for i in range(len(ppp_draft)):
            
            boards_element = []
            
            if pointer >= len(partitions_blocks):
                 turnover = pointer/len(partitions_blocks)
                 pointer = pointer - len(partitions_blocks)*turnover
            
            count = 0
            for j in range(len(ppp_draft[i])):                
                if ppp_draft[i][j] == 0:
                    boards_element.append(ppp_draft[i][j])
                else:
                    boards_element.append(int(partitions_blocks[pointer][count]))
                    count += 1

            pointer += 1
            boards_final.append(boards_element)
                
#        print(boards_final)

        ##############################################
        ### FINALLY, Assign partitions into boards ###
        ##############################################

        for i in range(0, len(ppp_draft)):    #len(boards_final)):
            ppp = boards_final[i]
            board_draft = []
            counter = 0
            for x in range(0, b_rows):
                for y in range(0, b_cols):
                    if self.board[x,y] == 'o':
                        board_draft.append(ppp[counter])
                        counter = counter + 1
                    else:
                        board_draft.append(self.board[x,y])
            boards.append(board_draft)

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

        
        AAA = np.array(board)         
        BBB = np.reshape(AAA, (self.rows, self.cols))      
                
        
        b0 = Block('0')
        b1 = Block('1')
        b2 = Block('2')
        b3 = Block('3')
        b4 = Block('4')
        
        BBB = np.array(BBB, dtype=Block)
        for i in range(self.rows):
            for j in range(self.cols):
                if BBB[i,j] == '3':     # TYPE A
                    BBB[i,j] = b3
                elif BBB[i,j] == '4':   # TYPE B
                    BBB[i,j] = b4
                elif BBB[i,j] == '2':   # TYPE C
                    BBB[i,j] = b2
                elif BBB[i,j] == 'A':   # TYPE A
                    BBB[i,j] = b3
                elif BBB[i,j] == 'B':   # TYPE B
                    BBB[i,j] = b4
                elif BBB[i,j] == 'C':   # TYPE C
                    BBB[i,j] = b2
                elif BBB[i,j] == '0':   # Available
                    BBB[i,j] = b0
                else:                   # Not Available
                    BBB[i,j] = b1

        return BBB
    

    def save_board(self):
        
        '''
        Difficulty 2

        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Returns**

            None
        '''
        
        # Write the solution board to an external file named "solution.txt"   
        board_draft_solution = self.solution   
        board_solution = np.array(board_draft_solution)
        board_sol_arranged = np.reshape(board_solution, (self.rows, self.cols))
        print(board_sol_arranged)
        np.savetxt('solution.txt', board_sol_arranged, fmt='%s', delimiter=',')
        

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
            board_checking = self.set_board(board)
            # MAYBE MORE CODE HERE?
            # LOOP THROUGH LASERS
            for j, laser in enumerate(current_lasers): 
              child_laser = None
              child_laser = laser.update(board_checking, self.Pts)
            if laser_solved:    #laser object returns a boolean after checking if all points are met       
                print('solved')
                self.solution = board
                save_board()
                break

#read board and dispose of non-pertanent lines

# B = Game("braid_5.input")

BB = Game("../boards/diagonal_8.input")
print(BB)
A = BB.run()
