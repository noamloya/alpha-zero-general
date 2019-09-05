'''
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
import numpy as np

# from bkcharts.attributes import color
class Board():
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, n, winning_amount, forbidden_moves):
        "Set up initial board configuration."

        self.n = n
        self.winning_amount = winning_amount
        self.forbidden_moves = forbidden_moves
        # Create the empty board array.
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n
            for j in range(n):
                if forbidden_moves[i][j] == 1:
                    self.pieces[i][j] = np.nan
    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def is_legal_move(self, x, y):
        return self[x][y] == 0 and (x,y) and self.forbidden_moves[x][y] == 0

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self.is_legal_move(x, y):
                    newmove = (x, y)
                    moves.add(newmove)
        return list(moves)

    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self.is_legal_move(x, y):
                    return True
        return False

    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        win = self.winning_amount
        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
                else:
                    count = 0
                if count == win:
                    return True
        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                if self[x][y] == color:
                    count += 1
                else:
                    count = 0
                if count == win:
                    return True
        # check two diagonal strips
        count = 0
        for d in range(self.n):
            if self[d][d] == color:
                count += 1
            else:
                count = 0
            if count == win:
                return True
        count = 0
        for d in range(self.n):
            if self[d][self.n - d - 1] == color:
                count += 1
            else:
                count = 0
            if count == win:
                return True

        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x, y) = move

        # Add the piece to the empty square.
        assert self[x][y] == 0
        self[x][y] = color
