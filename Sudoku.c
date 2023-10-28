#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define BOARD_SIZE 9
#define SUBSECTION_SIZE 3
#define BOARD_START_INDEX 0
#define NO_VALUE 0
#define MIN_VALUE 1
#define MAX_VALUE 9

void printBoard(int brd[BOARD_SIZE][BOARD_SIZE]);

int isValidSudoku(int initialBoard[BOARD_SIZE][BOARD_SIZE], int row, int column);

int isValidBoard(int initialBoard[BOARD_SIZE][BOARD_SIZE]);

int isValidRow(int initialBoard[BOARD_SIZE][BOARD_SIZE], int row);

int isValidColumn(int initialBoard[BOARD_SIZE][BOARD_SIZE], int col);

int isValidSubgrid(int initialBoard[BOARD_SIZE][BOARD_SIZE], int index);

void initializeBoard(int board[BOARD_SIZE][BOARD_SIZE]);

void generateRandomCells(int initialBoard[BOARD_SIZE][BOARD_SIZE], int boardToBeSolved[BOARD_SIZE][BOARD_SIZE], int numEmptyCells);

bool solve(int initialBoard[BOARD_SIZE][BOARD_SIZE]);

void GenerateSudokuWithEmptyCells(int X, int N);

void printResults(int X, int N, int countInvalid, int countUnsolvable, float clocktime);

int main() {
    GenerateSudokuWithEmptyCells(60, 10);
    return 0;
}

void printBoard(int brd[BOARD_SIZE][BOARD_SIZE]) {
    for (int row = BOARD_START_INDEX; row < BOARD_SIZE; row++) {
        for (int column = BOARD_START_INDEX; column < BOARD_SIZE; column++) {
            printf("%d ", brd[row][column]);
        }
        printf("\n");
    }
}

int isValidSudoku(int initialBoard[BOARD_SIZE][BOARD_SIZE], int row, int column) {
    return isValidBoard(initialBoard) && isValidColumn(initialBoard, column) && isValidRow(initialBoard, row);
}

int isValidBoard(int initialBoard[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        if (!isValidRow(initialBoard, i) || !isValidColumn(initialBoard, i) || !isValidSubgrid(initialBoard, i)) {
            return 0; // False
        }
    }
    return 1; // True
}

int isValidRow(int initialBoard[BOARD_SIZE][BOARD_SIZE], int row) {
    int seen[BOARD_SIZE + 1] = {0};
    for (int j = 0; j < BOARD_SIZE; j++) {
        int val = initialBoard[row][j];
        if (val != 0 && seen[val]) {
            return 0; // False
        }
        seen[val] = 1;
    }
    return 1; // True
}

int isValidColumn(int initialBoard[BOARD_SIZE][BOARD_SIZE], int col) {
    int seen[BOARD_SIZE + 1] = {0};
    for (int i = 0; i < BOARD_SIZE; i++) {
        int val = initialBoard[i][col];
        if (val != 0 && seen[val]) {
            return 0; // False
        }
        seen[val] = 1;
    }
    return 1; // True
}

int isValidSubgrid(int initialBoard[BOARD_SIZE][BOARD_SIZE], int index) {
    int seen[BOARD_SIZE + 1] = {0};
    int row = (index / SUBSECTION_SIZE) * SUBSECTION_SIZE;
    int col = (index % SUBSECTION_SIZE) * SUBSECTION_SIZE;

    for (int i = 0; i < SUBSECTION_SIZE; i++) {
        for (int j = 0; j < SUBSECTION_SIZE; j++) {
            int val = initialBoard[row + i][col + j];
            if (val != 0 && seen[val]) {
                return 0; // False
            }
            seen[val] = 1;
        }
    }
    return 1; // True
}

void initializeBoard(int board[BOARD_SIZE][BOARD_SIZE]) {
    for (int k = 0; k < BOARD_SIZE; k++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[k][j] = 0;
        }
    }
}

void generateRandomCells(int initialBoard[BOARD_SIZE][BOARD_SIZE], int boardToBeSolved[BOARD_SIZE][BOARD_SIZE], int numEmptyCells) {
    int emptyCellsGenerated = 0;
    srand(time(NULL));

    while (emptyCellsGenerated < numEmptyCells) {
        int x = rand() % (BOARD_SIZE - 1);
        int y = rand() % (BOARD_SIZE - 1);
        int randomInt = rand() % (MAX_VALUE - MIN_VALUE + 1) + MIN_VALUE;

        if (initialBoard[x][y] == 0 && randomInt != 0) {
            initialBoard[x][y] = randomInt;
            boardToBeSolved[x][y] = randomInt;
            emptyCellsGenerated++;
        }
    }
}

bool solve(int initialBoard[BOARD_SIZE][BOARD_SIZE]) {
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

void GenerateSudokuWithEmptyCells(int X, int N) {
    int numEmptyCells = (BOARD_SIZE * BOARD_SIZE) - X;
    int countInvalid = 0;
    int countUnsolvable = 0;
    clock_t startClock = clock(); // Start the time clock

    for (int i = 0; i < N; i++) {
        // Declare the arrays
        int initialBoard[BOARD_SIZE][BOARD_SIZE];
        int boardTobeSolved[BOARD_SIZE][BOARD_SIZE];

        bool isSolvable = true;
        bool isValid = false;

        while (!isValid || !isSolvable) {
            initializeBoard(initialBoard);
            initializeBoard(boardTobeSolved);
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
        printf("Board #%d\n", (i + 1));
        printBoard(boardTobeSolved);
        printf("Solution of the Board #%d\n", (i + 1));
        printBoard(initialBoard);
    }
    clock_t endClock = clock(); // End the time clock
    float clocktime = (float)(endClock - startClock) / CLOCKS_PER_SEC; // Calculate the time
    printResults(X, N, countInvalid, countUnsolvable, clocktime);
}

void printResults(int X, int N, int countInvalid, int countUnsolvable, float clocktime) {
    // Display the results
    printf("Empty cells per board     : %d\n", X);
    printf("Valid boards created      : %d\n", N);
    printf("Invalid boards created    : %d\n", countInvalid);
    printf("Unsolvable boards created : %d\n", countUnsolvable);
    printf("Elapsed time in seconds   : %.2f\n", clocktime);
}
