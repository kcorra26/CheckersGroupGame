'''
sprites

for gui purposes
'''
import pygame
from mocks import Piece
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)

class PieceSprite(pygame.sprite.Sprite):
    '''
    This class represents the sprites of all of the checkers pieces and derives from
    Sprite class in pygame
    '''
    def __init__(self, piece: Piece, sq_size:float):
        '''
        initialization function for PieceSprite class

        Args:
            piece: the Piece object that is represented
            size: the size of the sprites
        '''
        pygame.sprite.Sprite.__init__(self)
        self.piece = piece
        self.team = piece.team 
        self.is_king = piece.is_king
        self.sq_size = sq_size
        if self.team == "RED":
            if self.is_king:
                self.image = pygame.transform.scale(pygame.image.load('red_king.png'), (sq_size,sq_size))
            else:
                self.image = pygame.transform.scale(pygame.image.load('red.png'), (sq_size, sq_size))
        else:
            if self.is_king:
                self.image = pygame.transform.scale(pygame.image.load('black_king.png'), (sq_size, sq_size))
            else:
                self.image = pygame.transform.scale(pygame.image.load('black.png'), (sq_size,sq_size))
        self.rect = self.image.get_rect()

    def update(self):
        '''
        called in every frame - updates the position of the sprite
        piece.pos = (row, col) = (y, x)
        '''
        self.rect.x = self.sq_size * self.piece.col
        self.rect.y = self.sq_size * self.piece.row
