# RandomAI.py
# Contains the methods with respect to the random AI for the chess game.
# Carter Kruse (October 5, 2023)

import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)

        # sleep(1) # I'm thinking so hard.
        print("Random AI Recommended Move: " + str(move))

        return move
