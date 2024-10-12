from pieces import Piece

class Pawn(Piece):
    def __init__(self, piece_positions, board):
        super().__init__(board)
        self.piece_positions = piece_positions
        self.last_piece_moved = None
        self.l_p_m_column = None
        self.l_p_m_up_by = None
        self.left_en_passant = False
        self.right_en_passant = False
        self.board = board


    def white_pawn_moves(self, pawn_row, pawn_col):
        #pawn moves up
        if self.piece_positions[pawn_row - 1][pawn_col] is None:
            self.possible_moves[pawn_row - 1][pawn_col] = True
        if pawn_row == 6 and self.piece_positions[pawn_row - 2][pawn_col] is None and self.piece_positions[pawn_row - 1][pawn_col] is None:
            self.possible_moves[pawn_row - 2][pawn_col] = True
                
        #pawn eats
        self.white_pawn_eats(pawn_row, pawn_col)
                
        #pawn en passant   
        if self.last_piece_moved == 'black_pawn' and self.l_p_m_up_by == 2 and pawn_row == 3:
            if pawn_col > 0 and self.piece_positions[pawn_row][pawn_col-1] and self.l_p_m_column == pawn_col-1 and self.piece_positions[pawn_row-1][pawn_col-1] is None:
                self.possible_moves[pawn_row - 1][pawn_col - 1] = True
                self.left_en_passant = True
            elif pawn_col < 7 and self.piece_positions[pawn_row][pawn_col+1] and self.l_p_m_column == pawn_col+1 and self.piece_positions[pawn_row-1][pawn_col+1] is None:
                self.possible_moves[pawn_row - 1][pawn_col + 1] = True
                self.right_en_passant = True

    def black_pawn_moves(self, pawn_row, pawn_col):
        
            #pawn moves up
            if self.piece_positions[pawn_row + 1][pawn_col] is None:
                self.possible_moves[pawn_row + 1][pawn_col] = True
            if pawn_row == 1 and self.piece_positions[pawn_row + 2][pawn_col] is None and self.piece_positions[pawn_row + 1][pawn_col] is None:
                self.possible_moves[pawn_row + 2][pawn_col] = True

            #pawn eats
            self.black_pawn_eats(pawn_row, pawn_col)
                
            #pawn en passant
            if self.last_piece_moved == 'white_pawn' and self.l_p_m_up_by == 2 and pawn_row == 4:
                if pawn_col > 0 and self.piece_positions[pawn_row][pawn_col-1] and self.l_p_m_column == pawn_col-1 and self.piece_positions[pawn_row+1][pawn_col-1] is None:
                    self.possible_moves[pawn_row + 1][pawn_col - 1] = True
                    self.left_en_passant = True
                elif pawn_col < 7 and self.piece_positions[pawn_row][pawn_col+1] and self.l_p_m_column == pawn_col+1 and self.piece_positions[pawn_row+1][pawn_col+1] is None:
                    self.possible_moves[pawn_row + 1][pawn_col + 1] = True
                    self.right_en_passant = True
                        
    def show_possible_moves(self, pawn_row, pawn_col):
                
        self.clear_possible_moves()

        if self.board.current_player == 'white' and self.piece_positions[pawn_row][pawn_col] == 'white_pawn':
            self.white_pawn_moves(pawn_row, pawn_col)
            king_r, king_c = self.return_white_king_pos()
            if self.white_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(pawn_row, pawn_col, king_r, king_c)

        elif self.board.current_player == 'black' and self.piece_positions[pawn_row][pawn_col] == 'black_pawn':
            self.black_pawn_moves(pawn_row, pawn_col)
            king_r, king_c = self.return_black_king_pos()
            if self.black_walks_in_check(self.piece_positions, king_r, king_c):
                self.remove_moves_putting_king_in_check(pawn_row, pawn_col, king_r, king_c)
            
        self.highlight_possible_moves()

    def move(self, pawn_r, pawn_c, new_r, new_c):
        
        if self.possible_moves[new_r][new_c]:

            #en passant
            if self.left_en_passant and self.piece_positions[pawn_r][pawn_c] == 'white_pawn':
                self.piece_positions[pawn_r][pawn_c - 1] = None
                self.piece_positions[pawn_r - 1][pawn_c - 1] = 'white_pawn'
                self.left_en_passant = False

            if self.right_en_passant and self.piece_positions[pawn_r][pawn_c] == 'white_pawn':
                self.piece_positions[pawn_r][pawn_c + 1] = None
                self.piece_positions[pawn_r - 1][pawn_c + 1] = 'white_pawn'
                self.right_en_passant = False

            if self.left_en_passant and self.piece_positions[pawn_r][pawn_c] == 'black_pawn':
                self.piece_positions[pawn_r][pawn_c - 1] = None
                self.piece_positions[pawn_r + 1][pawn_c - 1] = 'black_pawn'
                self.left_en_passant = False

            if self.right_en_passant and self.piece_positions[pawn_r][pawn_c] == 'black_pawn':
                self.piece_positions[pawn_r][pawn_c + 1] = None
                self.piece_positions[pawn_r + 1][pawn_c + 1] = 'black_pawn'
                self.right_en_passant = False
            
            #promote pawn
            if new_r == 0 and self.piece_positions[pawn_r][pawn_c] == 'white_pawn':
                self.piece_positions[new_r][new_c] = 'white_queen'   

            elif new_r == 7 and self.piece_positions[pawn_r][pawn_c] == 'black_pawn':
                self.piece_positions[new_r][new_c] = 'black_queen'

            #normal movement   
            else:
                if self.piece_positions[pawn_r][pawn_c] == 'white_pawn':
                    self.piece_positions[new_r][new_c] = 'white_pawn'

                elif self.piece_positions[pawn_r][pawn_c] == 'black_pawn':
                    self.piece_positions[new_r][new_c] = 'black_pawn'
                    
            self.piece_positions[pawn_r][pawn_c] = None
            self.last_piece_moved = None
            self.l_p_m_column = None
            
            self.move_piece_on_board(pawn_r, pawn_c, new_r, new_c)
            self.last_piece_moved = self.piece_positions[new_r][new_c]
            self.l_p_m_column = pawn_c
            self.l_p_m_up_by = abs(pawn_r - new_r)
            self.switch_player_turn()

        else:
            pass