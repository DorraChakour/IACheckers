print("Menu :")
print("1. Jouer contre une IA")
print("2. Lancer GameManager (IA vs IA)")
choix = input("Votre choix (1 ou 2) : ")

if choix == '2':
    from game_manager import GameManager
    GameManager().run()
else:
    from ia.naif import Naif
    from ia.minimax import Minimax
    from ia.minimax_alpha_beta import MinimaxAlphaBeta
    from board import Board
    from constants import BLACK, WHITE, SQUARE_SIZE, WIDTH, HEIGHT
    import pygame
    import time
    import random

    def play_vs_ia():
        print("Choisissez l'IA contre laquelle jouer :")
        print("1. IA naïve")
        print("2. IA Minimax")
        print("3. IA Minimax Alpha-Beta")
        ia_choice = input("Votre choix (1, 2 ou 3) : ")
        if ia_choice == '2':
            ia = Minimax(BLACK, 3)
            ia_name = "Minimax"
        elif ia_choice == '3':
            ia = MinimaxAlphaBeta(BLACK, 5)
            ia_name = "Minimax Alpha-Beta"
        else:
            ia = Naif(BLACK)
            ia_name = "naïve"

        pygame.init()
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f'Jeu de Dames - Joueur vs IA {ia_name}')
        FONT = pygame.font.SysFont('Arial', 40)
        ANIMATION_DELAY = 0.5
        board = Board()
        player_turn = True
        selected_piece = None
        valid_moves = []
        rafle_in_progress = False
        run = True
        move = None  # Initialisation pour éviter UnboundLocalError
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE
                    if selected_piece:
                        for move in valid_moves:
                            if move[2] == row and move[3] == col:
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
                                piece.move(end_row, end_col)
                                if piece.color == WHITE and end_row == 9:
                                    piece.king = True
                                elif piece.color == BLACK and end_row == 0:
                                    piece.king = True
                                next_captures = get_valid_moves(board, piece, only_captures=True)
                                if captured and next_captures:
                                    selected_piece = piece
                                    valid_moves = next_captures
                                    rafle_in_progress = True
                                    break
                                else:
                                    player_turn = False
                                    selected_piece = None
                                    valid_moves = []
                                    rafle_in_progress = False
                                    break
                        else:
                            if not rafle_in_progress:
                                selected_piece = None
                                valid_moves = []
                    else:
                        piece = board.board[row][col]
                        if piece != 0 and piece.color == WHITE:
                            selected_piece = piece
                            valid_moves = get_valid_moves(board, piece)
            if not player_turn:
                move = ia.get_move(board)
                if move:
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
                    piece.move(end_row, end_col)
                    if piece.color == WHITE and end_row == 9:
                        piece.king = True
                    elif piece.color == BLACK and end_row == 0:
                        piece.king = True
                player_turn = True
                selected_piece = None
                valid_moves = []
                rafle_in_progress = False
            board.draw(WIN)
            if selected_piece:
                for move in valid_moves:
                    row, col = move[2], move[3]
                    color = (255, 0, 0) if (len(move) == 5) else (0, 255, 0)
                    pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
            pygame.display.update()
            # Vérifier la fin de partie pour le joueur humain
            if player_turn:
                coups_joueur = []
                for row in board.board:
                    for piece in row:
                        if piece != 0 and piece.color == WHITE:
                            coups_joueur.extend(get_valid_moves(board, piece))
                if not coups_joueur:
                    blancs = sum(1 for row in board.board for p in row if p != 0 and p.color == WHITE)
                    noirs = sum(1 for row in board.board for p in row if p != 0 and p.color == BLACK)
                    if blancs == 0 and noirs == 0:
                        print("Match nul ! Plus aucune pièce sur le plateau.")
                    elif blancs == 0:
                        print("Victoire de l'IA !")
                    elif noirs == 0:
                        print("Victoire du joueur !")
                    else:
                        print("Partie terminée ! Plus de coups possibles pour le joueur.")
                    break
            # Vérifier la fin de partie uniquement pour l'IA
            if not player_turn and not move:
                blancs = sum(1 for row in board.board for p in row if p != 0 and p.color == WHITE)
                noirs = sum(1 for row in board.board for p in row if p != 0 and p.color == BLACK)
                if blancs == 0 and noirs == 0:
                    print("Match nul ! Plus aucune pièce sur le plateau.")
                elif blancs == 0:
                    print("Victoire de l'IA !")
                elif noirs == 0:
                    print("Victoire du joueur !")
                else:
                    print("Partie terminée ! Plus de coups possibles pour l'IA.")
                break
        pygame.quit()

    def get_valid_moves(board, piece, only_captures=False):
        moves = []
        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        from constants import ROWS, COLS, WHITE
        if piece.king:
            for drow, dcol in directions:
                r, c = piece.row, piece.col
                found_opponent = False
                while True:
                    r += drow
                    c += dcol
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if board.board[r][c] == 0:
                            if found_opponent:
                                captures.append((piece.row, piece.col, r, c, (r - drow, c - dcol)))
                                break
                            elif not only_captures:
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
                if 0 <= new_row < 10 and 0 <= new_col < 10:
                    if board.board[new_row][new_col] == 0 and drow == (1 if piece.color == WHITE else -1) and not only_captures:
                        moves.append((piece.row, piece.col, new_row, new_col))
                    jump_row = piece.row + 2 * drow
                    jump_col = piece.col + 2 * dcol
                    if 0 <= jump_row < 10 and 0 <= jump_col < 10:
                        if board.board[jump_row][jump_col] == 0:
                            middle_row = piece.row + drow
                            middle_col = piece.col + dcol
                            if (board.board[middle_row][middle_col] != 0 and 
                                board.board[middle_row][middle_col].color != piece.color):
                                captures.append((piece.row, piece.col, jump_row, jump_col, (middle_row, middle_col)))
        if only_captures:
            return captures
        return moves + captures

    play_vs_ia()