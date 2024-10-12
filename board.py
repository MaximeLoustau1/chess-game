import pygame

piece_images = {
    'black_pawn': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_pawn.png",
    'black_bishop': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_bishop.png",
    'black_knight': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_knight.png",
    'black_king': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_king.png",
    'black_queen': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_queen.png",
    'black_rook': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\black_rook.png",
    'white_pawn': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_pawn.png",
    'white_bishop': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_bishop.png",
    'white_knight': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_knight.png",
    'white_king': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_king.png",
    'white_queen': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_queen.png",
    'white_rook': "C:\\Users\\rohan\\Desktop\\Coding Projects\\ChessGame\\white_rook.png"
}

class Board:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.green_color = (1, 100, 22)
        self.white_color = (255, 255, 255)
        self.beige_color = (245, 245, 220)
        self.columns = 8
        self.rows = 8
        self.block_size = self.width // 8
        self.selected_piece_position = None
        self.clicked_cells = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        self.piece_positions = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'white'
        self.piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

    def setup_board(self):
        
        pygame.display.set_caption('CHESS GAME')
        self.screen.fill(self.white_color)
        
        self.draw_chessboard()
        self.initialize_black_pieces()
        self.initialize_white_pieces()
        
        pygame.display.flip()

    def draw_chessboard(self):
        
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                
                if (x + y) % 2 == 0:
                    color = self.beige_color
                else:
                    color = self.green_color

                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.display.update()

    def place_piece_at_position(self, col, row, piece_name):
        
        size = self.width // 8
        
        piece_img = pygame.image.load(piece_images.get(piece_name, ""))
        piece_img = pygame.transform.scale(piece_img, (size, size))
        self.screen.blit(piece_img, (row * size, col * size))
        
        pygame.display.update()
        
    def initialize_black_pieces(self):
        
        for col in range(8):
            piece_name = f'black_{self.piece_order[col]}' if col < 8 else 'black_pawn'
            self.place_piece_at_position(0, col, piece_name)
            self.piece_positions[0][col] = piece_name

        for row in range(8):
            piece_name = 'black_pawn'
            self.place_piece_at_position(1, row, piece_name)
            self.piece_positions[1][row] = piece_name

    def initialize_white_pieces(self):
        
        for col in range(8):
            piece_name = f'white_{self.piece_order[col]}' if col < 8 else 'white_pawn'
            self.place_piece_at_position(7, col, piece_name)
            self.piece_positions[7][col] = piece_name

        for row in range(8):
            piece_name = 'white_pawn'
            self.place_piece_at_position(6, row, piece_name)
            self.piece_positions[6][row] = piece_name

    def highlight_selected_cell(self, row, col):      #keeps track of what piece is clicked on and if it's clicked for the first time
        counter = self.count_clicked_cells()          #updates the images on the board to represent current state of board matrix

        if self.selected_piece_position:
            selected_row, selected_col = self.selected_piece_position
            self.clicked_cells[selected_row][selected_col] = False
            self.selected_piece_position = None 

        if self.clicked_cells[row][col] == True or counter > 0:
            if (row + col) % 2 == 0:
                color = self.beige_color
            else:
                color = self.green_color
            self.clicked_cells[row][col] = False

        x = col * self.block_size
        y = row * self.block_size

        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, color, rect)

        self.update_piece_positions_on_board()
        pygame.display.flip()

    def count_clicked_cells(self):
        
        counter = 0
        for i in range(self.columns):
            for j in range(self.rows):
                if self.clicked_cells[i][j] == True:
                    counter += 1
        return counter

    def update_piece_positions_on_board(self):
        
        for row in range(self.rows):
            for col in range(self.columns):
                piece_name = self.piece_positions[row][col]
                if piece_name:
                    self.place_piece_at_position(row, col, piece_name)
