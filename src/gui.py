'''
Pygame and GUI Implementation
'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

from mocks import StubCheckerboard, Piece, TeamColor
#from checkers import Board
#from checkers import Board, TeamColor

WIDTH = 800
HEIGHT = 800

#colors
WHITE = (255, 255,255)
LIGHT_BROWN =(188,158,130)
DARK_BROWN = (155, 103,60)
BLACK = (0,0,0)
RED = (170,0,20)
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
        '''
        self.rect.x = self.sq_size * self.piece.pos[0]
        self.rect.y = self.sq_size * self.piece.pos[1]

"""class PossibleMovesSprite():
    '''
    This class represents the moves that are possible for a certain sprite
    '''
    def __init__(self, pos, sq_size):
        '''
        constructor for a PossibleMovesSprite

        Args:
            pos(tuple): a touple representing the row, col 
            sq_size(int): the size of the board squares 
        '''
        img_size = sq_size/2
        self.image = pygame.Surface([img_size, img_size])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.ellipse(self.image, YELLOW, [pos[1]*sq_size, pos[0]*sq_size, img_size-img_size/2, img_size+img_size/2])"""

def calc_sq_size(board):
    '''
    calaculates square size

    Args: 
        board: the current board

    Returns (float) the sq_size of the board
    '''
    sq_size = WIDTH // board.width
    return sq_size

def show_moves(board:StubCheckerboard, piece:Piece, window):
    '''
    generates sprites for all possible moves
    '''
    moves = board.list_moves(piece)
    for loc in moves: #loc is (row, col)
        x_pos = loc[1] * calc_sq_size(board)
        y_pos = loc[0] * calc_sq_size(board)
        pygame.draw.circle(window, YELLOW, )


#draw board methods
def __draw_empty_board(window, board):
    '''
    Draws checkerboard without pieces

    Args:
        window: the pygame window where the board is drawn
        board: the board that is being represented
        sq_size: the size of every square
    '''
    ROWS = board.width
    SQ_SIZE = calc_sq_size(board)

    window.fill(BLACK)
    for row in range(ROWS):
        for col in range(row%2, ROWS, 2):
            pygame.draw.rect(window, RED, (row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_board (window, board, sprite_list):
    '''
    draws checkerboard with sprites

    Args: 
        window: the pygame window where board is drawn
        board: the board being represented
        sq_size: the size of the squares
        sprite_list: current sprite list (at this time in game)
    '''
    __draw_empty_board(window, board)
    sprite_list.draw(window)


def init_sprites(board: StubCheckerboard):
    '''
    this function initializes all Pieces and returns a list of all PieceSprites

    args: 
        board: a board/game which contains a list of all Pieces

    retuns:
        all_sprites_list: a list of all PieceSprites on the board
    '''
    all_sprites_list = pygame.sprite.Group()
    all_pieces = board.red_pieces + board.black_pieces
    size = calc_sq_size(board)

    for piece in all_pieces:
        sprite = PieceSprite(piece, size)
        all_sprites_list.add(sprite)
    all_sprites_list.update()
    return all_sprites_list



def play_checkers(board:StubCheckerboard):

    ROWS = board.width
    SQ_SIZE = WIDTH // ROWS
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    pygame.display.update()

    all_sprites_list = init_sprites(board)
    curr_player = 'BLACK'

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // SQ_SIZE
                col = pos[0] //SQ_SIZE
                piece = board.get_piece(col, row)
                if piece.team == curr_player:
                    show_moves(board, piece, SQ_SIZE, display)
                #board.move_piece((col, row), (0,0)) #need to allow user to decide where piece moves
                
            #need one to see possible locations
            
            #switch current player
            if curr_player == 'BLACK':
                curr_player = 'RED'
            else:
                curr_player = "BLACK"

            all_sprites_list.update()
            draw_board(display, board, all_sprites_list)
            pygame.display.update()

    pygame.quit()
    quit()

#sample board
ex_board = StubCheckerboard()
play_checkers(ex_board)