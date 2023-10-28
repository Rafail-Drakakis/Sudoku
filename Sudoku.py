import random

BOARD_SIZE = 9
SUBSECTION_SIZE = 3
BOARD_START_INDEX = 0

NO_VALUE = 0
MIN_VALUE = 1
MAX_VALUE = 9


def printBoard(brd): #Given method
    for row in range(BOARD_START_INDEX, BOARD_SIZE):
        for column in range(BOARD_START_INDEX, BOARD_SIZE):
            print(brd[row][column], " ")
        print("")

def solve(initialBoard): #Given method
    for row in range(BOARD_START_INDEX, BOARD_SIZE):
        for column in range(BOARD_START_INDEX, BOARD_SIZE):
            if (initialBoard[row][column] == NO_VALUE):
                for k in range(MIN_VALUE, MAX_VALUE + 1):
                    initialBoard[row][column] = k
                    if (isValidSudoku(initialBoard, row, column) and solve(initialBoard)):
                        return True
                    initialBoard[row][column] = NO_VALUE
                return False
    return True

def isValidSudoku(initialBoard,  row,  column): #Given method
	return isValidBoard(initialBoard) and isValidColumn(initialBoard, column) and isValidRow(initialBoard, row)
	
def isValidBoard(initialBoard):
    for i in range (BOARD_SIZE):
        if (not isValidRow(initialBoard, i) or not isValidColumn(initialBoard, i) or not isValidSubgrid(initialBoard, i)):
            return False
    return True

def isValidRow(initialBoard, row):
    seen = [False] * (BOARD_SIZE + 1)
    for val in initialBoard[row]:
        if val != 0 and seen[val]:
            return False
        seen[val] = True
    return True

def isValidColumn(initialBoard, col):
    seen = [False] * (BOARD_SIZE + 1)
    for i in range(BOARD_SIZE):
        val = initialBoard[i][col]
        if val != 0 and seen[val]:
            return False
        seen[val] = True
    return True

def isValidSubgrid(initialBoard, index):
    seen = [False] * (BOARD_SIZE + 1)
    row = (index // SUBSECTION_SIZE) * SUBSECTION_SIZE
    col = (index % SUBSECTION_SIZE) * SUBSECTION_SIZE
    
    for i in range(SUBSECTION_SIZE):
        for j in range(SUBSECTION_SIZE):        
            val = initialBoard[row + i][col + j]
            if val != 0 and seen[val]:
                return False
            seen[val] = True
    return True

def generateRandomCells(initialBoard, boardToBeSolved, numEmptyCells):
    emptyCellsGenerated = 0
    while emptyCellsGenerated < numEmptyCells:
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        randomInt = random.randint(MIN_VALUE, MAX_VALUE)

        if (initialBoard[x][y] == 0 and randomInt != 0):
            initialBoard[x][y] = randomInt
            boardToBeSolved[x][y] = randomInt
            emptyCellsGenerated += 1
        else:
            continue
        
def GenerateSudokuWithEmptyCells( X,  N):
    numEmptyCells = (BOARD_SIZE * BOARD_SIZE) - X
    countInvalid = 0
    countUnsolvable = 0

    for i in range(N):
    	#declare the arrays
        initialBoard = [[0] * 9 for _ in range(9)]
        boardTobeSolved = [[0] * 9 for _ in range(9)]

        isSolvable = True
        isValid = False

        while (not isValid or not isSolvable):
            generateRandomCells(initialBoard, boardTobeSolved, numEmptyCells)
            isValid = isValidBoard(boardTobeSolved)
            if (not isValid):
                countInvalid  += 1
            else:
                isSolvable = solve(initialBoard)
                if (not isSolvable):
                    countUnsolvable += 1
        print("Board #" + (i + 1)) #print a message
        printBoard(boardTobeSolved)
        print("Solution of the Board #" + (i + 1)) #print the initialBoard
        printBoard(initialBoard)
    printResults(X, N, countInvalid, countUnsolvable)
    

	
def printResults(X,  N,  countInvalid,  countUnsolvable):
	# Display the results
	print("Empty cells per board     : ", X)
	print("Valid boards created      : ", N)
	print("Invalid boards created    : ", countInvalid)
	print("Unsolvable boards created : ", countUnsolvable)

GenerateSudokuWithEmptyCells(60, 2) #My method to solve the Sudoku