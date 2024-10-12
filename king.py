from pieces import Piece

class King(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.white_king_moved = False
        self.black_king_moved = False
        self.castling_rights = {
            'white': {'long': False, 'short': False},
            'black': {'long': False, 'short': False}
        }

    def castle(self, color, side, row, col):
        rook_col = col + 3 if side == 'short' else col - 4
        king_dest = col + 2 if side == 'short' else col - 2
        rook_dest = col + 1 if side == 'short' else col - 1

        self.piece_positions[row][king_dest] = f'{color}_king'
        self.piece_positions[row][rook_dest] = f'{color}_rook'
        self.piece_positions[row][col] = None
        self.piece_positions[row][rook_col] = None

        self.move_piece_on_board(row, col, row, king_dest)
        self.move_piece_on_board(row, rook_col, row, rook_dest)
        self.castling_rights[color][side] = False

    def move(self, king_r, king_c, new_r, new_c):
        offset = abs(king_c - new_c)
        color = 'white' if 'white' in self.piece_positions[king_r][king_c] else 'black'

        if self.possible_moves[new_r][new_c] and offset < 2:
            self.piece_positions[new_r][new_c] = f'{color}_king'
            setattr(self, f'{color}_king_moved', True)
            self.piece_positions[king_r][king_c] = None
            self.move_piece_on_board(king_r, king_c, new_r, new_c)
            self.switch_player_turn()
        
        elif self.castling_rights[color]['long'] and self.possible_moves[new_r][new_c]:
            self.castle(color, 'long', king_r, king_c)
            setattr(self, f'{color}_king_moved', True)
            self.switch_player_turn()
        elif self.castling_rights[color]['short'] and self.possible_moves[new_r][new_c]:
            self.castle(color, 'short', king_r, king_c)
            setattr(self, f'{color}_king_moved', True)
            self.switch_player_turn()

    def show_possible_moves(self, king_row, king_col):
        self.clear_possible_moves()

        if self.board.current_player == 'white' and self.piece_positions[king_row][king_col] == 'white_king':
            if king_row == 7 and king_col == 4 and self.piece_positions[king_row][king_col-4] == 'white_rook':  # long castle
                if not self.piece_positions[king_row][king_col-1] and not self.piece_positions[king_row][king_col-2] and not self.piece_positions[king_row][king_col-3]:
                    if not any(self.white_walks_in_check(self.piece_positions, king_row, king_col-i) for i in range(4)):
                        if not self.white_king_moved:
                            self.castling_rights['white']['long'] = True
                            self.possible_moves[king_row][king_col-4] = True

            if king_row == 7 and king_col == 4 and self.piece_positions[king_row][king_col+3] == 'white_rook':  # short castle
                if not self.piece_positions[king_row][king_col+1] and not self.piece_positions[king_row][king_col+2]:
                    if not any(self.white_walks_in_check(self.piece_positions, king_row, king_col+i) for i in range(3)):
                        if not self.white_king_moved:
                            self.castling_rights['white']['short'] = True
                            self.possible_moves[king_row][king_col+3] = True

            for i in range(king_row - 1, king_row + 2):
                for j in range(king_col - 1, king_col + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and not (i == king_row and j == king_col):
                        if not self.is_white(self.piece_positions[i][j]) and not self.white_walks_in_check(self.piece_positions, i, j):
                            self.possible_moves[i][j] = True

        elif self.board.current_player == 'black' and self.piece_positions[king_row][king_col] == 'black_king':
            if king_row == 0 and king_col == 4 and self.piece_positions[king_row][king_col-4] == 'black_rook':  # long castle
                if not self.piece_positions[king_row][king_col-1] and not self.piece_positions[king_row][king_col-2] and not self.piece_positions[king_row][king_col-3]:
                    if not any(self.black_walks_in_check(self.piece_positions, king_row, king_col-i) for i in range(4)):
                        if not self.black_king_moved:
                            self.castling_rights['black']['long'] = True
                            self.possible_moves[king_row][king_col-4] = True

            if king_row == 0 and king_col == 4 and self.piece_positions[king_row][king_col+3] == 'black_rook':  # short castle
                if not self.piece_positions[king_row][king_col+1] and not self.piece_positions[king_row][king_col+2]:
                    if not any(self.black_walks_in_check(self.piece_positions, king_row, king_col+i) for i in range(3)):
                        if not self.black_king_moved:
                            self.castling_rights['black']['short'] = True
                            self.possible_moves[king_row][king_col+3] = True

            for i in range(king_row - 1, king_row + 2):
                for j in range(king_col - 1, king_col + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and not (i == king_row and j == king_col):
                        if not self.is_black(self.piece_positions[i][j]) and not self.black_walks_in_check(self.piece_positions, i, j):
                            self.possible_moves[i][j] = True

        self.highlight_possible_moves()
