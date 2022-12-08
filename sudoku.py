#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#  SUDOKU V 1.0
#  Written by:
#               Hunter  Harbison
#               Fred    Longo
#               Keith   Machina
#
#
#
#  example Run:
#           python3 sudoku.py  -i sudokuPuzzle/expert2.txt  -v 1
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


import os, getopt, sys, ast
from datetime import datetime
import copy



class Puzzle:
    def __init__(self, puzzlearray):
        self.grid  = puzzlearray
        self.stack = []
        self.stepFlag = False
        count = 0
        for r in range(len(puzzlearray)):
            for c in range(len(puzzlearray[r])):
                count += 1
        self.length = count
        self.constraints = []
        self.baseSet = {1,2,3,4,5,6,7,8,9}


    def setStepFlag(self,flagvalue):
        self.stepFlag = flagvalue


    # Returns column of a given cell
    def column(self,i):
        return [row[i] for row in self.grid]

    # Returns row of a given cell
    def row(self,i):
        return self.grid[i]


    def block(self,i):
        ret = []
        if i == 0:
            for r in range(0,3):
                for c in range(0,3):
                    ret.append(self.grid[r][c])
        elif i == 1:
            for r in range(0,3):
                for c in range(3,6):
                    ret.append(self.grid[r][c])
        elif i == 2:
            for r in range(0,3):
                for c in range(6,9):
                    ret.append(self.grid[r][c])
        elif i == 3:
            for r in range(3,6):
                for c in range(0,3):
                    ret.append(self.grid[r][c])
        elif i == 4:
            for r in range(3,6):
                for c in range(3,6):
                    ret.append(self.grid[r][c])
        elif i == 5:
            for r in range(3,6):
                for c in range(6,9):
                    ret.append(self.grid[r][c])

        elif i == 6:
            for r in range(6,9):
                for c in range(0,3):
                    ret.append(self.grid[r][c])

        elif i == 7:
            for r in range(6,9):
                for c in range(3,6):
                    ret.append(self.grid[r][c])
        elif i == 8:
            for r in range(6,9):
                for c in range(6,9):
                    ret.append(self.grid[r][c])

        return ret

    def blockByRC(self,r,c):
        if r in [0,1,2]:
            if c in [0,1,2]:
                return 0
            elif c in [3,4,5]:
                return 1
            elif c in [6,7,8]:
                return 2
        elif r in [3,4,5]:
            if c in [0,1,2]:
                return 3
            elif c in [3,4,5]:
                return 4
            elif c in [6,7,8]:
                return 5
        elif r in [6,7,8]:
            if c in [0,1,2]:
                return 6
            elif c in [3,4,5]:
                return 7
            elif c in [6,7,8]:
                return 8



    # Pushes all constrained to options onto the Stack for a give cell
    def push(self,cell,constrained,puzzle):
        for o in range(len(constrained)):
            self.stack.append(list([cell,constrained[o],copy.deepcopy(puzzle)]))
            if (AppParameter.verboseLevel > 0):
                print("                                                ---->Pushing     Cell:",cell,"Option:",constrained[o])

    # Pops options from the stack that has been exhausted in evaluation
    def pop(self):
        stackDepth = len(self.stack )
        if(stackDepth > 0):
            if(self.lastCellOptionOnStack(stackDepth)):
                if (AppParameter.verboseLevel > 0):
                    print('                                                ---->Popping 2   Cell:',self.stack[-1][0],"Option:",self.stack[-1][1])
                del self.stack[-1]  # remove last from stack
                self.pop()                    # recursively called to remove nested exhausted options

            else:
                if (AppParameter.verboseLevel > 0):
                    print('                                                ---->Popping 1   Cell:',self.stack[-1][0],"Option:",self.stack[-1][1])
                del self.stack[-1]
        else:
            print("Depth of",stackDepth," on the stack, Impossible!!!")
            exit()

    # Evaluates to see of this is the last cells option on stack for this cell
    # if so its returning true to trigger double popping logic
    def lastCellOptionOnStack(self, depth):
        position = depth - 1
        if (AppParameter.verboseLevel >= 3):
            print("comparing:",self.stack[position][0],"with",self.stack[position-1][0])
        if(self.stack[position][0] == self.stack[position-1][0]):
            return False
        else:
            return True

    # Recreates Puzzles grig from what was saved off in the stack
    def setPuzzleFromStack(self):
        # set up next
        stackDepth = len(self.stack )
        if (stackDepth > 0):
            self.grid = copy.deepcopy(self.stack[stackDepth-1][2])
            cell = self.stack[stackDepth-1][0]
            cell_option = self.stack[stackDepth-1][1]
            self.updatecellO(cell,cell_option)
            if (AppParameter.verboseLevel > 0):
                print("Updated(stack): ",cell, "myvalue: ",cell_option,"cellcart: ",self.getcartesian(cell))
                #print("Updated(const): ",mycell, "myvalue: ",myvalue, "cellcart: ",cellcart)



    # Creates the grid of constraining valuses for each cell.
    def gridEvaluate(self):
        self.constraints = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.constraints.append(self.cellEvaluate(r,c))


    # Evaluates and returns a list of a given cells constraining values
    def cellEvaluate(self,row,col):
        if self.cellValue(row,col) == 0:
            cell_constraint_set = set(self.row(row))                                                                            # get constraining items for row
            cell_constraint_set = cell_constraint_set.union(set(self.column(col)),set(self.block(self.blockByRC(row,col))))     # get constraining itmes for col and block  Unions all together.
            cell_constraint_set.remove(0)                                                                                       # remove filler of Zero
            return cell_constraint_set
        else:
            cell_constraint_set = set([])  #set to empty if it is already filled
            return cell_constraint_set

    #returns cell value
    def cellValue(self,r,c):
        return self.grid[r][c]

    # Updates cell with a given value by row col
    def updatecell(self,r,c,value):
        self.grid[r][c] = value

    # Updates cell with a given value by ordinal
    def updatecellO(self,cell,value):
        cart  = self.getcartesian(cell)
        self.grid[cart[0]][cart[1]] = value


    # Checks if cell has an assigned value
    def cellFilled(self,r,c):
        if self.cellValue(r,c) == 0:
            return False
        else:
            return True

    # Check if puzzle is done
    def isSolved(self):
        #print("Entering Is Solved")
        solvedFlag = True
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                solvedFlag = self.cellFilled(r,c)
                if solvedFlag == False:
                    return solvedFlag
            if solvedFlag == False:
                return solvedFlag
        return solvedFlag
        print ("Done")

    # finds a cell only having one constrained to option
    def cell_with_one_constraint(self):
        for cell in range(len(self.constraints)):
            if len(self.constraints[cell]) == 8:
                return cell


    # goes through grid filling in cells that are constrained to one option             ##
    # returns validateflag depending if it found the grid in a valid or invalid state   ##
    def fill_constraints_of_one(self):
        self.gridEvaluate()                                                     #Builds list of constraints.
        mycell = self.cell_with_one_constraint()                                # Returns a cell having one constrait
        validateFlag = True                                                     # assuming start, all is well

        while mycell != None and validateFlag == True:
            myvalue = self.find_missing_digit(mycell)
            cellcart = self.getcartesian(mycell)
            self.updatecell(cellcart[0],cellcart[1],myvalue)
            if (AppParameter.verboseLevel > 0):
                print("Updated(const): ",mycell, "myvalue: ",myvalue, "cellcart: ",cellcart)
            self.gridEvaluate()                                                 #Builds list of constraints.
            validateFlag = self.validateGrid()
            mycell = self.cell_with_one_constraint()
        return validateFlag

    # finds what he constrained to value is for a cell
    def find_missing_digit(self,Ordinal):
        myValueList = list(self.baseSet - self.constraints[Ordinal])
        return myValueList[0]

    # finds what the constrained to set is.
    def find_missing_set(self,Ordinal):
        myValueList = list(self.baseSet - self.constraints[Ordinal])
        return myValueList

    # Use seach to find what is the most constrained cell to put all it's options on the stack
    def searchForCellWithMostConstraining(self):
        highestOrd = None
        highestLen = 0

        for o in range(len(self.constraints)):
            if (len(self.constraints[o]) > highestLen):
                highestOrd = o
                highestLen = len(self.constraints[o])

        if (AppParameter.verboseLevel >= 3):
            print("highestOrd:", highestOrd,"of len:",highestLen)
        return highestOrd
        # What are our options.
        # Choose a value.

    # Checks to see grid is in a valid state
    def validateGrid(self):           #return True if OK  False if not valid
        # Check if constraints have no filled an length of 9
        for cell in range(len(self.constraints)):
            p = self.getcartesian(cell)
            r = p[0]
            c = p[1]
            NumberOfConstranting = len(self.constraints[cell])
            if NumberOfConstranting == 9 and self.cellFilled(r,c) == False:
                if (AppParameter.verboseLevel >= 3):
                    print ("Validation Failed on cell:",cell)
                return False
        return True

    # Input loop for interactive mode
    def interactiveLoop(self):
        while self.stepFlag:
            x = input('pause:')
            if (x == 'g'):
                self.display()
            elif(x == 's'):
                self.displayStack(False)
            elif(x == 'c'):
                self.displayConstraints()
            elif(x == 'r'):
                self.stepFlag = False
            elif(x == 'x'):
                exit()
            else:
                break


    # Main code loop for working on puzzle   -----------------------------------
    def solvePuzzle(self):
        #This loops through steps of solving puzzle
        validFlag = True

        validFlag = self.fill_constraints_of_one()                      # Fill in constraints of ones
        while self.isSolved() == False:

            self.interactiveLoop()

            if validFlag == True:
                #Push
                CellToPush =  self.searchForCellWithMostConstraining()    #Returns Cell With Most Constraining
                listofOptions =     self.find_missing_set(CellToPush)     #Returns Options for cell
                self.push(CellToPush,listofOptions,self.grid)             #Pushs Cell with Options to Stack
            else:
                self.pop()

            self.setPuzzleFromStack()                                     # Sets grid to the next item on stack
            validFlag = self.fill_constraints_of_one()                    # Fill in constraints of ones








    #------ Display list of constraining values for all cells.
    def displayConstraints(self):
        #displayConstraint list state
        for cell in range(len(self.constraints)):
            p = self.getcartesian(cell)
            x = p[0]
            y = p[1]
            #print (p,x,y)
            print("Cell:",cell,"Len:",len(self.constraints[cell]),"IsFilled:",self.cellFilled(x,y) ,self.constraints[cell])


    # Displays Grid in Puzzle Board format
    def display(self):
        print("-------------")
        for r in range(len(self.grid)):
            if r in [3,6]:
                print("-------------")
            line = '|'
            for c in range(len(self.grid[r])):
                if c in [3,6]:
                    line = line + '|'


                if (self.grid[r][c] == 0):
                    cellvalue = ' '
                else:
                    cellvalue = str(self.grid[r][c])

                line = line + cellvalue
            line = line + '|'
            print(line)
        print("-------------")
        return

    # Displays Grid in Puzzle Board format with the ability to give a buffer offset
    def displayGrid(self,grid,buff):
        buff = ' ' * buff
        horizontal = buff + "-------------"
        print(horizontal)
        for r in range(len(grid)):
            if r in [3,6]:
                print(horizontal)
            line = '|'
            for c in range(len(grid[r])):
                if c in [3,6]:
                    line = line + '|'


                if (grid[r][c] == 0):
                    cellvalue = ' '
                else:
                    cellvalue = str(grid[r][c])

                line = line + cellvalue
            line = line + '|'
            print(buff + line)
        print(horizontal)
        return

    # Displays Stack that is used in the Depth First Seach Logic
    def displayStack(self, shortFlag):
        if(shortFlag == None):
            shortFlag == False
        for e in range(len(self.stack)):
            print("this is the org position", self.stack[e][0],"this is the value",self.stack[e][1])
            if(shortFlag == False):
                self.displayGrid(self.stack[e][2], 30)


    # converts Cartesian to Ordinal
    def getOrdinal(self,row,col):
        return ((row * 9 ) + col)

    # converts Ordinal to Cartesian
    def getcartesian(self,ordinal):
        return ( [(ordinal // 9 ) , (ordinal % 9 )] )



# This class is created to handle input parameters
class Parameters:
    def __init__(self):
        self.commandLineFormat  = 'sudoku.py \n\t-i <inputfile> \n\t-v <verbos level> \n\t-s StepFlag \n\t-h help'
        self.verboseLevel       = 0
                                    # 0 = No Excess information
                                    # 1 = Basic workflow items (Push, Pop, Update)
                                    # 2 = App Paramerters
                                    # 3 = Evaluations


        self.stepFlag           = False
        self.helpFlag           = False
        self.inputfile         = []
        self.getParameters()


    def getParameters(self):
        argv = sys.argv[1:]    # gets back list of Arguments given on command line from the system
        try:
            opts, args = getopt.getopt(argv,"hsi:v:",["inputfile="])
        except getopt.GetoptError:
            print (self.commandLineFormat)
            sys.exit(2)

        for opt, arg in opts:
          if opt in ['-h','--help']:                       #Help
             print (self.commandLineFormat)
             sys.exit()
          elif opt in ["-i","--inputfile"]:                   #Input File
             self.inputfile = arg
          elif opt in ["-s"]:                   # Steps Through Flag
             self.stepFlag = True
          elif opt in ["-v"]:                   #verbose level
             self.verboseLevel = int(arg)


    def printAll(self):
        # Display Parameters Passed in
        print ('helpFlag', self.helpFlag)
        print ('Input file is :', self.inputfile)
        print ('stepFlag', self.stepFlag)
        print ('verboseLevel', self.verboseLevel)




#------------------------------------------------------------------------------
#------------------------------------Main Code ---------------------------------


os.system('clear')                                  # Clear the output screen

now = datetime.now()
print("--------------------------------------------------------------------------------------------------------------------")
print("----------------                               SUDOKU                     ", now,                    "--------------")
print("--------------------------------------------------------------------------------------------------------------------")


AppParameter = Parameters()   # gets parameters

#options to display Parameters
if (AppParameter.verboseLevel >= 2):
    AppParameter.printAll()


#Validate input file is set
if AppParameter.inputfile == None:
    print("Must have an input file to load puzzle please try again")
    exit()  # leave program no file.


# Handle inporting puzzle data from file
if  AppParameter.inputfile != None :
    with open(AppParameter.inputfile, 'r') as f:
        lines = f.read().split(',\n')
        data = [ast.literal_eval(line) for line in lines]
    InPuzzleData = data[0]





puz = Puzzle(InPuzzleData)              #Create Puzzle
puz.setStepFlag(AppParameter.stepFlag)  #Pass Set flag to puzzle

puz.display()                           # Display Start State of Puzzle
puz.solvePuzzle()                       # Solves the Puzzle
print('----- ----- ----- ----- All  Done ----- ----- ----- -----')
puz.display()                           # Display End State of Puzzle









