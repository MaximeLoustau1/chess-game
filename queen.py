from pieces import Piece

class Queen(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.board = board

    def show_possible_moves(self, queen_row, queen_col):

        self.clear_possible_moves()
            
        if self.board.current_player == 'white' and self.piece_positions[queen_row][queen_col] == 'white_queen':
            self.white_depth_move(self.queen_directions, queen_row, queen_col)
            king_r, king_c = self.return_white_king_pos()
            if self.white_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(queen_row, queen_col, king_r, king_c)
            
        if self.board.current_player == 'black' and self.piece_positions[queen_row][queen_col] == 'black_queen':
            self.black_depth_move(self.queen_directions, queen_row, queen_col)
            king_r, king_c = self.return_black_king_pos()
            if self.black_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(queen_row, queen_col, king_r, king_c)

        self.highlight_possible_moves()

    def move(self, queen_r, queen_c, new_r, new_c):

        if self.possible_moves[new_r][new_c] == True:
            if self.piece_positions[queen_r][queen_c] == 'white_queen':
                self.piece_positions[new_r][new_c] = 'white_queen'
            elif self.piece_positions[queen_r][queen_c] == 'black_queen':
                self.piece_positions[new_r][new_c] = 'black_queen'

            self.piece_positions[queen_r][queen_c] = None
            self.move_piece_on_board(queen_r, queen_c, new_r, new_c)
            self.switch_player_turn()