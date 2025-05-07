import pygame
import time
from board import Board
from constants import WIDTH, HEIGHT, BLACK, WHITE, SQUARE_SIZE, ROWS, COLS, DARK
from ia import Naif

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu de Dames - Mode Naïf')
FONT = pygame.font.SysFont('Arial', 40)

ANIMATION_DELAY = 0.5  # secondes entre chaque case lors d'un déplacement

def get_valid_moves(board, piece, only_captures=False):
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
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board.board[r][c] == 0:
                        if found_opponent:
                            captures.append((piece.row, piece.col, r, c, (r - drow, c - dcol)))
                            break  # On ne peut pas sauter plus loin
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
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if board.board[new_row][new_col] == 0 and drow == (1 if piece.color == WHITE else -1) and not only_captures:
                    moves.append((piece.row, piece.col, new_row, new_col))
                jump_row = piece.row + 2 * drow
                jump_col = piece.col + 2 * dcol
                if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                    if board.board[jump_row][jump_col] == 0:
                        middle_row = piece.row + drow
                        middle_col = piece.col + dcol
                        if (board.board[middle_row][middle_col] != 0 and 
                            board.board[middle_row][middle_col].color != piece.color):
                            captures.append((piece.row, piece.col, jump_row, jump_col, (middle_row, middle_col)))
    return captures if captures else moves

def promote_if_needed(piece):
    if piece.color == WHITE and piece.row == ROWS - 1:
        piece.make_king()
    elif piece.color == BLACK and piece.row == 0:
        piece.make_king()

def animate_move(board, piece, path):
    for (row, col) in path:
        piece.move(row, col)
        board.draw(WIN)
        pygame.display.update()
        time.sleep(ANIMATION_DELAY)

def show_end_message(winner):
    WIN.fill((0, 0, 0))
    if winner == WHITE:
        text = FONT.render('Victoire des Blancs !', True, (255, 255, 255))
    elif winner == BLACK:
        text = FONT.render('Victoire des Noirs !', True, (255, 255, 255))
    else:
        text = FONT.render('Match nul !', True, (255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(4)

def check_game_over(board):
    white_left = black_left = 0
    white_moves = black_moves = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.board[row][col]
            if piece != 0:
                if piece.color == WHITE:
                    white_left += 1
                    if get_valid_moves(board, piece):
                        white_moves += 1
                elif piece.color == BLACK:
                    black_left += 1
                    if get_valid_moves(board, piece):
                        black_moves += 1
    if white_left == 0 or white_moves == 0:
        return BLACK
    if black_left == 0 or black_moves == 0:
        return WHITE
    return None

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    ia = Naif(BLACK)
    player_turn = True
    selected_piece = None
    valid_moves = []
    rafle_in_progress = False
    while run:
        clock.tick(60)
        winner = check_game_over(board)
        if winner is not None:
            show_end_message(winner)
            run = False
            continue
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
                animate_move(board, piece, [(end_row, end_col)])
                promote_if_needed(piece)
                # Rafle IA : tant qu'il y a une prise possible avec la même pièce, continuer
                while True:
                    next_captures = get_valid_moves(board, piece, only_captures=True)
                    if next_captures:
                        move = ia.get_rafle_move(piece, board, next_captures)
                        if move:
                            start_row, start_col, end_row, end_col, captured = move
                            board.board[end_row][end_col] = piece
                            board.board[start_row][start_col] = 0
                            if isinstance(captured, tuple):
                                board.board[captured[0]][captured[1]] = 0
                            animate_move(board, piece, [(end_row, end_col)])
                            promote_if_needed(piece)
                        else:
                            break
                    else:
                        break
            player_turn = True
            selected_piece = None
            valid_moves = []
            rafle_in_progress = False
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
                            animate_move(board, piece, [(end_row, end_col)])
                            promote_if_needed(piece)
                            # Rafle joueur : vérifier si la même pièce peut encore prendre
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
        board.draw(WIN)
        if selected_piece:
            for move in valid_moves:
                row, col = move[2], move[3]
                color = (255, 0, 0) if (len(move) == 5) else (0, 255, 0)
                pygame.draw.circle(WIN, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()