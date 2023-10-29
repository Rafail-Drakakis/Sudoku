import java.util.Random;
import java.util.stream.IntStream;
import java.util.Scanner;

public class Sudoku {
//Given code (constants)

	private static final int BOARD_SIZE = 9;
	private static final int SUBSECTION_SIZE = 3;
	private static final int BOARD_START_INDEX = 0;

	private static final int NO_VALUE = 0;
	private static final int MIN_VALUE = 1;
	private static final int MAX_VALUE = 9;

//main method (changed the name of the method from solve to GenerateSudokuWithEmptyCells)
	public static void main(String[] args) {
        Sudoku solver = new Sudoku();
        Scanner scanner = new Scanner(System.in);

        int choice;
        System.out.println("Sudoku Menu:");
        System.out.println("1. Create a random board with several empty cells");
        System.out.println("2. Check if Sudoku has a solution");
        System.out.println("3. Solve a Sudoku");
        System.out.println("4. Exit");
        System.out.print("Enter your choice (1/2/3/4): ");
            
        if (scanner.hasNextInt()) {
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
			        System.out.print("Enter the number of empty cells (X): ");
			        int X = scanner.nextInt();
			        System.out.print("Enter the number of boards to generate (N): ");
			        int N = scanner.nextInt();
                    // Create a random board with several empty cells
                    solver.GenerateSudokuWithEmptyCells(X,N);
                    break;
                case 2:
                    // Check if Sudoku has a solution
                    System.out.println("Enter the Sudoku puzzle to check for a solution:");
                    int[][] puzzleToCheck = readSudokuInput(scanner);
                    boolean hasSolution = solver.solve(puzzleToCheck);
                    if (hasSolution) {
                        System.out.println("The Sudoku puzzle has a solution.");
                    } else {
                        System.out.println("The Sudoku puzzle does not have a solution.");
                    }
                    break;
                case 3:
                    // Solve a Sudoku
                    System.out.println("Enter the Sudoku puzzle to solve:");
                    int[][] puzzleToSolve = readSudokuInput(scanner);
                    boolean solved = solver.solve(puzzleToSolve);
                    if (solved) {
                        System.out.println("Solved Sudoku:");
                        solver.printBoard(puzzleToSolve);
                    } else {
                        System.out.println("No solution found for the Sudoku puzzle.");
                    }
                    break;
                case 4:
                    System.out.println("Exiting the program.");
                	System.exit(0);
                default:
                    System.out.println("Invalid choice");
                	System.exit(0);
            }
        }
    }

    private static int[][] readSudokuInput(Scanner scanner) {
        int[][] puzzle = new int[BOARD_SIZE][BOARD_SIZE];
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (scanner.hasNextInt()) {
                    puzzle[i][j] = scanner.nextInt();
                } else {
                    System.out.println("Invalid input. Please enter valid numbers.");
                    scanner.next(); // Consume invalid input
                    i = BOARD_SIZE; // Exit outer loop
                    break;
                }
            }
        }
        return puzzle;
    }

	private void printBoard(int [][] brd) { //Given method
		for (int row = BOARD_START_INDEX; row < BOARD_SIZE; row++) {
			for (int column = BOARD_START_INDEX; column < BOARD_SIZE; column++) {
				System.out.print(brd[row][column] + " ");
			}
			System.out.println();
		}
	}

	private boolean solve(int[][] initialBoard) { //Given method
		for (int row = BOARD_START_INDEX; row < BOARD_SIZE; row++) {
			for (int column = BOARD_START_INDEX; column < BOARD_SIZE; column++) {
				if (initialBoard[row][column] == NO_VALUE) {
					for (int k = MIN_VALUE; k <= MAX_VALUE; k++) {
						initialBoard[row][column] = k;
						if (isValidSudoku(initialBoard, row, column) && solve(initialBoard)) {
							return true;
						}
						initialBoard[row][column] = NO_VALUE;
					}
					return false;
				}
			}
		}
		return true;
	}

	private boolean isValidSudoku(int[][] initialBoard, int row, int column) { //Given method
		return isValidBoard(initialBoard) && isValidColumn(initialBoard, column) && isValidRow(initialBoard, row);
	}

	private boolean isValidBoard(int[][] initialBoard) {
	    for (int i = 0; i < BOARD_SIZE; i++) {
	        if (!isValidRow(initialBoard, i) || !isValidColumn(initialBoard, i) || !isValidSubgrid(initialBoard, i)) {
	            return false;
	        }
	    }
	    return true;
	}

	private boolean isValidRow(int[][] initialBoard, int row) {
	    boolean[] seen = new boolean[BOARD_SIZE + 1];
	    for (int val : initialBoard[row]) {
	        if (val != 0 && seen[val]) {
	            return false;
	        }
	        seen[val] = true;
	    }
	    return true;
	}

	private boolean isValidColumn(int[][] initialBoard, int col) {
	    boolean[] seen = new boolean[BOARD_SIZE + 1];
	    for (int i = 0; i < BOARD_SIZE; i++) {
	        int val = initialBoard[i][col];
	        if (val != 0 && seen[val]) {
	            return false;
	        }
	        seen[val] = true;
	    }
	    return true;
	}

	private boolean isValidSubgrid(int[][] initialBoard, int index) {
	    boolean[] seen = new boolean[BOARD_SIZE + 1];
	    int row = (index / SUBSECTION_SIZE) * SUBSECTION_SIZE;
	    int col = (index % SUBSECTION_SIZE) * SUBSECTION_SIZE;
	    
	    for (int i = 0; i < SUBSECTION_SIZE; i++) {
	        for (int j = 0; j < SUBSECTION_SIZE; j++) {
	            int val = initialBoard[row + i][col + j];
	            if (val != 0 && seen[val]) {
	                return false;
	            }
	            seen[val] = true;
	        }
	    }
	    return true;
	}

	public void initializeBoard(int[][] board, int BOARD_SIZE) {
	    for (int k = 0; k < BOARD_SIZE; k++) {
	        for (int j = 0; j < BOARD_SIZE; j++) {
	            board[k][j] = 0;
	        }
	    }
	}

	public static void generateRandomCells(int[][] initialBoard, int[][] boardToBeSolved, int numEmptyCells) {
        int emptyCellsGenerated = 0;
        Random randomGenerator = new Random();

        while (emptyCellsGenerated < numEmptyCells) {
            int x = randomGenerator.nextInt(BOARD_SIZE - 1);
            int y = randomGenerator.nextInt(BOARD_SIZE - 1);
            int randomInt = randomGenerator.nextInt(MAX_VALUE - MIN_VALUE + 1) + MIN_VALUE;

            if (initialBoard[x][y] == 0 && randomInt != 0) {
                initialBoard[x][y] = randomInt;
                boardToBeSolved[x][y] = randomInt;
                emptyCellsGenerated++;
            } else {
                continue;
            }
        }
    }

	public void GenerateSudokuWithEmptyCells(int X, int N) {
	    int numEmptyCells = (BOARD_SIZE * BOARD_SIZE) - X;
	    int countInvalid = 0;
	    int countUnsolvable = 0;
	    long startClock = System.currentTimeMillis(); // Start the time clock

	    for (int i = 0; i < N; i++) { 
	    	//declare the arrays
	        int[][] initialBoard = new int[BOARD_SIZE][BOARD_SIZE];
	        int[][] boardTobeSolved = new int[BOARD_SIZE][BOARD_SIZE];

	        boolean isSolvable = true;
	        boolean isValid = false;

	        while (!isValid || !isSolvable) {
	            initializeBoard(initialBoard, BOARD_SIZE);
	            initializeBoard(boardTobeSolved, BOARD_SIZE);
	            generateRandomCells(initialBoard, boardTobeSolved, numEmptyCells);
				isValid = isValidBoard(boardTobeSolved);
	            if (!isValid) {
			        countInvalid++;
			    } else {
			        isSolvable = solve(initialBoard);
			        if (!isSolvable) {
			            countUnsolvable++;
			        }
			    }
	        }
			System.out.println("Board #" + (i + 1)); //print a message
		    printBoard(boardTobeSolved);
		    System.out.println("Solution of the Board #" + (i + 1)); //print the initialBoard
		    printBoard(initialBoard);
	    }
	    long endClock = System.currentTimeMillis(); // End the time clock
	    float clocktime = (endClock - startClock) / 1000F; // Calculate the time
	    printResults(X, N, countInvalid, countUnsolvable, clocktime);
	    
	}
	
	void printResults(int X, int N, int countInvalid, int countUnsolvable, float clocktime){
		// Display the results
	    System.out.println("Empty cells per board     : " + X);
	    System.out.println("Valid boards created      : " + N);
	    System.out.println("Invalid boards created    : " + countInvalid);
	    System.out.println("Unsolvable boards created : " + countUnsolvable);
	    System.out.println("Elapsed time in seconds   : " + clocktime);
	}
}