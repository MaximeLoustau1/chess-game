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
        self.pieces = {
            'pawn': Pawn(self.board.piece_positions, self.board),
            'knight': Knight(self.board.piece_positions, self.board),
            'bishop': Bishop(self.board.piece_positions, self.board),
            'rook': Rook(self.board.piece_positions, self.board),
            'queen': Queen(self.board.piece_positions, self.board),
            'king': King(self.board.piece_positions, self.board)
        }
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
                self.pieces['pawn'].clear_possible_moves()  
                self.board.highlight_selected_cell(row, col)

    def show_possible_moves(self, row, col):
        piece_type = self._get_piece_type(row, col)
        if piece_type:
            self.pieces[piece_type].show_possible_moves(row, col)

    def move_piece(self, piece_r, piece_c, row, col):
        piece_type = self._get_piece_type(piece_r, piece_c)
        if piece_type:
            self.pieces[piece_type].move(piece_r, piece_c, row, col)

    def _get_piece_type(self, row, col):
        piece = self.board.piece_positions[row][col]
        return piece.split('_')[-1] if piece else None
