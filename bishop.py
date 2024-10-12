from pieces import Piece

class Bishop(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.board = board

    def show_possible_moves(self, bishop_row, bishop_col):
        self.clear_possible_moves()
        
        if self.board.current_player == 'white' and self.piece_positions[bishop_row][bishop_col] == 'white_bishop':
            self.white_depth_move(self.bishop_directions, bishop_row, bishop_col)
            king_r, king_c = self.return_white_king_pos()
            if self.white_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(bishop_row, bishop_col, king_r, king_c)

        if self.board.current_player == 'black' and self.piece_positions[bishop_row][bishop_col] == 'black_bishop':
            self.black_depth_move(self.bishop_directions, bishop_row, bishop_col)
            king_r, king_c = self.return_black_king_pos()
            if self.black_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(bishop_row, bishop_col, king_r, king_c)

        self.highlight_possible_moves()

    def move(self, bishop_r, bishop_c, new_r, new_c):
        
        if self.possible_moves[new_r][new_c] == True:
            if self.piece_positions[bishop_r][bishop_c] == 'white_bishop':
                self.piece_positions[new_r][new_c] = 'white_bishop'
            elif self.piece_positions[bishop_r][bishop_c] == 'black_bishop':
                self.piece_positions[new_r][new_c] = 'black_bishop'

            self.piece_positions[bishop_r][bishop_c] = None
            self.move_piece_on_board(bishop_r, bishop_c, new_r, new_c)
            self.switch_player_turn()

