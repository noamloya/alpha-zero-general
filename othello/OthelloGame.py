from __future__ import print_function
import sys

sys.path.append('..')
from Game import Game
from .OthelloLogic import Board
import numpy as np


class OthelloGame(Game):
    def __init__(self, n, forbidden_moves=None):
        self.n = n
        if forbidden_moves is not None:
            self.forbidden_moves = forbidden_moves
        else:
            self.forbidden_moves = np.zeros((n, n))
        self.symmetry_indices = self.get_symmetry_indices()

    def get_symmetry_indices(self):
        indices = []
        forbidden_symmetry = np.copy(self.forbidden_moves)
        for i in range(1, 5):
            for j in [True, False]:
                forbidden_symmetry = np.rot90(forbidden_symmetry)
                if j:
                    forbidden_symmetry = np.fliplr(forbidden_symmetry)
                if np.all(np.equal(forbidden_symmetry, self.forbidden_moves)):
                    indices.append((i, j))
        return indices

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n, self.forbidden_moves)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return (board, -player)
        b = Board(self.n, self.forbidden_moves)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.n, self.forbidden_moves)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        b = Board(self.n, self.forbidden_moves)

        b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if b.countDiff(player) > 0:
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == self.n ** 2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        if not self.symmetry_indices:
            return [(board, pi)]

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                if (i, j) in self.symmetry_indices:
                    l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def getScore(self, board, player):
        b = Board(self.n, self.forbidden_moves)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    def display(self, board):
        board = board.astype(float)
        board[self.forbidden_moves == 1] = np.nan

        n = board.shape[0]

        for y in range(n):
            print(y, "|", end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(y, "|", end="")  # print the row #
            for x in range(n):
                piece = board[y][x]  # get the piece to print
                if np.isnan(piece):
                    print("/ ", end="")
                elif piece == -1:
                    print("b ", end="")
                elif piece == 1:
                    print("W ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")

        print("   -----------------------")
