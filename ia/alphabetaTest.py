import copy
import time
from math import inf
from constants import WHITE, BLACK
from ia.naif import Naif

class MinimaxAlphaBetaTest:
    PIECE_VAL = 10
    KING_VAL = 50
    CAPTURE_BONUS = 100
    THREAT_BONUS = 50
    MOBILITY_BONUS = 5
    ADVANCE_BONUS = 3

    def __init__(self, color, depth):
        self.color = color
        self.depth = depth
        self.naif = Naif(color)

    def get_move(self, board):
        start = time.time()
        score, move = self.minimax_alpha_beta(board, self.depth, -inf, inf, True, self.depth)
        end = time.time()
        return move

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player, max_depth):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board, depth, max_depth), None

        color = self.color if maximizing_player else (WHITE if self.color == BLACK else BLACK)
        naif = Naif(color)
        
        if maximizing_player:
            moves = self.get_all_valid_moves_with_rafle(board)
            # Tri des mouvements pour maximiser l'élagage
            moves = sorted(moves, key=lambda m: self.move_heuristic(board, m), reverse=True)
        else:
            moves = naif.get_all_valid_moves(board)
            # Tri des mouvements adverses pour maximiser l'élagage
            moves = sorted(moves, key=lambda m: -self.move_heuristic(board, m))

        if not moves:
            return self.evaluate(board, depth, max_depth), None

        if maximizing_player:
            max_eval = -inf
            best_move = None
            for move in moves:
                # Utilisation de undo_move au lieu de deepcopy
                self.apply_move(board, move)
                eval, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False, max_depth)
                self.undo_move(board, move)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = inf
            best_move = None
            for move in moves:
                # Utilisation de undo_move au lieu de deepcopy
                self.apply_move(board, move)
                eval, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True, max_depth)
                self.undo_move(board, move)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def move_heuristic(self, board, move):
        """Évalue rapidement un mouvement pour le tri"""
        score = 0
        if len(move) == 5:  # C'est une capture
            score += self.CAPTURE_BONUS
            # Bonus pour les captures qui mènent à une promotion
            end_row = move[2]
            if (self.color == WHITE and end_row == 9) or (self.color == BLACK and end_row == 0):
                score += self.KING_VAL
            # Bonus pour les captures qui évitent une menace
            piece = board.board[move[0]][move[1]]
            if piece and self.is_threatened(board, piece):
                score += self.THREAT_BONUS
        else:  # Mouvement simple
            # Bonus pour l'avancement
            start_row, end_row = move[0], move[2]
            if self.color == BLACK:
                score += (end_row - start_row) * self.ADVANCE_BONUS
            else:
                score += (start_row - end_row) * self.ADVANCE_BONUS
            # Bonus pour les mouvements qui créent une menace
            piece = board.board[move[0]][move[1]]
            if piece and self.can_capture(board, piece):
                score += self.THREAT_BONUS
        return score

    def evaluate(self, board, depth, max_depth):
        if self.is_game_over(board):
            blancs = sum(1 for row in board.board for p in row if p and p.color == WHITE)
            noirs = sum(1 for row in board.board for p in row if p and p.color == BLACK)
            if blancs == 0 and noirs == 0:
                return 0
            ia_wins = (noirs == 0 and self.color == WHITE) or (blancs == 0 and self.color == BLACK)
            score = 10000 - (max_depth - depth)  # Prise en compte de la profondeur
            return score if ia_wins else -score

        value = 0
        mobility_bonus = 0
        capture_bonus = 0
        threat_bonus = 0

        for row in board.board:
            for piece in row:
                if piece != 0:
                    base = self.KING_VAL if piece.king else self.PIECE_VAL
                    bonus = 0

                    # Bonus d'avancement
                    if not piece.king:
                        bonus += piece.row if piece.color == BLACK else (9 - piece.row)
                        bonus *= self.ADVANCE_BONUS

                    # Bonus pour pièces menacées ou capables de capturer
                    if self.can_capture(board, piece):
                        capture_bonus += self.CAPTURE_BONUS
                    if self.is_threatened(board, piece):
                        threat_bonus -= self.THREAT_BONUS

                    # Bonus bord
                    if piece.col in (0, 9):
                        bonus += 2

                    # Mobilité
                    moves = self.naif.get_piece_moves(board, piece)
                    mobility_bonus += len(moves) * self.MOBILITY_BONUS

                    if piece.color == self.color:
                        value += base + bonus
                    else:
                        value -= base + bonus

        value += mobility_bonus + capture_bonus + threat_bonus
        return value

    def is_threatened(self, board, piece):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for drow, dcol in directions:
            enemy_row = piece.row + drow
            enemy_col = piece.col + dcol
            jump_row = piece.row - drow
            jump_col = piece.col - dcol
            if (0 <= enemy_row < 10 and 0 <= enemy_col < 10 and
                0 <= jump_row < 10 and 0 <= jump_col < 10):
                enemy = board.board[enemy_row][enemy_col]
                if enemy != 0 and enemy.color != piece.color:
                    if board.board[jump_row][jump_col] == 0:
                        return True
        return False

    def is_game_over(self, board):
        white_left = black_left = 0
        for row in board.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        white_left += 1
                    elif piece.color == BLACK:
                        black_left += 1
        return white_left == 0 or black_left == 0

    def apply_move(self, board, move):
        if len(move) == 5:
            start_row, start_col, end_row, end_col, captured = move
        else:
            start_row, start_col, end_row, end_col = move
            captured = None
        piece = board.board[start_row][start_col]
        if piece and piece != 0:
            piece.move(end_row, end_col)
        board.board[end_row][end_col] = piece
        board.board[start_row][start_col] = 0
        if captured:
            if isinstance(captured, tuple):
                board.board[captured[0]][captured[1]] = 0
        if piece and piece != 0:
            if piece.color == WHITE and end_row == 9:
                piece.king = True
            elif piece.color == BLACK and end_row == 0:
                piece.king = True

    def undo_move(self, board, move):
        """Annule un coup joué"""
        if len(move) == 5:
            start_row, start_col, end_row, end_col, captured = move
        else:
            start_row, start_col, end_row, end_col = move
            captured = None
            
        piece = board.board[end_row][end_col]
        if piece and piece != 0:
            piece.move(start_row, start_col)
        board.board[start_row][start_col] = piece
        board.board[end_row][end_col] = 0
        
        if captured:
            if isinstance(captured, tuple):
                # On recrée la pièce capturée avec la couleur opposée
                from piece import Piece
                # On détermine la couleur de la pièce capturée en fonction de sa position
                captured_color = WHITE if captured[0] < 5 else BLACK
                captured_piece = Piece(captured[0], captured[1], captured_color)
                board.board[captured[0]][captured[1]] = captured_piece

    def get_chain_captures(self, board, piece):
        def explore(board, piece, path, visited):
            if piece == 0:
                return []
            captures = []
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            found = False
            for drow, dcol in directions:
                jump_row = piece.row + 2 * drow
                jump_col = piece.col + 2 * dcol
                middle_row = piece.row + drow
                middle_col = piece.col + dcol
                if (0 <= jump_row < len(board.board) and 0 <= jump_col < len(board.board[0]) and
                    0 <= middle_row < len(board.board) and 0 <= middle_col < len(board.board[0])):
                    middle_piece = board.board[middle_row][middle_col]
                    if (middle_piece != 0 and middle_piece.color != piece.color and
                        board.board[jump_row][jump_col] == 0 and (middle_row, middle_col) not in visited):
                        new_board = copy.deepcopy(board)
                        new_piece = new_board.board[piece.row][piece.col]
                        new_board.board[jump_row][jump_col] = new_piece
                        new_board.board[piece.row][piece.col] = 0
                        new_board.board[middle_row][middle_col] = 0
                        if new_piece != 0:
                            new_piece.row, new_piece.col = jump_row, jump_col
                        new_path = path + [(piece.row, piece.col, jump_row, jump_col, (middle_row, middle_col))]
                        new_visited = visited | {(middle_row, middle_col)}
                        sub_captures = explore(new_board, new_piece, new_path, new_visited)
                        if sub_captures:
                            captures.extend(sub_captures)
                        else:
                            captures.append(new_path)
                        found = True
            if not found and path:
                return [path]
            return captures
        return explore(board, piece, [], set())

    def get_all_valid_moves_with_rafle(self, board):
        valid_moves = []
        chain_captures = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.board[row][col]
                if piece != 0 and piece.color == self.color:
                    rafles = self.get_chain_captures(board, piece)
                    for rafle in rafles:
                        if len(rafle) > 0:
                            chain_captures.append(rafle)
        if chain_captures:
            # On retourne toutes les rafles possibles, triées par longueur
            chain_captures.sort(key=len, reverse=True)
            return [move for rafle in chain_captures for move in rafle]  # Retourne tous les coups de toutes les rafles
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.board[row][col]
                if piece != 0 and piece.color == self.color:
                    moves = self.naif.get_piece_moves(board, piece)
                    valid_moves.extend([m for m in moves if len(m) == 4])
        return valid_moves

    def can_capture(self, board, piece):
        moves = self.naif.get_piece_moves(board, piece)
        return any(len(m) == 5 for m in moves) 