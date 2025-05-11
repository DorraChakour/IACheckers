from ia.naif import Naif
from ia.minimax_complexe import Minimax
from ia.minimax_alpha_beta_complexe_heuristique import MinimaxAlphaBeta
from normal_alphabeta_minimax import MinimaxAlphaBetaSansHeuristique
from board import Board
from constants import WHITE, BLACK

def jouer_match(ia1_class, ia2_class, depth1=4, depth2=4, nb_parties=1):
    scores = { 'IA1': 0, 'IA2': 0, 'Nul': 0 }
    for i in range(nb_parties):
        board = Board()
        # Alterner les couleurs
        if i % 2 == 0:
            ia1 = ia1_class(WHITE, depth1) if ia1_class != Naif else ia1_class(WHITE)
            ia2 = ia2_class(BLACK, depth2) if ia2_class != Naif else ia2_class(BLACK)
            ia1_name = ia1_class.__name__
            ia2_name = ia2_class.__name__
        else:
            ia1 = ia1_class(BLACK, depth1) if ia1_class != Naif else ia1_class(BLACK)
            ia2 = ia2_class(WHITE, depth2) if ia2_class != Naif else ia2_class(WHITE)
            ia1_name = ia1_class.__name__
            ia2_name = ia2_class.__name__
        joueurs = [ia1, ia2]
        turn = 0
        max_turns = 400
        while not ia1.is_game_over(board) and turn < max_turns:
            joueur = joueurs[turn % 2]
            move = joueur.get_move(board)
            if move is None:
                break
            joueur.apply_move(board, move)
            turn += 1
        blancs = sum(1 for row in board.board for p in row if p and p.color == WHITE)
        noirs = sum(1 for row in board.board for p in row if p and p.color == BLACK)
        if blancs == 0 and noirs == 0:
            scores['Nul'] += 1
        elif noirs == 0:
            if i % 2 == 0:
                scores['IA1'] += 1
            else:
                scores['IA2'] += 1
        elif blancs == 0:
            if i % 2 == 0:
                scores['IA2'] += 1
            else:
                scores['IA1'] += 1
        else:
            scores['Nul'] += 1
    return scores

def tournoi_ia():
    confrontations = [
       # (Naif, Minimax, 0, 3),
      #  (Naif, MinimaxAlphaBetaSansHeuristique, 0, 4),
      #  (Naif, MinimaxAlphaBeta, 0, 4),
        (Minimax, MinimaxAlphaBetaSansHeuristique, 3, 4),
      #  (Minimax, MinimaxAlphaBeta, 3, 4),
        (MinimaxAlphaBetaSansHeuristique, MinimaxAlphaBeta, 4, 4),
    ]
    noms = {
        Naif: "Naif",
        Minimax: "Minimax",
        MinimaxAlphaBetaSansHeuristique: "MinimaxAlphaBeta (sans heuristique)",
        MinimaxAlphaBeta: "MinimaxAlphaBeta (avec heuristique)"
    }
    with open("resultats50tours2.txt", "w", encoding="utf-8") as f:
        for ia1_class, ia2_class, d1, d2 in confrontations:
            scores = jouer_match(ia1_class, ia2_class, depth1=d1, depth2=d2, nb_parties=50)
            f.write(f"Duel : {noms[ia1_class]} vs {noms[ia2_class]}\n")
            f.write(f"{noms[ia1_class]} : {scores['IA1']} victoires\n")
            f.write(f"{noms[ia2_class]} : {scores['IA2']} victoires\n")
            f.write(f"Matchs nuls : {scores['Nul']}\n")
            f.write("-"*40 + "\n")

if __name__ == "__main__":
    tournoi_ia() 