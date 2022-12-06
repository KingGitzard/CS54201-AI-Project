import os, getopt, sys, ast
from datetime import datetime



class Puzzle:
    def __init__(self, puzzlearray):
        self.grid  = puzzlearray

        count = 0
        for r in range(len(puzzlearray)):
            for c in range(len(puzzlearray[r])):
                count += 1
        self.length = count
        self.constraints = []
        self.baseSet = {1,2,3,4,5,6,7,8,9}

    def column(self,i):
        return [row[i] for row in self.grid]

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


    def gridEvaluate(self):
        self.constraints = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.constraints.append(self.cellEvaluate(r,c))

    def cellEvaluate(self,row,col):
        if self.cellValue(row,col) == 0:
            cell_constraint_set =  set(self.row(row))     # get the value of the cell
            cell_constraint_set = cell_constraint_set.union(set(self.column(col)),set(self.block(self.blockByRC(row,col))))
            cell_constraint_set.remove(0)
            return cell_constraint_set
        else:
            cell_constraint_set = set([])  #set to empty if it is already filled
            return cell_constraint_set


    def cellValue(self,r,c):
        return self.grid[r][c]

    def updatecell(self,r,c,value):
        self.grid[r][c] = value

    def cellFilled(self,r,c):
        if self.cellValue(r,c) == 0:
            return False
        else:
            return True

    def isSolved(self):
        print("Entering Is Solved")
        solvedFlag = True
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                solvedFlag = self.cellFilled(r,c)
                if solvedFlag == False:
                    quit # breaks c loop
            if solvedFlag == False:
                quit # breaks r loop
        return solvedFlag
        print ("Done")


#------------  Working with Constraint List
    def cell_with_one_constraint(self):
        for cell in range(len(self.constraints)):
            if len(self.constraints[cell]) == 8:
                return cell


    def fill_constraints_of_one(self):
        self.gridEvaluate()
        mycell = self.cell_with_one_constraint()
        validateFlag = True  # assuming start, all is well

        while mycell != None and validateFlag == True:
            print("One Contraint:",mycell)
            myvalue = self.find_missing_digit(mycell)
            print("myvalue",myvalue)
            cellcart = self.getcartesian(mycell)
            print("cellcart:",cellcart)
            self.updatecell(cellcart[0],cellcart[1],myvalue)
#            self.display()
            self.gridEvaluate()
            validateFlag = self.validateGrid()
            mycell = self.cell_with_one_constraint()
        return validateFlag


    def find_missing_digit(self,Ordinal):
        myValueList = list(self.baseSet - self.constraints[Ordinal])
        return myValueList[0]

    def search(self):
        # find the most constrainted cell
        highestOrd = None
        highestLen = 0

        for o in range(len(self.constraints)):
#            print("trying:",o,"of len:",len(self.constraints[o]))
            if (len(self.constraints[o]) > highestLen):
                highestOrd = o
                highestLen = len(self.constraints[o])


        print("highestOrd:", highestOrd,"of len:",highestLen)
        # What are our options.
        # Choose a value.


    def validateGrid(self):           #return True if OK  False if not valid
        print ("validating grid")
        # Check if constraints have no filled an length of 9
        for cell in range(len(self.constraints)):
            p = self.getcartesian(cell)
            r = p[0]
            c = p[1]
            NumberOfConstranting = len(self.constraints[cell])
            if NumberOfConstranting == 9 and self.cellFilled(r,c) == False:
                print ("Somethings is wrong with cell:",cell)
                return False
        return True

    def solvePuzzle(self):
        #This loops through steps of solving puzzle
        validFlag = True

        validFlag = self.fill_constraints_of_one()
        self.displayConstraints()
        while self.isSolved() == False:
            #Push DFS Stack
            validFlag = self.fill_constraints_of_one() #Fill in ones
            print ("validFlag:", validFlag)
            #if not valid grid Pop DFS stack
        #puz.displayConstraints()

#        puz.search()

    def dfs(self):
        print("Start DFS")
        #TODO search for a value to try
        #Push Puzzle State to Stack





#------------- Display Items
    def displayConstraints(self):
        #displayConstraint list state
        for cell in range(len(self.constraints)):
            p = self.getcartesian(cell)
            x = p[0]
            y = p[1]
            #print (p,x,y)
            print("Cell:",cell,"Len:",len(self.constraints[cell]),"IsFilled:",self.cellFilled(x,y) ,self.constraints[cell])


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



#------------- ideas Not used yet



    def getOrdinal(self,row,col):
        return ((row * 9 ) + col)

    def getcartesian(self,ordinal):
        return ( [(ordinal // 9 ) , (ordinal % 9 )] )




#------------- deprecated
    def unique(self,list1):

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        unique_list.sort()
        unique_list.remove(0)
        return unique_list


#---------Pull in Paremeters

#------------------------------------Main Code ---------------------------------


os.system('clear')   # Clear the output screen

now = datetime.now()
print("--------------------------------------------------------------------------------------------------------------------")
print("----------------                               SUDOKU                     ", now,                    "--------------")
print("--------------------------------------------------------------------------------------------------------------------")



argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hi:v:",["ifile=","ofile="])
except getopt.GetoptError:
    print ('KMeans.py \n\t-i <inputfile> \n\t-v <verbos level> \n\t-h help')
    sys.exit(2)

for opt, arg in opts:
  if opt == '-h':                       #Help
     print ('Sudoku.py \n\t-i <inputfile> \n\t-v <verbos level> \n\t-h help')
     sys.exit()
  elif opt in ("-i"):                   #Input File
     inputfile = arg
  elif opt in ("-v"):                   #verbose level
     verboseLevel = arg




# Display Parameters Passed in
print ('Input file is :', inputfile)


if inputfile == None:
    print("Must have an input file to load puzzle please try again")
    exit()  # leave program no file.

# Handle file Data
if  inputfile != None :
    with open(inputfile, 'r') as f:
        lines = f.read().split(',\n')
        data = [ast.literal_eval(line) for line in lines]

    InPuzzleData = data[0]


puz = Puzzle(InPuzzleData)

puz.display()  # display Start State
puz.solvePuzzle()





