#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 9

// Function to print the Sudoku board
void print_board(int board[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            printf("%d ", board[row][col]);
        }
        printf("\n");
    }
}

// Function to check if a number is valid in a given position
int is_valid(int board[SIZE][SIZE], int row, int col, int num) {
    // Check row
    for (int x = 0; x < SIZE; x++) {
        if (board[row][x] == num) {
            return 0;
        }
    }

    // Check column
    for (int x = 0; x < SIZE; x++) {
        if (board[x][col] == num) {
            return 0;
        }
    }

    // Check 3x3 square
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i + startRow][j + startCol] == num) {
                return 0;
            }
        }
    }

    return 1;
}

// Function to solve the Sudoku using backtracking
int solve_sudoku(int board[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if (board[row][col] == 0) {
                for (int num = 1; num <= 9; num++) {
                    if (is_valid(board, row, col, num)) {
                        board[row][col] = num;

                        if (solve_sudoku(board)) {
                            return 1;
                        }

                        board[row][col] = 0;
                    }
                }
                return 0;
            }
        }
    }
    return 1;
}

void removeCells(int board[SIZE][SIZE], int cellsToRemove) {
    int row, col;
    
    srand(time(0)); // Seed for random numbers
    
    while (cellsToRemove > 0) {
        row = rand() % SIZE;
        col = rand() % SIZE;
        
        if (board[row][col] != 0) {
            board[row][col] = 0;
            cellsToRemove--;
        }
    }
}

void generateSudoku(int board[SIZE][SIZE], int difficulty) {
    solve_sudoku(board);
    removeCells(board, 81 - difficulty);
}

void initialize_sudoku(int sudoku[SIZE][SIZE]) {
    for(int i = 0; i < SIZE; i++) {
        for(int j = 0; j < SIZE; j++) {
            sudoku[i][j] = 0;  // Assigning each element to 0 (empty)
        }
    }
}

int main() {
    int choice;

    printf("Sudoku Solver and Checker\n");
    printf("Enter 1 to solve a Sudoku\n");
    printf("Enter 2 to check if a Sudoku is valid\n");
    printf("Enter 3 to generate a Sudoku board\n");
    printf("Enter 4 to generate and solve a sudoku");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    int board[SIZE][SIZE];

    if (choice == 1 || choice == 2) {
        printf("Enter the Sudoku puzzle (use 0 for empty cells):\n");
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                scanf("%d", &board[row][col]);
            }
        }
    }

    if (choice == 1) {
        if (solve_sudoku(board)) {
            printf("Solved Sudoku:\n");
            print_board(board);
        } else {
            printf("No solution exists.\n");
        }
    } else if (choice == 2) {
        if (solve_sudoku(board)) {
            printf("The Sudoku puzzle is valid.\n");
        } else {
            printf("The Sudoku puzzle is invalid.\n");
        }
    } else if (choice == 3){
        initialize_sudoku(board);
        int difficulty;
        printf("Enter the number of non-zero elements for the generated Sudoku board: ");
        scanf("%d", &difficulty);
        
        generateSudoku(board, difficulty);
        print_board(board);
    } else if (choice == 4){
        initialize_sudoku(board);
        int difficulty;
        printf("Enter the number of non-zero elements for the generated Sudoku board: ");
        scanf("%d", &difficulty);
        generateSudoku(board, difficulty);
        printf("Solved Sudoku:\n");
        print_board(board);    
        if (solve_sudoku(board)) {
            printf("Solved Sudoku:\n");
            print_board(board);
        } else {
            printf("No solution exists.\n");
        }
    }

    else {
        printf("Invalid choice!\n");
    }

    return 0;
}