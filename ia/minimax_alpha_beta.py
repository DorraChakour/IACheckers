import copy
import time
from constants import WHITE, BLACK
from ia.naif import Naif

class MinimaxAlphaBeta:
    PIECE_VAL = 10
    KING_VAL = 50

    def __init__(self, color, depth):
        """
        Initialise l'IA Minimax avec élagage alpha-beta avec une couleur (BLACK ou WHITE) et une profondeur de recherche
        """
        self.color = color
        self.depth = depth
        self.naif = Naif(color)

    def get_move(self, board):
        """
        Retourne le meilleur mouvement selon l'algorithme Minimax avec élagage alpha-beta
        À implémenter
        """
        start = time.time()
        score, move = self.minimax_alpha_beta(board, self.depth, float('-inf'), float('inf'), True, self.depth)
        end = time.time()
        print(f"[AlphaBeta] Temps de calcul du coup : {round(end - start, 3)}s, score évalué : {score}")
        return move

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player, max_depth):
        """
        Implémentation de l'algorithme Minimax avec élagage alpha-beta
        À implémenter
        """
        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board, depth, max_depth), None

        color = self.color if maximizing_player else (WHITE if self.color == BLACK else BLACK)
        naif = Naif(color)
        if maximizing_player:
            moves = self.get_all_valid_moves_with_rafle(board)
        else:
            moves = naif.get_all_valid_moves(board)
        if not moves:
            return self.evaluate(board, depth, max_depth), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, move)
                eval, _ = self.minimax_alpha_beta(new_board, depth-1, alpha, beta, False, max_depth)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, move)
                eval, _ = self.minimax_alpha_beta(new_board, depth-1, alpha, beta, True, max_depth)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board, depth, max_depth):
        """
        Fonction d'évaluation du plateau
        À implémenter
        """
        # Bonus/malus selon la profondeur pour favoriser la victoire rapide
        if self.is_game_over(board):
            blancs = sum(1 for row in board.board for p in row if p != 0 and p.color == WHITE)
            noirs = sum(1 for row in board.board for p in row if p != 0 and p.color == BLACK)
            if blancs == 0 and noirs == 0:
                return 0  # Match nul
            elif blancs == 0:
                return 10000 - (max_depth - depth)  # Victoire IA
            elif noirs == 0:
                return -10000 + (max_depth - depth)  # Défaite IA
        # Évaluation simple et rapide
        value = 0
        for row in board.board:
            for piece in row:
                if piece != 0:
                    if piece.color == self.color:
                        value += self.KING_VAL if piece.king else self.PIECE_VAL
                    else:
                        value -= self.KING_VAL if piece.king else self.PIECE_VAL
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
        # Applique un mouvement sur une copie du plateau (identique à Minimax)
        if len(move) == 5:
            start_row, start_col, end_row, end_col, captured = move
        else:
            start_row, start_col, end_row, end_col = move
            captured = None
        piece = board.board[start_row][start_col]
        board.board[end_row][end_col] = piece
        board.board[start_row][start_col] = 0
        if captured:
            if isinstance(captured, tuple):
                board.board[captured[0]][captured[1]] = 0
        # Promotion éventuelle
        if piece and piece != 0:
            if piece.color == WHITE and end_row == 9:
                piece.king = True
            elif piece.color == BLACK and end_row == 0:
                piece.king = True

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
            return [rafle[0] for rafle in chain_captures]
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