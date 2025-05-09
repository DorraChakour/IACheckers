import copy
import random
from board import Board
from ia.minimax import Minimax
from ia.minimax_alpha_beta import MinimaxAlphaBeta
from ia.naif import Naif
from constants import WHITE, BLACK

class GameManager:
    def __init__(self):
        self.nb_games = 10
        self.max_turns = 500
        self.scores = {'minimax': 0, 'minimax_alpha_beta': 0, 'draw': 0}

    def run(self):
        for game in range(self.nb_games):
            board = Board()
            # Alterner les couleurs à chaque partie
            if game % 2 == 0:
                minimax_color = BLACK
                alpha_beta_color = WHITE
            else:
                minimax_color = WHITE
                alpha_beta_color = BLACK
            minimax = Minimax(minimax_color, 3)
            alpha_beta = MinimaxAlphaBeta(alpha_beta_color, 5)
            turn_color = BLACK  # Noir commence toujours
            turn_count = 0
            winner = None
            while turn_count < self.max_turns:
                turn_count += 1
                if turn_color == minimax_color:
                    move = minimax.get_move(board)
                else:
                    move = alpha_beta.get_move(board)
                if not move:
                    winner = WHITE if turn_color == BLACK else BLACK
                    break
                self.apply_move(board, move)
                # Promotion éventuelle
                if len(move) >= 4:
                    end_row = move[2]
                    piece = board.board[move[2]][move[3]]
                    if piece and piece != 0:
                        if piece.color == WHITE and end_row == 9:
                            piece.king = True
                        elif piece.color == BLACK and end_row == 0:
                            piece.king = True
                turn_color = WHITE if turn_color == BLACK else BLACK
            # Détermination du résultat
            if winner is None:
                self.scores['draw'] += 1
                print(f"Partie {game+1}: Match nul ({self.max_turns} coups atteints)")
            elif winner == minimax_color:
                self.scores['minimax'] += 1
                print(f"Partie {game+1}: Victoire Minimax")
            else:
                self.scores['minimax_alpha_beta'] += 1
                print(f"Partie {game+1}: Victoire Minimax Alpha-Beta")
        # Affichage du score final
        print(f"\nRésultat final après {self.nb_games} parties :")
        print(f"Minimax : {self.scores['minimax']} victoires")
        print(f"Minimax Alpha-Beta : {self.scores['minimax_alpha_beta']} victoires")
        print(f"Matchs nuls : {self.scores['draw']}")

    def apply_move(self, board, move):
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