class Puzzle:
    def __init__(self, puzzlearray):
        self.grid  = puzzlearray

        count = 0
        for r in range(len(puzzlearray)):
            for c in range(len(puzzlearray[r])):
                count += 1
        self.length = count
        self.constraints = []

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
        cell_constraint_set =  set(self.row(row))
        cell_constraint_set = cell_constraint_set.union(set(self.column(col)),set(self.block(self.blockByRC(row,col))))
        cell_constraint_set.remove(0)
        return cell_constraint_set


    def getOrdinal(row,col):
        return ((row * 9 ) + col)

    def getcartesian(ordinal):
        return ( [(ordinal // 9 ) , (ordinal % 9 )] )





#------------  Working with Constraint List
    def cell_with_one_constraint(self):
#TODO:  This need to looks at constrains not values.
#TODO:  ignore cells filled in.
        for cell in range(len(self.constraints)):
            if len(self.constraints[cell]) == 1:
                return cell


    def fill_constraints_of_one(self):
        KeepSearching = True
        LoopCount = 0

        while (KeepSearching and LoopCount < 81):
            LoopCount += 1
            CelltoUpdate = self.cell_with_one_constraint()
            #TODO UpdateCell




#------------- Display Items
    def displayConstraints(self):
        #displayConstraint list state
        for cell in range(len(self.constraints)):
            print("Cell:",cell,"Len:",len(self.constraints[cell]),self.constraints[cell])


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
    def cellValue(self,r,c):
        return self.grid[r][c]

    def cellFilled(self,r,c):
        if self.cellValue(r,c) == 0:
            return False
        else:
            return True


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



puz = Puzzle([[0,6,0,8,0,0,5,0,0],[0,0,5,0,0,0,3,6,7],[3,7,0,0,6,5,8,0,9],[6,0,9,0,0,2,1,0,0],[0,0,1,4,8,9,2,0,0],[0,0,0,3,0,6,9,0,0],[0,5,0,0,0,0,4,0,0],[0,1,0,5,4,7,0,0,3],[0,9,6,0,3,8,0,5,1]])

#print(puz.length)

#print("Grid:",puz.grid[5])
#print("Column:",puz.column(5))
#print("Row:",puz.row(1))


puz.display()

puz.gridEvaluate()

puz.displayConstraints()


print("One Contraint:",puz.cell_with_one_constraint())











