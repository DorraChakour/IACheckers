import random
from board import Board
from constants import WHITE

class Naif:
    def __init__(self, color):
        """
        Initialise l'IA naïf avec une couleur (BLACK ou WHITE)
        """
        self.color = color

    def get_move(self, board):
        """
        Retourne un mouvement, en priorisant les prises dans la rangée devant
        """
        valid_moves = self.get_all_valid_moves(board)
        if not valid_moves:
            return None
        captures = [m for m in valid_moves if (len(m) == 5)]
        simple_moves = [m for m in valid_moves if (len(m) == 4)]
        if captures:
            return random.choice(captures)
        return random.choice(simple_moves)

    def get_rafle_move(self, piece, board, next_captures):
        # next_captures est une liste de mouvements de type (start_row, start_col, end_row, end_col, captured)
        if not next_captures:
            return None
        return random.choice(next_captures)

    def get_all_valid_moves(self, board):
        """
        Retourne tous les mouvements valides possibles pour l'IA
        """
        valid_moves = []
        
        # Parcourir toutes les pièces du plateau
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.board[row][col]
                
                # Si la pièce appartient à l'IA
                if piece != 0 and piece.color == self.color:
                    # Récupérer les mouvements possibles pour cette pièce
                    moves = self.get_piece_moves(board, piece)
                    valid_moves.extend(moves)
                    
        return valid_moves

    def get_piece_moves(self, board, piece):
        """
        Retourne tous les mouvements possibles pour une pièce donnée
        """
        moves = []
        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.king:
            for drow, dcol in directions:
                r, c = piece.row, piece.col
                found_opponent = False
                while True:
                    r += drow
                    c += dcol
                    if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]):
                        if board.board[r][c] == 0:
                            if found_opponent:
                                captures.append((piece.row, piece.col, r, c, (r - drow, c - dcol)))
                                break  # On ne peut pas sauter plus loin
                            else:
                                moves.append((piece.row, piece.col, r, c))
                        elif board.board[r][c] != 0 and board.board[r][c].color != piece.color and not found_opponent:
                            found_opponent = True
                        else:
                            break
                    else:
                        break
        else:
            for drow, dcol in directions:
                new_row = piece.row + drow
                new_col = piece.col + dcol
                if 0 <= new_row < len(board.board) and 0 <= new_col < len(board.board[0]):
                    if board.board[new_row][new_col] == 0 and drow == (1 if piece.color == WHITE else -1):
                        moves.append((piece.row, piece.col, new_row, new_col))
                    jump_row = piece.row + 2 * drow
                    jump_col = piece.col + 2 * dcol
                    if 0 <= jump_row < len(board.board) and 0 <= jump_col < len(board.board[0]):
                        if board.board[jump_row][jump_col] == 0:
                            middle_row = piece.row + drow
                            middle_col = piece.col + dcol
                            if (board.board[middle_row][middle_col] != 0 and 
                                board.board[middle_row][middle_col].color != piece.color):
                                captures.append((piece.row, piece.col, jump_row, jump_col, (middle_row, middle_col)))
        return captures if captures else moves 