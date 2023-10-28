import random
import math
import numpy as np

BOARD_SIZE = 9
SUBSECTION_SIZE = 3
BOARD_START_INDEX = 0

NO_VALUE = 0
MIN_VALUE = 1
MAX_VALUE = 9

def printBoard(brd):
    for row in range(BOARD_START_INDEX, BOARD_SIZE):
        for column in range(BOARD_START_INDEX, BOARD_SIZE):
            print(brd[row][column], end=" ")
        print("")

def solve(initialBoard):
    for row in range(BOARD_START_INDEX, BOARD_SIZE):
        for column in range(BOARD_START_INDEX, BOARD_SIZE):
            if initialBoard[row][column] == NO_VALUE:
                for k in range(MIN_VALUE, MAX_VALUE + 1):
                    initialBoard[row][column] = k
                    if isValidSudoku(initialBoard, row, column) and solve(initialBoard):
                        return True
                    initialBoard[row][column] = NO_VALUE
                return False
    return True

def isValidSudoku(initialBoard, row, column):
    return isValidBoard(initialBoard) and isValidColumn(initialBoard, column) and isValidRow(initialBoard, row)

def isValidBoard(initialBoard):
    for i in range(BOARD_SIZE):
        if not (isValidRow(initialBoard, i) and isValidColumn(initialBoard, i) and isValidSubgrid(initialBoard, i)):
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
        if initialBoard[x][y] == 0:
            randomInt = random.randint(MIN_VALUE, MAX_VALUE)
            if isValidMove(boardToBeSolved, x, y, randomInt):
                initialBoard[x][y] = randomInt
                boardToBeSolved[x][y] = randomInt
                emptyCellsGenerated += 1

def isValidMove(board, row, col, num):
    for i in range(BOARD_SIZE):
        # Check if the number already exists in the same row or column
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check if the number already exists in the 3x3 subgrid
    subgrid_row, subgrid_col = row // SUBSECTION_SIZE, col // SUBSECTION_SIZE
    for i in range(subgrid_row * SUBSECTION_SIZE, (subgrid_row + 1) * SUBSECTION_SIZE):
        for j in range(subgrid_col * SUBSECTION_SIZE, (subgrid_col + 1) * SUBSECTION_SIZE):
            if board[i][j] == num:
                return False
    return True

def GenerateSudokuWithEmptyCells(X, N):
    numEmptyCells = (BOARD_SIZE * BOARD_SIZE) - X
    countInvalid = 0
    countUnsolvable = 0

    for i in range(N):
        # Declare the arrays
        initialBoard = [[0] * 9 for _ in range(9)]
        boardToBeSolved = [[0] * 9 for _ in range(9)]

        isSolvable = True
        isValid = False

        while not isValid or (not isSolvable and isValid):
            generateRandomCells(initialBoard, boardToBeSolved, numEmptyCells)
            isValid = isValidBoard(boardToBeSolved)
            if not isValid:
                countInvalid += 1
            else:
                isSolvable = solve(initialBoard)
                if not isSolvable:
                    countUnsolvable += 1
        print("Board #", (i + 1))  # Print a message
        printBoard(boardToBeSolved)
        print("Solution of Board #", (i + 1))  # Print the initialBoard
        printBoard(initialBoard)
    printResults(X, N, countInvalid, countUnsolvable)


def printResults(X, N, countInvalid, countUnsolvable):
    # Display the results
    print("Empty cells per board     :", X)
    print("Valid boards created      :", N)
    print("Invalid boards created    :", countInvalid)
    print("Unsolvable boards created :", countUnsolvable)

def input_array():
    array = []
    for i in range(9):
        try:
            elements = input(f"Enter the elements for row {i + 1}, separated by spaces: ")
            elements = elements.split()
            elements = [int(element) for element in elements]
            array.append(elements)
        except ValueError:
            print("Invalid input. Please enter integer values separated by spaces.")
    
    return np.array(array)

def main():
    while True:
        print("\nSudoku Menu:")
        print("1. Create a random Sudoku board with empty cells")
        print("2. Check if a Sudoku has a solution")
        print("3. Solve a Sudoku")
        print("4. Quit")
        
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == "1":
            X = int(input("Enter the number of empty cells: "))
            N = int(input("Enter the number of boards to generate: "))
            GenerateSudokuWithEmptyCells(X, N)
        elif choice == "2":
            boardToBeSolved = input_array()
            if solve(boardToBeSolved):
                print("This Sudoku has a solution!")
            else:
                print("This Sudoku does not have a solution.")
        elif choice == "3":
            boardToBeSolved = input_array()
            if solve(boardToBeSolved):
                print("Solved Sudoku:")
                printBoard(boardToBeSolved)
            else:
                print("This Sudoku does not have a solution.")
        elif choice == "4":
            print("Exiting the Sudoku solver. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2/3/4).")

if __name__ == "__main__":
    main()