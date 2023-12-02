# test_chess_openings.py
# A file to test the chess AI programs, which are designed to play the optimal moves.
# Includes: RandomAI, MinimaxAI, IterativeDeepeningAI, AlphaBetaAI, AlphaBetaAI_Transposition
# Carter Kruse (October 5, 2023)

# pip3 install python-chess

import chess
import sys
import time
import random

from HumanPlayer import HumanPlayer
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from IterativeDeepeningAI import IterativeDeepeningAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAI_Transposition import AlphaBetaAI_Transposition
from AlphaBetaAI_Zobrist import AlphaBetaAI_Zobrist
from ChessGame import ChessGame

# player1 = HumanPlayer()
player1 = RandomAI()
# player1 = MinimaxAI(2)
# player1 = IterativeDeepeningAI(2)
# player1 = AlphaBetaAI(2)
# player1 = AlphaBetaAI_Transposition(2)
# player1 = AlphaBetaAI_Zobrist(2)

# player2 = HumanPlayer()s
# player2 = RandomAI()
# player2 = MinimaxAI(1)
# player2 = IterativeDeepeningAI(2)
# player2 = AlphaBetaAI(2)
# player2 = AlphaBetaAI_Transposition(2)
player2 = AlphaBetaAI_Zobrist(2)

# Initialize the chess game with the corresponding players.
game = ChessGame(player1, player2)
print(game)

# List out all of the openings.
opening_book = {'vienna_game': ['e2e4', 'e7e5', 'b1c3'],
                 'scotch_game': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'd2d4'],
                 'italian_game': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3'],
                 'ruy_lopez': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'a7a6'],
                 'sicilian_defense': ['e2e4', 'c7c5'],
                 'french_defense': ['e2e4', 'e7e6'],
                 'caro-kann_defense': ['e2e4', 'c7c6'],
                 'pirc_defense': ['e2e4', 'd7d6', 'g1f3', 'g8f6'],
                 'queens_gambit': ['d2d4', 'd7d5', 'c2c4'],
                 'slav_defense': ['d2d4', 'd7d5', 'c2c4', 'c7c6'],
                 'kings_indian_defense': ['d2d4', 'g8f6', 'c2c4', 'g7g6'],
                 'grunfeld_defense': ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'd7d5'],
                 'english_opening': ['c2c4'],
                 'reti_opening': ['g1f3'],
                 'giuoco_piano': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'g8f6', 'd2d4', 'e5d4', 'f3d4', 'b7b5'],
                 'two_knights_defense': ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'g8f6', 'g2g4'],
                 'queens_gambit_declined': ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'c4d5', 'f6e4'],
                 'sicilian_najdorf': ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'a7a6']
                 }

# # # # # # # # # #

# UNCOMMENT
# # Choose a random opening.
# opening_name = random.choice(list(opening_book.keys()))

# # Run the opening book, keeping track of how long it takes (short!).
# start = time.time()
# for move in opening_book[opening_name]:
#     game.board.push(chess.Move.from_uci(move))
# end = time.time()

# # Provide the name of the opening book, along with the total time taken and result.
# print("Opening Book: " + opening_name)
# print('(Time: {:.3g} Seconds)'.format(end - start))
# print(game)

# # Run the chess game, allowing for moves to be made.
# while not game.is_game_over():
#     print(game)
#     game.make_move()

# print()
# print("WHITE - BLACK")
# print(game.board.result())
# print()

# # print(hash(str(game.board)))

# # # # # # # # # #

# Cycle through all of the openings in the opening book to demonstrate.
for opening_name in list(opening_book.keys()):
    # Run the opening book, keeping track of how long it takes (short!).
    start = time.time()
    for move in opening_book[opening_name]:
        game.board.push(chess.Move.from_uci(move))
    end = time.time()

    # Provide the name of the opening book, along with the total time taken and result.
    print("Opening Book: " + opening_name)
    print('(Time: {:.3g} Seconds)'.format(end - start))

    # Ensure that the next opening book starts with the white player.
    game.board.turn = chess.WHITE
    print(game)

    # Reset the chess board.
    game.board.reset()
