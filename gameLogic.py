import pygame, sys
from board import Board
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from pawn import Pawn
from knight import Knight

class Game:
    def __init__(self):
        self.board = Board()
        self.pawn = Pawn(self.board.piece_positions, self.board)
        self.knight = Knight(self.board.piece_positions, self.board)
        self.bishop = Bishop(self.board.piece_positions, self.board)
        self.rook = Rook(self.board.piece_positions, self.board)
        self.queen = Queen(self.board.piece_positions, self.board)
        self.king = King(self.board.piece_positions, self.board)
        self.board.setup_board()

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // (self.board.height // self.board.rows)
                    col = pos[0] // (self.board.width // self.board.columns)
                    self.handle_click(row, col)
            
    def handle_click(self, row, col):
        if 0 <= row < self.board.rows and 0 <= col < self.board.columns:
            if self.board.selected_piece_position is None:
                if self.board.piece_positions[row][col]:
                    self.board.selected_piece_position = (row, col)
                    self.board.clicked_cells[row][col] = True
                    self.show_possible_moves(row, col)
            else:
                piece_r, piece_c = self.board.selected_piece_position
                self.move_piece(piece_r, piece_c, row, col)
                self.pawn.clear_possible_moves()
                self.board.highlight_selected_cell(row, col)

    def show_possible_moves(self, row, col):
        if self.board.piece_positions[row][col] == 'white_pawn' or self.board.piece_positions[row][col] == 'black_pawn':
            self.pawn.show_possible_moves(row, col)         
        elif self.board.piece_positions[row][col] == 'white_knight' or self.board.piece_positions[row][col] == 'black_knight':
            self.knight.show_possible_moves(row, col)
        elif self.board.piece_positions[row][col] == 'white_bishop' or self.board.piece_positions[row][col] == 'black_bishop':
            self.bishop.show_possible_moves(row, col)
        elif self.board.piece_positions[row][col] == 'white_rook' or self.board.piece_positions[row][col] == 'black_rook':
            self.rook.show_possible_moves(row, col)
        elif self.board.piece_positions[row][col] == 'white_queen' or self.board.piece_positions[row][col] == 'black_queen':
            self.queen.show_possible_moves(row, col)
        elif self.board.piece_positions[row][col] == 'white_king' or self.board.piece_positions[row][col] == 'black_king':
            self.king.show_possible_moves(row, col)

    def move_piece(self, piece_r, piece_c, row, col):
        if self.board.piece_positions[piece_r][piece_c] == 'white_pawn' or self.board.piece_positions[piece_r][piece_c] == 'black_pawn':
            self.pawn.move(piece_r, piece_c, row, col)
        elif self.board.piece_positions[piece_r][piece_c] == 'white_knight' or self.board.piece_positions[piece_r][piece_c] == 'black_knight':
            self.knight.move(piece_r, piece_c, row, col)
        elif self.board.piece_positions[piece_r][piece_c] == 'white_bishop' or self.board.piece_positions[piece_r][piece_c] == 'black_bishop':
            self.bishop.move(piece_r, piece_c, row, col)
        elif self.board.piece_positions[piece_r][piece_c] == 'white_rook' or self.board.piece_positions[piece_r][piece_c] == 'black_rook':
            self.rook.move(piece_r, piece_c, row, col)
        elif self.board.piece_positions[piece_r][piece_c] == 'white_queen' or self.board.piece_positions[piece_r][piece_c] == 'black_queen':
            self.queen.move(piece_r, piece_c, row, col)
        elif self.board.piece_positions[piece_r][piece_c] == 'white_king' or self.board.piece_positions[piece_r][piece_c] == 'black_king':
            self.king.move(piece_r, piece_c, row, col)


