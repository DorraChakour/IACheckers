import copy
from constants import WHITE, BLACK
from ia.naif import Naif

class Minimax:
    PIECE_VAL = 10
    KING_VAL = 50

    def __init__(self, color, depth):
        """
        Initialise l'IA Minimax avec une couleur (BLACK ou WHITE) et une profondeur de recherche
        """
        self.color = color
        self.depth = depth
        self.naif = Naif(color)

    def get_move(self, board):
        """
        Retourne le meilleur mouvement selon l'algorithme Minimax
        """
        _, move = self.minimax(board, self.depth, True)
        return move

    def minimax(self, board, depth, maximizing_player):
        """
        Implémentation de l'algorithme Minimax
        """
        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board), None

        color = self.color if maximizing_player else (WHITE if self.color == BLACK else BLACK)
        naif = Naif(color)
        moves = naif.get_all_valid_moves(board)
        if not moves:
            return self.evaluate(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, move)
                eval, _ = self.minimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, move)
                eval, _ = self.minimax(new_board, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def evaluate(self, board):
        """
        Fonction d'évaluation du plateau
        """
        value = 0
        for row in board.board:
            for piece in row:
                if piece != 0:
                    if piece.color == self.color:
                        value += self.KING_VAL if piece.king else self.PIECE_VAL
                    else:
                        value -= self.KING_VAL if piece.king else self.PIECE_VAL
        return value

    def is_game_over(self, board):
        # Simple : partie finie si un joueur n'a plus de pièces
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
        # Applique un mouvement sur une copie du plateau
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
        """
        Retourne toutes les séquences de captures en chaîne possibles pour une pièce donnée.
        Chaque séquence est une liste de mouvements [(start_row, start_col, end_row, end_col, captured), ...]
        """
        def explore(board, piece, path, visited):
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
                        # On simule la capture
                        new_board = copy.deepcopy(board)
                        new_piece = new_board.board[piece.row][piece.col]
                        new_board.board[jump_row][jump_col] = new_piece
                        new_board.board[piece.row][piece.col] = 0
                        new_board.board[middle_row][middle_col] = 0
                        new_piece.row, new_piece.col = jump_row, jump_col
                        new_path = path + [(piece.row, piece.col, jump_row, jump_col, (middle_row, middle_col))]
                        new_visited = visited | {(middle_row, middle_col)}
                        # On continue la rafle
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