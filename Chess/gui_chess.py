# gui_chess.py
# A file to visualize the chess AI programs, which are designed to play the optimal moves.
# Includes: RandomAI, MinimaxAI, AlphaBetaAI, IterativeDeepeningAI
# Carter Kruse (October 5, 2023)

# brew install pyqt

from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget

import chess, chess.svg
import sys
import random

from HumanPlayer import HumanPlayer
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from IterativeDeepeningAI import IterativeDeepeningAI
from ChessGame import ChessGame

class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()
    
    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)
    
    def make_move(self):
        print("Making Move, White Turn " + str(self.game.board.turn))

        self.game.make_move()
        self.display_board()

        # print(game.board.result())

if __name__ == "__main__":
    random.seed(1)

    # To Do: GUI does not work well with HumanPlayer, due to input() use on stdin conflict with event loop.
    
    player1 = RandomAI()
    player2 = RandomAI()

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
