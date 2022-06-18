from __future__ import print_function
import numpy as np
from .GoLogic import GoBoard, PASS
from Game import Game
import sys
sys.path.append('..')


class GoGame(Game):

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = GoBoard(self.n)
        return b

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # if action == self.n*self.n:
        #    return (board, -player)
        b = board.copy()
        move = PASS if action == 0 else b.index_to_vertex(action-1)
        assert b.legal(move)
        b.play(move)
        return (b, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        valids[0] = 1  # PASS
        for i in range(self.n):
            for j in range(self.n):
                if board.legal(board.get_vertex(i, j)):
                    valids[board.get_index(i, j)+1] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        if board.num_passes >= 2:
            if board.final_score() > 0:
                return 1
            elif board.final_score() < 0:
                return -1
            else:
                return 1e-8
        else:
            return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        """
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l
        """
        return []

    def stringRepresentation(self, board):
        return board.get_features().tobytes()

    def stringRepresentationReadable(self, board):
        #board_s = "".join(self.square_content[square] for row in board for square in row)
        return board.__str__()

    def getScore(self, board, player):
        return board.final_score()

    @staticmethod
    def display(board):
        print(board)
