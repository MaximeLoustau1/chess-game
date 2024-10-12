from pieces import Piece

class King(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.board = board
        self.white_long_castle = False
        self.white_short_castle = False
        self.black_long_castle = False
        self.black_short_castle = False
        self.white_king_moved = False
        self.black_king_moved = False

    def white_l_castle(self, row, col): 
        self.piece_positions[row][col-4] = True
        self.piece_positions[row][col-2] = 'white_king'
        self.piece_positions[row][col] = None
        self.piece_positions[row][col-1] = 'white_rook'
        self.piece_positions[row][col-4] = None
        self.move_piece_on_board(row, col, row, col-2)
        self.move_piece_on_board(row, col-4, row, col-1)
        self.white_castle = False

    def white_s_castle(self, row, col): 
        self.piece_positions[row][col+3] = True
        self.piece_positions[row][col+2] = 'white_king'
        self.piece_positions[row][col] = None
        self.piece_positions[row][col+1] = 'white_rook'
        self.piece_positions[row][col+3] = None
        self.move_piece_on_board(row, col, row, col+2)
        self.move_piece_on_board(row, col+3, row, col+1)
        self.white_castle = False

    def black_l_castle(self, row, col): 
        self.piece_positions[row][col-4] = True
        self.piece_positions[row][col-2] = 'black_king'
        self.piece_positions[row][col] = None
        self.piece_positions[row][col-1] = 'black_rook'
        self.piece_positions[row][col-4] = None
        self.move_piece_on_board(row, col, row, col-2)
        self.move_piece_on_board(row, col-4, row, col-1)
        self.black_castle = False

    def black_s_castle(self, row, col): 
        self.piece_positions[row][col+3] = True
        self.piece_positions[row][col+2] = 'black_king'
        self.piece_positions[row][col] = None
        self.piece_positions[row][col+1] = 'black_rook'
        self.piece_positions[row][col+3] = None
        self.move_piece_on_board(row, col, row, col+2)
        self.move_piece_on_board(row, col+3, row, col+1)
        self.black_castle = False       

    def show_possible_moves(self, king_row, king_col):

        self.clear_possible_moves()

        if self.board.current_player == 'white' and self.piece_positions[king_row][king_col] == 'white_king':

            if king_row==7 and king_col==4 and self.piece_positions[king_row][king_col-4] == 'white_rook':   #long castle
                if not self.piece_positions[king_row][king_col-1] and not self.piece_positions[king_row][king_col-2] and not self.piece_positions[king_row][king_col-3]:
                    if not self.white_walks_in_check(self.piece_positions, king_row, king_col) and not self.white_walks_in_check(self.piece_positions, king_row, king_col-1) and not self.white_walks_in_check(self.piece_positions, king_row, king_col-2) and not self.white_walks_in_check(self.piece_positions, king_row, king_col-3):
                        if not self.white_king_moved:
                            self.white_long_castle = True
                            self.possible_moves[king_row][king_col-4] = True

            if king_row==7 and king_col==4 and self.piece_positions[king_row][king_col-4] == 'white_rook':   #short castle
                if not self.piece_positions[king_row][king_col+1] and not self.piece_positions[king_row][king_col+2]:
                    if not self.white_walks_in_check(self.piece_positions, king_row, king_col) and not self.white_walks_in_check(self.piece_positions, king_row, king_col+1) and not self.white_walks_in_check(self.piece_positions, king_row, king_col+2):
                        if not self.white_king_moved:
                            self.white_short_castle = True
                            self.possible_moves[king_row][king_col+3] = True
                        
            for i in range(king_row - 1, king_row + 2):
                for j in range(king_col - 1, king_col + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and not (i == king_row and j == king_col):
                        if not self.is_white(self.piece_positions[i][j]) and not self.white_walks_in_check(self.piece_positions, i, j):
                            self.possible_moves[i][j] = True

        elif self.board.current_player == 'black' and self.piece_positions[king_row][king_col] == 'black_king':

            if king_row==0 and king_col==4 and self.piece_positions[king_row][king_col-4] == 'black_rook':   #long castle
                if not self.piece_positions[king_row][king_col-1] and not self.piece_positions[king_row][king_col-2] and not self.piece_positions[king_row][king_col-3]:
                    if not self.black_walks_in_check(self.piece_positions, king_row, king_col) and not self.black_walks_in_check(self.piece_positions, king_row, king_col-1) and not self.black_walks_in_check(self.piece_positions, king_row, king_col-2) and not self.black_walks_in_check(self.piece_positions, king_row, king_col-3):
                        if not self.black_king_moved:
                            self.black_long_castle = True
                            self.possible_moves[king_row][king_col-4] = True

            if king_row==0 and king_col==4 and self.piece_positions[king_row][king_col-4] == 'black_rook':   #short castle
                if not self.piece_positions[king_row][king_col+1] and not self.piece_positions[king_row][king_col+2]:
                    if not self.black_walks_in_check(self.piece_positions, king_row, king_col) and not self.black_walks_in_check(self.piece_positions, king_row, king_col+1) and not self.black_walks_in_check(self.piece_positions, king_row, king_col+2):
                        if not self.black_king_moved:
                            self.black_short_castle = True
                            self.possible_moves[king_row][king_col+3] = True
                            
            for i in range(king_row - 1, king_row + 2):
                for j in range(king_col - 1, king_col + 2):
                    if 0 <= i < 8 and 0 <= j < 8 and not (i == king_row and j == king_col):
                        if not self.is_black(self.piece_positions[i][j]) and not self.black_walks_in_check(self.piece_positions, i, j):
                            self.possible_moves[i][j] = True
                
        self.highlight_possible_moves()

    def move(self, king_r, king_c, new_r, new_c):
        offset = abs(king_c - new_c)

        if self.possible_moves[new_r][new_c] == True and offset<2:
            if self.piece_positions[king_r][king_c] == 'white_king':
                self.piece_positions[new_r][new_c] = 'white_king'
                self.white_king_moved = True
            elif self.piece_positions[king_r][king_c] == 'black_king':
                self.piece_positions[new_r][new_c] = 'black_king'
                self.black_king_moved = True

            self.piece_positions[king_r][king_c] = None
            self.move_piece_on_board(king_r, king_c, new_r, new_c)
            self.switch_player_turn()

        elif self.white_long_castle and self.possible_moves[new_r][new_c] == True:
            self.white_l_castle(king_r, king_c)
            self.switch_player_turn()
            self.white_king_moved = True
        elif self.white_short_castle and self.possible_moves[new_r][new_c] == True:
            self.white_s_castle(king_r, king_c)
            self.switch_player_turn()
            self.white_king_moved = True

        elif self.black_long_castle and self.possible_moves[new_r][new_c] == True:
            self.black_l_castle(king_r, king_c)
            self.switch_player_turn()
            self.black_king_moved = True
        elif self.black_short_castle and self.possible_moves[new_r][new_c] == True:
            self.black_s_castle(king_r, king_c)
            self.switch_player_turn()
            self.black_king_moved = True