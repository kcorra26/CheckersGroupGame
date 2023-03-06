'''
sprites

a file to hold the sprite class, for gui purposes

Sources:
    the piece images are from Adobe Stock
    link: https://stock.adobe.com/nz/images/checkers-board-game-pieces-vector-illustration-icon-symbol-graphic/249920338?start-checkout=1&content-id=249920338
'''
import pygame
from mocks import Piece

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
        if self.team == "Red":
            if self.is_king:
                self.image = pygame.transform.scale(pygame.image.load('src/red_king.png'), (sq_size,sq_size))
            else:
                self.image = pygame.transform.scale(pygame.image.load('src/red.png'), (sq_size, sq_size))
        else:
            if self.is_king:
                self.image = pygame.transform.scale(pygame.image.load('src/black_king.png'), (sq_size, sq_size))
            else:
                self.image = pygame.transform.scale(pygame.image.load('src/black.png'), (sq_size,sq_size))
        self.rect = self.image.get_rect()

    def update(self):  
        '''
        called in every frame - updates the position of the sprite
        piece.pos = (row, col) = (y, x)

        args:
            None

        '''
        self.rect.x = self.sq_size * self.piece.x_pos
        self.rect.y = self.sq_size * self.piece.y_pos
        if self.piece.is_king:
            if self.team == 'Red':
                self.image = pygame.transform.scale(pygame.image.load('src/red_king.png'), (self.sq_size,self.sq_size))
            else:
                self.image = pygame.transform.scale(pygame.image.load('src/black_king.png'), (self.sq_size, self.sq_size))
