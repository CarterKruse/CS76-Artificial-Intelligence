# ChessGame.py
# Contains the methods with respect to the chess game.
# Carter Kruse (October 5, 2023)

import chess
import time

class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):
        start = time.time()
        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)
        end = time.time()
        print('(Time: {:.3g} Seconds)'.format(end - start))
        
        self.board.push(move) # Make the move.
    
    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):
        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # Did you know Python has a ternary conditional operator?
        move_str = "White To Move" if self.board.turn else "Black To Move"

        return board_str + "\n" + move_str
    