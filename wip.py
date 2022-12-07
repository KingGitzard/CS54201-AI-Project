import sys, getopt

class Parameters:
    def __init__(self):
        self.commandLineFormat  = 'sudoku.py \n\t-i <inputfile> \n\t-v <verbos level> \n\t-s StepFlag \n\t-h help'
        self.verboseLevel       = 0
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
             self.verboseLevel = arg


    def printAll(self):
        # Display Parameters Passed in
        print ('helpFlag', self.helpFlag)
        print ('Input file is :', self.inputfile)
        print ('stepFlag', self.stepFlag)
        print ('verboseLevel', self.verboseLevel)



class Program:
    def __init__(self):
        self.verbos = []

    def run(self):
        print("running")
        print("AppParameter.verboseLevel",AppParameter.verboseLevel)

app = Program()



AppParameter = Parameters()
AppParameter.printAll()



app.run()