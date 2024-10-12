#TODO:
#   - implement view_last_board_state functionality ?!
#   - option to choose what piece to promote pawn to
#   - start and end game loading screen
#   - show possible moves for castling should display the squares where the king and rook will be
#   - when in check, it doesnt let other pieces block the path, it only lets other piece move to take the attacking piece
#   - if king can move anywhere but checked squares, make other pieces move anywhere but not checked squares
#   - prevent pinned pieces from moving

##next step would be to handle double checks, pinned pieces and stalemates
##stalemate::>>make a function that checks if white/black has any possible moves that won't be king_walks_in_check() and if None then stalemate

import pygame
from gameLogic import Game

if __name__ == '__main__':

    pygame.init()
    game = Game()

    game.handle_events()

