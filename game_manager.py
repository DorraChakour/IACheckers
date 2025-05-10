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
        self.scores = {'player1': 0, 'player2': 0, 'draw': 0}

    def choose_players(self):
        print("\nChoisissez les joueurs pour le combat :")
        print("1. Naif vs Minimax")
        print("2. Minimax vs MinimaxAlphaBeta")
        print("3. MinimaxAlphaBeta vs Naif")
        choice = input("Votre choix (1, 2 ou 3) : ")
        
        if choice == '1':
            return (Naif, Minimax)
        elif choice == '2':
            return (Minimax, MinimaxAlphaBeta)
        elif choice == '3':
            return (MinimaxAlphaBeta, Naif)
        else:
            print("Choix invalide, utilisation par défaut : Minimax vs MinimaxAlphaBeta")
            return (Minimax, MinimaxAlphaBeta)

    def run(self):
        player1_class, player2_class = self.choose_players()
        
        for game in range(self.nb_games):
            print(f"\nDébut de la partie {game+1}/{self.nb_games}")
            board = Board()
            
            # Alterner les couleurs à chaque partie
            if game % 2 == 0:
                player1_color = BLACK
                player2_color = WHITE
            else:
                player1_color = WHITE
                player2_color = BLACK
                
            # Initialisation des joueurs avec la même profondeur
            depth1 = 4 if player1_class == MinimaxAlphaBeta else 4
            depth2 = 4 if player2_class == MinimaxAlphaBeta else 4
            
            if player1_class == Naif:
                player1 = player1_class(player1_color)
            else:
                player1 = player1_class(player1_color, depth1)
                
            if player2_class == Naif:
                player2 = player2_class(player2_color)
            else:
                player2 = player2_class(player2_color, depth2)
            
            turn_color = BLACK  # Noir commence toujours
            turn_count = 0
            winner = None
            
            print(f"Configuration : {player1_class.__name__} ({'Noir' if player1_color == BLACK else 'Blanc'}) vs {player2_class.__name__} ({'Noir' if player2_color == BLACK else 'Blanc'})")
            
            while turn_count < self.max_turns:
                turn_count += 1
                current_player = player1 if turn_color == player1_color else player2
                move = current_player.get_move(board)
                print(f"Tour {turn_count} - {current_player.__class__.__name__} joue : {move}")
                if not move:
                    winner = WHITE if turn_color == BLACK else BLACK
                    print(f"Plus de mouvements possibles pour {'Noir' if turn_color == BLACK else 'Blanc'}")
                    break
                self.apply_move(board, move)
                # Promotion éventuelle
                if len(move) >= 4:
                    end_row = move[2]
                    piece = board.board[move[2]][move[3]]
                    if piece and piece != 0:
                        if piece.color == WHITE and end_row == 9:
                            piece.king = True
                            print("Promotion en Dame pour les Blancs!")
                        elif piece.color == BLACK and end_row == 0:
                            piece.king = True
                            print("Promotion en Dame pour les Noirs!")
                turn_color = WHITE if turn_color == BLACK else BLACK
            # Détermination du résultat
            if winner is None:
                self.scores['draw'] += 1
                print(f"\nPartie {game+1}: Match nul ({self.max_turns} coups atteints)")
            elif winner == player1_color:
                self.scores['player1'] += 1
                print(f"\nPartie {game+1}: Victoire {player1_class.__name__}")
            else:
                self.scores['player2'] += 1
                print(f"\nPartie {game+1}: Victoire {player2_class.__name__}")
            # Affichage du score intermédiaire
            print(f"\nScore après la partie {game+1}:")
            print(f"{player1_class.__name__} : {self.scores['player1']} victoires")
            print(f"{player2_class.__name__} : {self.scores['player2']} victoires")
            print(f"Matchs nuls : {self.scores['draw']}")
        # Affichage du score final
        print(f"\nRésultat final après {self.nb_games} parties :")
        print(f"{player1_class.__name__} : {self.scores['player1']} victoires")
        print(f"{player2_class.__name__} : {self.scores['player2']} victoires")
        print(f"Matchs nuls : {self.scores['draw']}")

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