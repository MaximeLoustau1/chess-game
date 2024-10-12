#TODO:
#   - implement view_last_board_state functionality 
#   - option to choose what piece to promote pawn to
#   - show possible moves for castling should display the squares where the king and rook will be

import pygame
from gameLogic import Game

if __name__ == '__main__':

    pygame.init()
    game = Game()

    game.handle_events()

