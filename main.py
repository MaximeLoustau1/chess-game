# ALL PIECES MOVEMENT IMPLEMENTED
#NEXT STEP:
#   - implement view_last_board_state functionality ?!
#   - option to choose what piece to promote pawn to
#   - start and end game loading screen
#   - show possible moves for castling should display the squares where the king and rook will be
#   - when in check, it doesnt let other pieces block the path, it only lets other piece move to take the attacking piece
#   - if king can move anywhere but checked squares, make other pieces move anywhere but not checked squares
#   - prevent pinned pieces from moving

##FIX ISSUE WITH CHANGING WINDOW SIZE

##in the simulate moves and check, if the attacking piece is not a pawn or a knight then make a function that calculates the path of the attacking piece from its
##position to the position of the king and see if any piece can go on that path

##next step would be to handle double checks, pinned pieces and stalemates
##stalemate::>>make a function that checks if white/black has any possible moves that won't be king_walks_in_check() and if None then stalemate

import pygame
from gameLogic import Game

if __name__ == '__main__':

    pygame.init()
    game = Game()

    game.handle_events()

