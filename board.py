import pygame
from piece import Piece
from constants import ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, DARK

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 20
        self.black_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    pygame.draw.rect(win, DARK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    if row < 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win) 