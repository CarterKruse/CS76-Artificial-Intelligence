# test_chess.py
# A file to test the chess AI programs, which are designed to play the optimal moves.
# Includes: RandomAI, MinimaxAI, IterativeDeepeningAI, AlphaBetaAI, AlphaBetaAI_Transposition
# Carter Kruse (October 5, 2023)

# pip3 install python-chess

import chess
import sys

from HumanPlayer import HumanPlayer
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from MinimaxAI_Mobility import MinimaxAI_Mobility
from IterativeDeepeningAI import IterativeDeepeningAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAI_Transposition import AlphaBetaAI_Transposition
from AlphaBetaAI_Zobrist import AlphaBetaAI_Zobrist
from ChessGame import ChessGame

# player1 = HumanPlayer()
player1 = RandomAI()
# player1 = MinimaxAI(1)
# player1 = MinimaxAI_Mobility(2)
# player1 = IterativeDeepeningAI(2)
# player1 = AlphaBetaAI(2)
# player1 = AlphaBetaAI_Transposition(2)
# player1 = AlphaBetaAI_Zobrist(2)

# player2 = HumanPlayer()s
# player2 = RandomAI()
player2 = MinimaxAI(1)
# player2 = MinimaxAI_Mobility(2)
# player2 = IterativeDeepeningAI(2)
# player2 = AlphaBetaAI(2)
# player2 = AlphaBetaAI_Transposition(2)
# player2 = AlphaBetaAI_Zobrist(2)

# Initialize the chess game with the corresponding players.
game = ChessGame(player1, player2)

# Run the chess game, allowing for moves to be made.
while not game.is_game_over():
    print(game)
    game.make_move()

print()
print("WHITE - BLACK")
print(game.board.result())
print()

# print(hash(str(game.board)))
