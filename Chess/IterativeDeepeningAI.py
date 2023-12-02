# IterativeDeepeningAI.py
# Contains the methods with respect to the iterative deepening AI for the chess game.
# Carter Kruse (October 5, 2023)

import chess
import random

class IterativeDeepeningAI():
    # Constructor
    def __init__(self, depth):
        self.depth = depth
        self.moves = 0
        self.calls = 0
    
    # Applying the minimax algorithm to the board and displaying the recommended move.
    def choose_move(self, board):
        move = self.iterative_deepening(board)
        print("Iterative Deepening AI Recommended Move: " + str(move) + " (Moves: " + str(self.moves) + ", Calls: " + str(self.calls) + ", Max Depth: " + str(self.depth) + ")")
        return move
    
    # Algorithm
    def iterative_deepening(self, board):
        # Set the current depth and value equal to 0.
        current_depth = 0
        current_value = 0

        # Determine the set of legal moves from the board, and shuffle for randomization.
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Set the best value equal to the boundary, and the best move equal to a random move.
        best_value = float('-inf') if board.turn == chess.WHITE else float('inf')
        best_move = moves[0]

        # Set the maximum depth equal to the instance variable.
        max_depth = 1

        # Make a copy of the board for resetting.
        copy_of_board = board

        # Iterative Deepening - Max Depth
        while max_depth <= self.depth:
            board = copy_of_board

            # Update the number of iterative deepening moves.
            self.moves += 1

            # Cycle through the possible legal moves.
            for move in moves:
                # Update the state of the board.
                board.push(move)
                self.calls += 1
                
                # If the "new" turn is the white player, i.e. the move is the black player.
                if board.turn == chess.WHITE:
                    # Begin the recursive algorithm.
                    current_value = self.max_value(board, current_depth, max_depth)

                    # Check to see if the current value beats the best value.
                    if current_value < best_value:
                        # Update the variables accordingly.
                        best_value = current_value
                        best_move = move
                
                # Otherwise if the "new" turn is the black player, i.e. the move is the white player.
                else:
                    # Begin the recursive algorithm.
                    current_value = self.min_value(board, current_depth, max_depth)

                    # Check to see if the current value beats the best value.
                    if current_value > best_value:
                        # Update the variables accordingly.
                        best_value = current_value
                        best_move = move
                
                # Return the board to it's previous state.
                board.pop()
            
            max_depth += 1
        
        return best_move
    
    # Max Value
    def max_value(self, board, current_depth, max_depth):
        # Check if the cutoff conditions are satisfied.
        if self.cutoff_test(board, current_depth, max_depth):
            # Return the "utility" of the board position.
            return self.utility(board)
        
        # Determine the set of legal moves from the board, and shuffle for randomization.
        value = float('-inf')
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Cycle through the possible legal moves, and apply the recursive algorithm.
        for move in moves:
            board.push(move)
            self.calls += 1
            value = max(value, self.min_value(board, current_depth + 1, max_depth))
            board.pop()
        
        return value
    
    # Min Value
    def min_value(self, board, current_depth, max_depth):
        # Check if the cutoff conditions are satisfied.
        if self.cutoff_test(board, current_depth, max_depth):
            # Return the "utility" of the board position.
            return self.utility(board)
        
        # Determine the set of legal moves from the board, and shuffle for randomization.
        value = float('inf')
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Cycle through the possible legal moves, and apply the recursive algorithm.
        for move in moves:
            board.push(move)
            self.calls += 1
            value = min(value, self.max_value(board, current_depth + 1, max_depth))
            board.pop()
        
        return value
    
    # Cutoff Test
    def cutoff_test(self, board, current_depth, max_depth):
        # The search stops if we have reached a terminal state (win/draw)
            # OR we have reached the specified maximum depth.
        if board.is_checkmate() or board.is_stalemate() or current_depth >= max_depth:
            return True
        return False
    
    # Utility (Board State)
    def utility(self, board):
        if board.is_checkmate():
            # Check if checkmate is against the white player.
            if board.turn == chess.WHITE:
                return float('-inf')
            
            # Check if checkmate is against the white player.
            else:
                return float('inf')
        
        elif board.is_stalemate():
            return 0
        
        else:
            return float(self.evaluate(board))
    
    # Evaluate
    def evaluate(self, board):
        white_pawn, black_pawn = len(board.pieces(chess.PAWN, chess.WHITE)), len(board.pieces(chess.PAWN, chess.BLACK))
        white_knight, black_knight = len(board.pieces(chess.KNIGHT, chess.WHITE)), len(board.pieces(chess.KNIGHT, chess.BLACK))
        white_bishop, black_bishop = len(board.pieces(chess.BISHOP, chess.WHITE)), len(board.pieces(chess.BISHOP, chess.BLACK))
        white_rook, black_rook = len(board.pieces(chess.ROOK, chess.WHITE)), len(board.pieces(chess.ROOK, chess.BLACK))
        white_queen, black_queen = len(board.pieces(chess.QUEEN, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))
        white_king, black_king = len(board.pieces(chess.KING, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))

        return (white_pawn - black_pawn) + (3 * (white_knight - black_knight)) + (3 * (white_bishop - black_bishop)) + \
            (5 * (white_rook - black_rook)) + (9 * (white_queen - black_queen)) + (200 * (white_king - black_king))
    