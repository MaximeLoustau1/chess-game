from pieces import Piece

class Knight(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.board = board

    def show_possible_moves(self, knight_row, knight_col):
        
        self.clear_possible_moves()

        if self.board.current_player == 'white' and self.piece_positions[knight_row][knight_col] == 'white_knight':
            self.white_knight_moves(knight_row, knight_col, self.knight_moves)
            king_r, king_c = self.return_white_king_pos()
            if self.white_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(knight_row, knight_col, king_r, king_c)

        if self.board.current_player == 'black' and self.piece_positions[knight_row][knight_col] == 'black_knight':
            self.black_knight_moves(knight_row, knight_col, self.knight_moves)
            king_r, king_c = self.return_black_king_pos()
            if self.black_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(knight_row, knight_col, king_r, king_c)
            
        self.highlight_possible_moves()

    def move(self, knight_r, knight_c, new_r, new_c):

        if self.possible_moves[new_r][new_c]:

            if self.piece_positions[knight_r][knight_c] == 'white_knight':
                self.piece_positions[new_r][new_c] = 'white_knight'
            elif self.piece_positions[knight_r][knight_c] == 'black_knight':
                self.piece_positions[new_r][new_c] = 'black_knight'

            self.piece_positions[knight_r][knight_c] = None
            self.move_piece_on_board(knight_r, knight_c, new_r, new_c)
            self.switch_player_turn()