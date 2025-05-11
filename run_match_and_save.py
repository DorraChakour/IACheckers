from ia.naif import Naif
from ia.minimax_complexe import Minimax
from ia.alphabetaTest import MinimaxAlphaBetaTest
from board import Board
from constants import WHITE, BLACK

def jouer_match(ia1_class, ia2_class, depth1=4, depth2=4, nb_parties=1):
    scores = { 'IA1': 0, 'IA2': 0, 'Nul': 0 }
    for i in range(nb_parties):
        print(f"\nDébut de la partie {i+1}/{nb_parties}")
        board = Board()
        # Alterne les couleurs
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
        max_turns = 300
        print(f"Configuration : {ia1_name} ({'Noir' if i % 2 == 1 else 'Blanc'}) vs {ia2_name} ({'Noir' if i % 2 == 0 else 'Blanc'})")
        
        while not ia1.is_game_over(board) and turn < max_turns:
            joueur = joueurs[turn % 2]
            joueur_name = ia1_name if turn % 2 == 0 else ia2_name
            move = joueur.get_move(board)
            if move is None:
                print(f"Plus de mouvements possibles pour {joueur_name}")
                break
                
            # affiche coup joué
            if len(move) == 5:
                start_row, start_col, end_row, end_col, captured = move
                print(f"Tour {turn+1} - {joueur_name} : Capture de ({start_row},{start_col}) vers ({end_row},{end_col}) en prenant la pièce en ({captured[0]},{captured[1]})")
            else:
                start_row, start_col, end_row, end_col = move
                print(f"Tour {turn+1} - {joueur_name} : Déplacement de ({start_row},{start_col}) vers ({end_row},{end_col})")
            
            joueur.apply_move(board, move)
            
            # on a affiché lévaluation de la position
            if hasattr(joueur, 'evaluate_state'):
                score = joueur.evaluate_state(board)
                print(f"Évaluation de la position pour {joueur_name} : {score}")
            
            turn += 1
            
        blancs = sum(1 for row in board.board for p in row if p and p.color == WHITE)
        noirs = sum(1 for row in board.board for p in row if p and p.color == BLACK)
        print(f"\nFin de la partie {i+1}:")
        print(f"Pièces blanches restantes : {blancs}")
        print(f"Pièces noires restantes : {noirs}")
        
        if blancs == 0 and noirs == 0:
            scores['Nul'] += 1
            print("Match nul !")
        elif noirs == 0:
            if i % 2 == 0:
                scores['IA1'] += 1
                print(f"Victoire de {ia1_name} !")
            else:
                scores['IA2'] += 1
                print(f"Victoire de {ia2_name} !")
        elif blancs == 0:
            if i % 2 == 0:
                scores['IA2'] += 1
                print(f"Victoire de {ia2_name} !")
            else:
                scores['IA1'] += 1
                print(f"Victoire de {ia1_name} !")
        else:
            scores['Nul'] += 1
            print("Match nul !")
            
        print(f"\nScore actuel :")
        print(f"{ia1_name} : {scores['IA1']} victoires")
        print(f"{ia2_name} : {scores['IA2']} victoires")
        print(f"Matchs nuls : {scores['Nul']}")
        print("-"*50)
    return scores

def tournoi_ia():
    confrontations = [
       (Naif, Minimax, 0, 3),
        (Naif, MinimaxAlphaBetaTest, 0, 3),
       (Minimax, MinimaxAlphaBetaTest, 2, 3),
        
    ]
    noms = {
        Naif: "Naif",
        Minimax: "Minimax",
        MinimaxAlphaBetaTest: "MinimaxAlphaBeta (nouvelle version)"
    }
    with open("resultatsFinals1.txt", "w", encoding="utf-8") as f:
        for ia1_class, ia2_class, d1, d2 in confrontations:
            print(f"\nDébut du duel : {noms[ia1_class]} vs {noms[ia2_class]}")
            scores = jouer_match(ia1_class, ia2_class, depth1=d1, depth2=d2, nb_parties=50)  
            f.write(f"Duel : {noms[ia1_class]} vs {noms[ia2_class]}\n")
            f.write(f"{noms[ia1_class]} : {scores['IA1']} victoires\n")
            f.write(f"{noms[ia2_class]} : {scores['IA2']} victoires\n")
            f.write(f"Matchs nuls : {scores['Nul']}\n")
            f.write("-"*40 + "\n")

if __name__ == "__main__":
    tournoi_ia() 