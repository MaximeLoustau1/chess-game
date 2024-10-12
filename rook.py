from pieces import Piece

class Rook(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.board = board

    def show_possible_moves(self, rook_row, rook_col):

        self.clear_possible_moves()            


        if self.board.current_player == 'white' and self.piece_positions[rook_row][rook_col] == 'white_rook':
            self.white_depth_move(self.rook_directions, rook_row, rook_col)
            king_r, king_c = self.return_white_king_pos()
            if self.white_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(rook_row, rook_col, king_r, king_c)

        if self.board.current_player == 'black' and self.piece_positions[rook_row][rook_col] == 'black_rook':
            self.black_depth_move(self.rook_directions, rook_row, rook_col)
            king_r, king_c = self.return_black_king_pos()
            if self.black_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(rook_row, rook_col, king_r, king_c)

        self.highlight_possible_moves()

    def move(self, rook_r, rook_c, new_r, new_c):

        if self.possible_moves[new_r][new_c] == True:
            if self.piece_positions[rook_r][rook_c] == 'white_rook':
                self.piece_positions[new_r][new_c] = 'white_rook'
            elif self.piece_positions[rook_r][rook_c] == 'black_rook':
                self.piece_positions[new_r][new_c] = 'black_rook'

            self.piece_positions[rook_r][rook_c] = None
            self.move_piece_on_board(rook_r, rook_c, new_r, new_c)
            self.switch_player_turn()