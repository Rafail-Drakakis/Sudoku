import random

def sudoku_number_is_valid(board):
    """
    The function `sudoku_number_is_valid` checks if a given Sudoku board is valid by verifying that each row,
    column, and subgrid contains unique numbers from 1 to 9.
    
    :param board: The parameter "board" is a 2-dimensional list representing the Sudoku board. It should
    have 9 rows and 9 columns, where each element represents a number in the Sudoku puzzle. The numbers
    can be integers from 1 to 9, or 0 to represent an empty cell
    :return: The function sudoku_number_is_valid is returning a boolean value. It returns True if the given
    board is a valid Sudoku board, and False otherwise.
    """
    # Check rows
    for row in board:
        if not row_number_is_valid(row):
            return False

    # Check columns
    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if not row_number_is_valid(column):
            return False

    # Check subgrids
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            subgrid = [
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            ]
            if not row_number_is_valid(subgrid):
                return False

    return True

def row_number_is_valid(row):
    """
    The function checks if a given row in a Sudoku puzzle is valid, meaning it does not contain any
    duplicate numbers (except for zeros).
    
    :param row: The parameter `row` is a list representing a row in a Sudoku puzzle. Each element in the
    list represents a number in the row, with 0 indicating an empty cell
    :return: The function row_number_is_valid is returning a boolean value. It returns True if the row is
    valid, meaning it does not contain any duplicate non-zero numbers. It returns False if the row is
    invalid, meaning it contains at least one duplicate non-zero number.
    """
    seen = set()
    for num in row:
        if num != 0 and num in seen:
            return False
        seen.add(num)
    return True

def solve_sudoku(board):
    """
    The function `solve_sudoku` uses backtracking to solve a given Sudoku board.
    
    :param board: The "board" parameter is a 9x9 grid representing the Sudoku puzzle. It is a
    2-dimensional list where each element represents a cell in the grid. The value of each cell can be
    an integer from 1 to 9, or 0 if the cell is empty. The
    :return: The function `solve_sudoku` returns a boolean value. It returns `True` if the sudoku board
    is successfully solved, and `False` if it is not possible to solve the board.
    """
    if find_empty_cell(board) is None:
        return True

    row, col = find_empty_cell(board)
    numbers = list(range(1, 10))
    random.shuffle(numbers)  # Randomizing the order of numbers tried
    for num in numbers:
        if number_is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def number_is_valid(board, row, col, num):
    """
    The function checks if a given number is valid to be placed in a specific position on a Sudoku
    board.
    
    :param board: The board parameter is a 2-dimensional list representing the Sudoku board. It has 9
    rows and 9 columns. Each element in the list represents a number on the board. If a cell is empty,
    it is represented by 0
    :param row: The row parameter represents the row index of the cell we want to check in the Sudoku
    board. It is an integer value ranging from 0 to 8, where 0 represents the first row and 8 represents
    the last row
    :param col: The `col` parameter represents the column index of the cell in the Sudoku board that we
    want to check for validity
    :param num: The parameter "num" represents the number that we want to check for validity in the
    Sudoku board
    :return: The function number_is_valid is returning a boolean value. It returns True if the given number
    (num) is valid to be placed in the specified row and column of the Sudoku board, and False
    otherwise.
    """
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 subgrid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def find_empty_cell(board):
    """
    The function `find_empty_cell` takes a 9x9 board as input and returns the row and column indices of
    the first empty cell (with value 0) it encounters, or None if there are no empty cells.
    
    :param board: The parameter "board" is a 2-dimensional list representing a Sudoku board. Each
    element in the list represents a cell on the board, and its value can be either a number from 1 to 9
    or 0 if the cell is empty
    :return: the row and column indices of the first empty cell in the board. If there are no empty
    cells, it returns None.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def generate_sudoku(difficulty):
    """
    The function generates a Sudoku board of a specified difficulty level by first solving a complete
    Sudoku board and then removing a certain number of cells based on the difficulty level.
    
    :param difficulty: The difficulty parameter is used to determine how many cells should be removed
    from the solved Sudoku board to create the puzzle. It can be a value between 1 and 81, where a lower
    value represents a higher difficulty level
    :return: a Sudoku board with a specified difficulty level.
    """
    board = [[0] * 9 for _ in range(9)]
    
    # Randomly filling a few cells before solving
    for _ in range(random.randint(3, 5)):  
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if number_is_valid(board, row, col, num):
            board[row][col] = num
    
    solve_sudoku(board)
    remove_cells(board, difficulty)
    return board

def remove_cells(board, difficulty):
    """
    The function `remove_cells` takes a Sudoku board and a difficulty level as input, and removes cells
    from the board until the desired difficulty level is reached.
    
    :param board: The "board" parameter is a 2-dimensional list representing the Sudoku board. Each
    element in the list represents a cell on the board, with 0 indicating an empty cell and numbers 1-9
    indicating the value of the cell
    :param difficulty: The difficulty parameter represents the number of cells that should be removed
    from the board. The higher the difficulty, the more cells will be removed
    """
    cells_to_remove = 81 - difficulty

    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if board[row][col] != 0:
            backup = board[row][col]
            board[row][col] = 0

            temp_board = [row[:] for row in board]
            unique_solution = solve_sudoku(temp_board)

            if unique_solution:
                cells_to_remove -= 1
            else:
                board[row][col] = backup

def print_board(board):
    """
    The function `print_board` prints each row of a given board.
    
    :param board: The parameter "board" is a list of lists. Each inner list represents a row on the game
    board
    """
    for row in board:
        print(row)

def input_array():
    """
    The function `input_array` prompts the user to input a 9x9 array of integers for a Sudoku puzzle and
    returns the array as a NumPy array.
    :return: a NumPy array containing the elements entered by the user for each row of a Sudoku puzzle.
    """
    num_rows = 9  # Sudoku has 9 rows

    array = []
    for i in range(num_rows):
        while True:
            try:
                elements = input(f"Enter the elements for row {i + 1}, separated by spaces: ")
                elements = elements.split()
                elements = [int(element) for element in elements]
                if len(elements) != 9:  # Sudoku has 9 columns
                    raise ValueError("Invalid number of elements. Please enter 9 elements per row.")
                if any(element < 0 or element > 9 for element in elements):
                    raise ValueError("Invalid element value. Please enter values between 0 and 9.")
                array.append(elements)
                break
            except ValueError:
                print("Invalid input. Please enter integer values separated by spaces.")

    return array

def main():
    choice = int(input("Sudoku Solver, Checker, and Generator\nEnter\n1.To check if a given sudoku has solution\n2.To generate a random sudoku\n3.To solve a sudoku\n4.To generate a random sudoku and solve it: "))
    if choice not in [1,2,3,4]:
        print("invalid input")
        exit(0)

    if choice == 1:
        print("Enter the Sudoku puzzle:")
        board = input_array()
        if sudoku_number_is_valid(board):
            print("\nThe Sudoku board is valid.")
        else:
            print("\nThe Sudoku board is invalid.")
    elif choice == 2:
        print("Sudoku Generator")
        difficulty_level = int(input("Enter the number of non-zero elements for the generated Sudoku board: "))
        print("Generating a Sudoku board:")
        sudoku_board = generate_sudoku(difficulty_level)
        print_board(sudoku_board)
    elif choice == 3:
        print("Enter the Sudoku puzzle to solve:")
        puzzle = input_array()
        print("Original puzzle:")
        print_board(puzzle)
        if solve_sudoku(puzzle):
            print("\nSolution:")
            print_board(puzzle)
        else:
            print("\nNo solution exists for the puzzle.")
    elif choice == 4:
        difficulty_level = int(input("Enter the number of non-zero elements for the generated Sudoku board: "))
        sudoku_board = generate_sudoku(difficulty_level)
        print("\nOriginal:")
        print_board(sudoku_board)

        if solve_sudoku(sudoku_board):
            print("\nSolution:")
            print_board(sudoku_board)
        else:
            print("\nNo solution exists for the puzzle.")

if __name__ == "__main__":
    main()