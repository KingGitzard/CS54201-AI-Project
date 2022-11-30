class Puzzle:
    def __init__(self, puzzlearray):
        self.grid  = puzzlearray

        count = 0
        for r in range(len(puzzlearray)):
            for c in range(len(puzzlearray[r])):
                count += 1
        self.length = count

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

    def display(self):
        print ( )




puz = Puzzle([[0,1,2,3,4,5,6,7,8],[1,'','','',0,0,0,0,0],[2,0,0,0,0,0,0,0,0],[3,0,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,0,0],[5,0,0,0,0,0,0,0,0],[6,0,0,0,0,0,0,0,0],[7,0,0,0,0,0,0,0,0],[8,0,0,0,0,0,0,0,0]])

#print(puz.length)

#print("Grid:",puz.grid[5])
#print("Column:",puz.column(5))
#print("Row:",puz.row(5))

print("Block0:",puz.block(0))
print("Block1:",puz.block(1))
print("Block2:",puz.block(2))
print("Block3:",puz.block(3))
print("Block4:",puz.block(4))
print("Block5:",puz.block(5))
print("Block6:",puz.block(6))
print("Block7:",puz.block(7))
print("Block8:",puz.block(8))
