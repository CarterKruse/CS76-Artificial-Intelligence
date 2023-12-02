# AlphaBetaAI_Zobrist.py
# Contains the methods with respect to the alpha-beta AI for the chess game.
# Carter Kruse (October 5, 2023)

import chess
import random

class AlphaBetaAI_Zobrist():
    # Constructor
    def __init__(self, depth):
        self.depth = depth
        self.moves = 0
        self.calls = 0
        self.table = {}

        # Zobrist Hashing
        self.zobrist_table = {}
        
        # Enumerating the pieces in the chess match.
        pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

        # Enumerating the colors in the chess match.
        colors = [chess.WHITE, chess.BLACK]

        # Cycle through each of the colors, pieces, and squares on the chess board.
        for color in colors:
            for piece in pieces:
                for square in range(64):
                    self.zobrist_table[(color, piece, square)] = random.randint(0, 2**64 - 1)
    
    # Zobrist Hash (Algorithm)
        # XOR Hashes (Pieces On Squares)
    def zobrist_hash(self, board):
        hash = 0

        # Cycle through the squares on the chess board.
        for square in range(64):
            # Determine the piece at a particular square.
            piece = board.piece_at(square)
            
            # Updating the Zobrist hash according to the piece color, type, and location.
            if piece:
                hash ^= self.zobrist_table[(piece.color, piece.piece_type, square)]
            
            # Updating the Zobrist hash according to which player's turn it is.
            if board.turn == chess.BLACK:
                hash ^= 2**64 - 1

        return hash
    
    def lookup(self, board):
        return self.table[self.zobrist_hash(board)]
    
    def store(self, board, value):
        self.table[self.zobrist_hash(board)] = value

    # Applying the minimax algorithm to the board and displaying the recommended move.
    def choose_move(self, board):
        move = self.alpha_beta(board)
        print("Alpha-Beta AI Recommended Move: " + str(move) + " (Moves: " + str(self.moves) + ", Calls: " + str(self.calls) + ", Max Depth: " + str(self.depth) + ")")
        return move
    
    # Algorithm
    def alpha_beta(self, board, alpha = float('-inf'), beta = float('inf')):
        # Set the current depth and value equal to 0.
        current_depth = 0
        current_value = 0

        # Determine the set of legal moves from the board, and shuffle for randomization.
        # moves = list(board.legal_moves)
        # random.shuffle(moves)

        moves = self.ordered_moves(board)

        # Set the best value equal to the boundary, and the best move equal to a random move.
        best_value = float('-inf') if board.turn == chess.WHITE else float('inf')
        best_move = moves[0]

        # Set the maximum depth equal to the instance variable.
        max_depth = self.depth

        # Update the number of alpha beta moves.
        self.moves += 1

        # Cycle through the possible legal moves.
        for move in moves:
            # Update the state of the board.
            board.push(move)
            self.calls += 1
            
            # If the "new" turn is the white player, i.e. the move is the black player.
            if board.turn == chess.WHITE:
                # Begin the recursive algorithm.
                current_value = self.max_value(board, current_depth, max_depth, alpha, beta)

                # Check to see if the current value beats the best value.
                if current_value < best_value:
                    # Update the variables accordingly.
                    best_value = current_value
                    best_move = move
            
            # Otherwise if the "new" turn is the black player, i.e. the move is the white player.
            else:
                # Begin the recursive algorithm.
                current_value = self.min_value(board, current_depth, max_depth, alpha, beta)

                # Check to see if the current value beats the best value.
                if current_value > best_value:
                    # Update the variables accordingly.
                    best_value = current_value
                    best_move = move
            
            # Return the board to it's previous state.
            board.pop()
        
        return best_move
    
    # Max Value
    def max_value(self, board, current_depth, max_depth, alpha, beta):
        # Check if the cutoff conditions are satisfied.
        if self.cutoff_test(board, current_depth, max_depth):
            # Return the "utility" of the board position.
            return self.utility(board)
        
        # Return the value if we already know the result of the state.
        if hash(str(board)) in self.table:
            return self.lookup(board)
        
        # Determine the set of legal moves from the board, and shuffle for randomization.
        value = float('-inf')
        # moves = list(board.legal_moves)
        # random.shuffle(moves)

        moves = self.ordered_moves(board)

        # Cycle through the possible legal moves, and apply the recursive algorithm.
        for move in moves:
            board.push(move)
            self.calls += 1
            value = max(value, self.min_value(board, current_depth + 1, max_depth, alpha, beta))
            board.pop()

            # Pruning
            if value >= beta:
                self.store(board, value)
                return value
            
            # Updating the alpha value.
            alpha = max(alpha, value)
        
        self.store(board, value)
        return value
    
    # Min Value
    def min_value(self, board, current_depth, max_depth, alpha, beta):
        # Check if the cutoff conditions are satisfied.
        if self.cutoff_test(board, current_depth, max_depth):
            # Return the "utility" of the board position.
            return self.utility(board)
        
        # Return the value if we already know the result of the state.
        if hash(str(board)) in self.table:
            return self.lookup(board)
        
        # Determine the set of legal moves from the board, and shuffle for randomization.
        value = float('inf')
        # moves = list(board.legal_moves)
        # random.shuffle(moves)

        moves = self.ordered_moves(board)

        # Cycle through the possible legal moves, and apply the recursive algorithm.
        for move in moves:
            board.push(move)
            self.calls += 1
            value = min(value, self.max_value(board, current_depth + 1, max_depth, alpha, beta))
            board.pop()
        
            # Pruning
            if value <= alpha:
                self.store(board, value)
                return value
        
            # Updating the beta value.
            beta = min(beta, value)
        
        self.store(board, value)
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
    
    # Ordered Moves
    def ordered_moves(self, board):
        # Determine the set of legal moves/captures from the board.
        moves = list(board.legal_moves)
        captures = list(board.generate_legal_captures())

        # Create a list of "non-capture" moves that do not capture a piece.
        non_captures = []

        # Cycle through the moves to construct the list.
        for move in moves:
            if move not in captures:
                non_captures.append(move)
        
        # Randomize the lists separately to allow for unique movement.
        random.shuffle(captures)
        random.shuffle(non_captures)

        return captures + non_captures
        