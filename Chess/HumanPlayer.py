# HumanPlayer.py
# Contains the methods with respect to the human player for the chess game.
# Carter Kruse (October 5, 2023)

import chess

class HumanPlayer():
    def __init__(self):
        print("Moves can be entered using four characters. For example, d2d4 moves the piece at d2 to d4.")
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)

        uci_move = None

        while not uci_move in moves:
            print("Please enter your move: ")
            human_move = input()

            try:
                uci_move = chess.Move.from_uci(human_move)
            except:
                # Illegal Move Format
                uci_move = None

            if uci_move not in moves:
                print("-- That is not a legal move!\n")
        
        print(uci_move in moves)

        return uci_move
    