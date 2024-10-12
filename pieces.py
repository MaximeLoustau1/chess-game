import pygame
from abc import ABC, abstractmethod
from board import piece_images

class Piece(ABC):
    def __init__(self, board):
        self.board = board
        self.row = 8
        self.col = 8
        self.possible_moves = [[False for _ in range(self.row)] for _ in range(self.col)]
        self.block_size = board.block_size
        self.black = (0,0,0)
        self.rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        self.bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.queen_directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.threatening_moves = [[False] * 8 for _ in range(8)]
        self.check_for_check = False
        self.white_check = False
        self.black_check = False
        self.board = board
        self.checking_piece = None
        
    @abstractmethod
    def show_possible_moves(self, board):
        pass

    @abstractmethod
    def move(self, pawn_r, pawn_c, new_r, new_c):
        pass

    def switch_player_turn(self):

        if self.board.current_player == 'white':
            self.board.current_player = 'black'
        else:
            self.board.current_player = 'white'
    
    def king_walks_in_king(self, row, col):
        if row<7:
            self.threatening_moves[row+1][col] = True
            if col>0:
                self.threatening_moves[row+1][col-1] = True
            if col<7:
                self.threatening_moves[row+1][col+1] = True
        if row>0:
            self.threatening_moves[row-1][col] = True
            if col>0:
                self.threatening_moves[row-1][col-1] = True
            if col<7:
                self.threatening_moves[row-1][col+1] = True
        if col<7:
            self.threatening_moves[row][col+1] = True
        if col>0:
            self.threatening_moves[row][col-1] = True 

    def white_walks_in_check(self, piece_position, king_row, king_col):
        self.white_check = False
        # Reset threatening moves before checking
        self.threatening_moves = [[False] * 8 for _ in range(8)]
        self.check_for_check = True

        # Iterate over the copied board to simulate black pieces' moves
        for row in range(self.row):
            for col in range(self.col):
                if piece_position[row][col] == 'black_pawn':
                    self.black_pawn_check(row, col)
                elif piece_position[row][col] == 'black_knight':
                    self.black_knight_moves(row, col, self.knight_moves)
                elif piece_position[row][col] == 'black_bishop':
                    self.black_depth_move(self.bishop_directions, row, col)
                elif piece_position[row][col] == 'black_rook':
                    self.black_depth_move(self.rook_directions, row, col)
                elif piece_position[row][col] == 'black_queen':
                    self.black_depth_move(self.queen_directions, row, col)
                elif piece_position[row][col] == 'black_king':
                    self.king_walks_in_king(row, col)

        # Check if the white king's position is in the list of threatening moves
        if self.threatening_moves[king_row][king_col]:
            self.white_check = True

        self.check_for_check = False

        return self.white_check

    def black_walks_in_check(self, piece_positions, king_row, king_col):
        self.black_check = False
        self.threatening_moves = [[False] * 8 for _ in range(8)]
        self.check_for_check = True

        for row in range(self.row):
            for col in range(self.col):
                if piece_positions[row][col] == 'white_pawn':
                    self.white_pawn_check(row, col)
                elif piece_positions[row][col] == 'white_knight':
                    self.white_knight_moves(row, col, self.knight_moves)
                elif piece_positions[row][col] == 'white_bishop':
                    self.white_depth_move(self.bishop_directions, row, col)
                elif piece_positions[row][col] == 'white_rook':
                    self.white_depth_move(self.rook_directions, row, col)
                elif piece_positions[row][col] == 'white_queen':
                    self.white_depth_move(self.queen_directions, row, col)
                elif piece_positions[row][col] == 'white_king':
                    self.king_walks_in_king(row, col)

        if self.threatening_moves[king_row][king_col]:
            self.black_check = True

        self.check_for_check = False

        return self.black_check

    def return_white_king_pos(self):

        for row in range(self.row):
            for col in range(self.col):
                if self.piece_positions[row][col] == 'white_king':
                    return (row, col)

    def return_black_king_pos(self):

        for row in range(self.row):
            for col in range(self.col):
                if self.piece_positions[row][col] == 'black_king':
                    return (row, col)
                
    def black_knight_moves(self, knight_row, knight_col, knight_moves):
        for dr, dc in knight_moves:
            new_row, new_col = knight_row + dr, knight_col + dc

            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.columns:
                if not self.is_black(self.piece_positions[new_row][new_col]):
                    if not self.check_for_check:
                        self.possible_moves[new_row][new_col] = True
                    else:
                        self.threatening_moves[new_row][new_col] = True


    def white_knight_moves(self, knight_row, knight_col, knight_moves):
        for dr, dc in knight_moves:
            new_row, new_col = knight_row + dr, knight_col + dc

            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.columns:
                if not self.is_white(self.piece_positions[new_row][new_col]):
                    if not self.check_for_check:
                        self.possible_moves[new_row][new_col] = True
                    else:
                        self.threatening_moves[new_row][new_col] = True


    def black_pawn_eats(self, pawn_row, pawn_col):
        if pawn_col < 7:   
            if self.piece_positions[pawn_row + 1][pawn_col + 1] and self.is_white(self.piece_positions[pawn_row + 1][pawn_col + 1]):
                self.possible_moves[pawn_row + 1][pawn_col + 1] = True

        if pawn_col > 0:
            if self.piece_positions[pawn_row + 1][pawn_col - 1] and self.is_white(self.piece_positions[pawn_row + 1][pawn_col - 1]):
                self.possible_moves[pawn_row + 1][pawn_col - 1] = True

    def white_pawn_eats(self, pawn_row, pawn_col):
        if pawn_col < 7:   
            if self.piece_positions[pawn_row - 1][pawn_col + 1] and self.is_black(self.piece_positions[pawn_row - 1][pawn_col + 1]):
                self.possible_moves[pawn_row - 1][pawn_col + 1] = True

        if pawn_col > 0:
            if self.piece_positions[pawn_row - 1][pawn_col - 1] and self.is_black(self.piece_positions[pawn_row - 1][pawn_col - 1]):
                self.possible_moves[pawn_row - 1][pawn_col - 1] = True

    def black_pawn_check(self, pawn_row, pawn_col):
        if pawn_col < 7:
            if not self.is_black(self.piece_positions[pawn_row + 1][pawn_col + 1]):
                self.threatening_moves[pawn_row + 1][pawn_col + 1] = True
        if pawn_col > 0:
            if not self.is_black(self.piece_positions[pawn_row + 1][pawn_col - 1]):
                self.threatening_moves[pawn_row + 1][pawn_col - 1] = True

    def white_pawn_check(self, pawn_row, pawn_col):
        if pawn_col < 7:
            if not self.is_white(self.piece_positions[pawn_row - 1][pawn_col + 1]):
                self.threatening_moves[pawn_row - 1][pawn_col + 1] = True
        if pawn_col > 0:
            if not self.is_white(self.piece_positions[pawn_row - 1][pawn_col - 1]):
                self.threatening_moves[pawn_row - 1][pawn_col - 1] = True

    def highlight_possible_moves(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.possible_moves[i][j] == True and self.piece_positions[i][j] is None:
                    x = j * self.block_size
                    y = i * self.block_size
                    center_x = x + self.block_size // 2
                    center_y = y + self.block_size // 2
                    pygame.draw.circle(self.board.screen, self.black, (center_x, center_y), self.block_size // 8)

        pygame.display.update()


    def clear_possible_moves(self):
        
        for i in range(self.row):         #reset all empty squares on the board
            for j in range(self.col):
                if self.piece_positions[i][j] is None:
                    
                    empty_square = pygame.Surface((self.block_size, self.block_size))
                    empty_square.fill(self.board.beige_color if (j + i) % 2 == 0 else self.board.green_color)
                    self.board.screen.blit(empty_square, (j * self.block_size, i * self.block_size))

        for i in range(self.row):         #reset all values in possible_moves array
            for j in range(self.col):
                self.possible_moves[i][j] = False
                    
        pygame.display.update()
    
    #def white_stalemate(self, from_row, from_col, to_row, to_col):
                                                                   #go through all white moves, if none return True, else return false


    def move_piece_on_board(self, from_row, from_col, to_row, to_col):    #move piece image 
                
        piece_name = self.piece_positions[to_row][to_col]
        piece_img = pygame.image.load(piece_images.get(piece_name, ""))
        piece_img = pygame.transform.scale(piece_img, (self.block_size, self.block_size))
        self.board.screen.blit(piece_img, (to_col * self.block_size, to_row * self.block_size))

        empty_square = pygame.Surface((self.block_size, self.block_size))
        empty_square.fill(self.board.green_color if (to_row + to_col) % 2 == 0 else self.board.beige_color)
        self.board.screen.blit(empty_square, (from_col * self.block_size, from_row * self.block_size))

        pygame.display.update()

    def white_depth_move(self, directions, piece_row, piece_col):    # movement for rook, bishop and queen
        for dr, dc in directions:
            row, col = piece_row + dr, piece_col + dc

            while 0 <= row <= 7 and 0 <= col <= 7:
                if self.check_for_check:                             # consider moves past the king as checked squares
                    if self.piece_positions[row][col] is None:
                        self.threatening_moves[row][col] = True
                    elif self.is_black(self.piece_positions[row][col]) and self.piece_positions[row][col] == 'black_king':
                        self.threatening_moves[row][col] = True
                    elif self.is_black(self.piece_positions[row][col]) and self.piece_positions[row][col] != 'black_king':
                        self.threatening_moves[row][col] = True
                        break
                    else:
                        break
                else:
                    if self.piece_positions[row][col] is None:
                            self.possible_moves[row][col] = True
                    elif self.is_black(self.piece_positions[row][col]):
                        self.possible_moves[row][col] = True
                        break
                    else:
                        break

                row += dr
                col += dc
    
    def white_dth_move(self, piece_positions, directions, piece_row, piece_col):    # movement for rook, bishop and queen
        for dr, dc in directions:
            row, col = piece_row + dr, piece_col + dc

            while 0 <= row <= 7 and 0 <= col <= 7:
                if self.check_for_check:                             # consider moves past the king as checked squares
                    if piece_positions[row][col] is None:
                        self.threatening_moves[row][col] = True
                    elif self.is_black(piece_positions[row][col]) and piece_positions[row][col] == 'black_king':
                        self.threatening_moves[row][col] = True
                    elif self.is_black(piece_positions[row][col]) and piece_positions[row][col] != 'black_king':
                        self.threatening_moves[row][col] = True
                        break
                    else:
                        break
                else:
                    if piece_positions[row][col] is None:
                            self.possible_moves[row][col] = True
                    elif self.is_black(piece_positions[row][col]):
                        self.possible_moves[row][col] = True
                        break
                    else:
                        break

                row += dr
                col += dc
                
    def black_depth_move(self, directions, piece_row, piece_col):
        for dr, dc in directions:
            row, col = piece_row + dr, piece_col + dc

            while 0 <= row <= 7 and 0 <= col <= 7:
                if self.check_for_check:
                    if self.piece_positions[row][col] is None:
                        self.threatening_moves[row][col] = True
                    elif self.is_white(self.piece_positions[row][col]) and self.piece_positions[row][col] == 'white_king':
                        self.threatening_moves[row][col] = True
                    elif self.is_white(self.piece_positions[row][col]) and self.piece_positions[row][col] != 'white_king':
                        self.threatening_moves[row][col] = True
                        break
                    else:
                        break
                else:
                    if self.piece_positions[row][col] is None:
                            self.possible_moves[row][col] = True
                    elif self.is_white(self.piece_positions[row][col]):
                        self.possible_moves[row][col] = True
                        break
                    else:
                        break

                row += dr
                col += dc

    def is_white(self, piece):
        return piece in ['white_rook', 'white_bishop', 'white_queen', 'white_king', 'white_pawn', 'white_knight']

    def is_black(self, piece):
        return piece in ['black_rook', 'black_bishop', 'black_queen', 'black_king', 'black_pawn', 'black_knight']



    def simulate_move_and_check(self, new_r, new_c, piece_row, piece_col, king_r, king_c):
        temp_piece_positions = [row[:] for row in self.piece_positions]
        temp_piece_positions[new_r][new_c] = temp_piece_positions[piece_row][piece_col]
        temp_piece_positions[piece_row][piece_col] = None


        if self.is_white(temp_piece_positions[new_r][new_c]):
            if self.white_walks_in_check(temp_piece_positions, king_r, king_c):
                return True
        else:
            if self.black_walks_in_check(temp_piece_positions, king_r, king_c):
                return True

        return False

    def remove_moves_putting_king_in_check(self, piece_row, piece_col, king_r, king_c):
        for r in range(len(self.possible_moves)):
            for c in range(len(self.possible_moves[r])):
                if self.possible_moves[r][c]:
                    if self.simulate_move_and_check(r, c, piece_row, piece_col, king_r, king_c):
                        self.possible_moves[r][c] = False
    
