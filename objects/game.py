import sys
import copy
import itertools
import numpy as np

from block import Block
from point import Point
from laser import Laser

from itertools import permutations # Used in generate_boards(self)


class Game(object):
    
    # initialize object
    def __init__(self, fptr):

        self.fname = fptr
        self.read(fptr)

    # so the board read in can be printed
    def __str__(self):
        a = 'this is the board read in'+'\n'
        b = '\n'.join(self.display_board)
        display=a+b
        return display
    
    #read in the board 
    def read(self, fptr):

        lines = [] # relevant lines 
        P = [] # points coordinates
        lasers = [] # laser direction and position
        num_blocks = np.zeros((3,1)) # array of number of each type of block [A,B,C]
        # read board only keep relevant lines
        with open(fptr,"r") as f:
           for line in f:
               if line[0] == "#" or line == "\n" or line == "GRID START\n":
                   pass
               else:
                lines.append(line)
        # find size of board create empty matrix rows x collumns
        collumns = []
        display_board = [] # so you can print board __str__
        rows = 0
        characters = ['x','o','A','B','C']
        # find size of board/create string to print Board        
        for line in lines:
             if line[0] in characters and line[4] in characters:
               rows+=1
               collumns.append(line.count('o') + line.count('x')+line.count('A')+line.count('B')+line.count('C'))
               display_board.append(line)
             else: break
        #B   o   o   o
        #o o B

        board = np.empty((rows,max(collumns)),dtype=str)
        #build board with the correct string
        spacing=4
        if display_board[0][2] in characters:
            spacing = 2
        for i in range(rows):
            a = lines[i]
            for j in range(max(collumns)):
                if a[j*spacing] in characters:
                    board[i,j] = a[j*spacing]
                else:
                    print('there is an error with reading in the board')
        # assemble vector of points, lasers, blocks
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
        # convert to numpy
        for i in range(len(laser)):
            laser[i] = np.fromstring(lasers[i],dtype=int,sep=' ')
        # convert to objects
        for i in range(len(Ps)):
            Ps[i] = np.fromstring(P[i],dtype = int,sep=' ')
            B = Point(Ps[i])
            Pts[i] = B
        self.board = board
        self.num_type_blocks = num_blocks
        self.points = Pts
        self.laser = laser
        self.display_board = display_board   
        
    # Generate all possible board variations
    def generate_boards(self):

        ### Obtain the number of each type of blocks from num_type_blocks
        N_Blocks_A = int(self.num_type_blocks[0])   # -----> Numbered 3
        N_Blocks_B = int(self.num_type_blocks[1])   # -----> Numbered 4        
        N_Blocks_C = int(self.num_type_blocks[2])   # -----> Numbered 2
        N_Blocks = N_Blocks_A + N_Blocks_B + N_Blocks_C # Total Number of Blocks
        
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
            '''
            Found on StackOverflow: 
            Generate permutations of list with repeated elements

            ***Reference**

             - https://stackoverflow.com/a/4250183

            '''
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

        # Make an empty list to write down all partitions
        boards_final = []
        
        pointer = 0
        for i in range(len(ppp_draft)):
            
            boards_element = []    
            if pointer >= len(partitions_blocks):
                 turnover = pointer/len(partitions_blocks)
                 pointer = pointer - len(partitions_blocks)*turnover # continue onto 
            
            count = 0
            for j in range(len(ppp_draft[i])):                
                if ppp_draft[i][j] == 0:
                    boards_element.append(ppp_draft[i][j])
                else:
                    boards_element.append(int(partitions_blocks[pointer][count]))
                    count += 1

            pointer += 1
            boards_final.append(boards_element)

        ##############################################
        ### FINALLY, Assign partitions into boards ###
        ##############################################

        for i in range(0, len(ppp_draft)):
            ppp = boards_final[i]
            board_draft = []
            counter = 0
            for x in range(0, b_rows):
                for y in range(0, b_cols):
                    if self.board[x,y] == 'o':
                        board_draft.append(ppp[counter])
                        counter = counter + 1
                    elif self.board[x,y] == 'A':
                        board_draft.append(3)
                    elif self.board[x,y] == 'B':
                        board_draft.append(4)
                    elif self.board[x,y] == 'C':
                        board_draft.append(2)
                    else:
                        board_draft.append(1)
            boards.append(board_draft)

        self.boards = boards       
        return boards


    def set_board(self, board):
        
        ### Reshape the board (1D-array) into matrix form
        AAA = np.array(board) 
        BBB = np.reshape(AAA, (self.rows, self.cols))      
        
        ### Define block object
        b0 = Block(0)
        b1 = Block(1)
        b2 = Block(2)
        b3 = Block(3)
        b4 = Block(4)
        
        ### Convert every element in the matrix into block object (saves memory)
        BBB = np.array(BBB, dtype=Block)
        for i in range(self.rows):
            for j in range(self.cols):
                if BBB[i,j] == 3:       # TYPE A
                    BBB[i,j] = b3
                elif BBB[i,j] == 4 :    # TYPE B
                    BBB[i,j] = b4
                elif BBB[i,j] == 2:     # TYPE C
                    BBB[i,j] = b2
                elif BBB[i,j] == 0:     # Available
                    BBB[i,j] = b0
                else:                   # Not Available
                    BBB[i,j] = b1

        return BBB
    

    def save_board(self):

        # We used integers to represent each block type to improve our speed
        # Now, we convert the integers back into Block types (A,B,C)
        solution_converted = []
        for i in range(len(self.solution)):
            if self.solution[i] == 0:
                solution_converted.append('o')
            elif self.solution[i] == 1:
                solution_converted.append('x')
            elif self.solution[i] == 2:
                solution_converted.append('C')
            elif self.solution[i] == 3:
                solution_converted.append('A')                
            else:
                solution_converted.append('B')

        # Reshape the 1D array into matrix (board) form
        board_draft_solution = solution_converted
        board_solution = np.array(board_draft_solution)
        board_sol_arranged = np.reshape(board_solution, (self.rows, self.cols))
        print(board_sol_arranged)

        # Write the solution board to an external file named "solution.txt" 
        np.savetxt('solution.txt', board_sol_arranged, fmt='%s', delimiter=',')
        
    # run the game to solve
    def run(self):
        
        # Get all boards
        print("Generating all the boards..."),
        sys.stdout.flush()
        boards = self.generate_boards()
        print("Done")
        sys.stdout.flush() 

        print("Playing boards...") 
        sys.stdout.flush()
        
        # Loop through all boards, and "play" them
        for b_index, board in enumerate(boards):

            board_checking = self.set_board(board)
            Test_1 = Laser(board_checking, self.points)
            laser_solved = Test_1.laser_run(self.laser)
            
            #laser object returns a boolean after checking if all points are met
            if laser_solved:           
                print('solved')
                self.solution = board
                self.save_board()
                break
