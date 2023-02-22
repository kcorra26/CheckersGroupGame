'''
Pygame and GUI Implementation
'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

from mocks import StubCheckerboard, Piece
from sprites import PieceSprite
#from checkers import Board, Game

WIDTH = HEIGHT = 800

#colors
WHITE = (255, 255,255)
LIGHT_BROWN =(188,158,130)
DARK_BROWN = (155, 103,60)
BLACK = (0,0,0)
RED = (170,0,20)
YELLOW = (255, 204, 0)

class GUIPlayer():

    def __init__(self, board):
        """
        init function for GUI Player

        Args: 
            board: the board being played
        """
        self.board = board
        self.sq_size = WIDTH // board.width
        self.curr_player = 'BLACK'
        self.ROWS = self.board.width
        self.all_sprites_list = pygame.sprite.Group()
        self.window = None
        self.selected_piece = None

    def init_game (self):
        '''
        initializes the display for the game

        Args: None
        Returns None
        '''
        pygame.init()
        display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window = display
        pygame.display.set_caption('Checkers')
        pygame.display.update()
    
    def init_sprites(self):
        '''
        this function initializes all Pieces and returns a list of all PieceSprites

        args: 
            board: a board/game which contains a list of all Pieces

        retuns:
            all_sprites_list: a list of all PieceSprites on the board
        '''
        all_pieces = self.board.red_pieces + self.board.black_pieces

        for piece in all_pieces:
            sprite = PieceSprite(piece, self.sq_size)
            self.all_sprites_list.add(sprite)
        self.all_sprites_list.update()
        return 

    #draw board methods
    def __draw_empty_board(self):
        '''
        Draws checkerboard without pieces, helper function for draw_board()

        Args:
            None
        '''
        self.window.fill(BLACK)
        for row in range(self.ROWS):
            for col in range(row%2, self.ROWS, 2):
                pygame.draw.rect(self.window, RED, (row*self.sq_size, col*self.sq_size, self.sq_size, self.sq_size))

    def __draw_highlighted_board(self):
        '''
        Draws checkerboard without pieces but with possible moves highlighted

        Args:
            None
        '''
        moves = self.board.list_moves(self.selected_piece)
        for row in range(self.ROWS):
            for col in range(self.ROWS):
                if (row, col) in moves:
                    pygame.draw.rect(self.window, YELLOW, (col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))
    
    def draw_board (self):
        '''
        draws checkerboard with sprites

        Args: 
            window: the pygame window where board is drawn
            board: the board being represented
            sq_size: the size of the squares
            sprite_list: current sprite list (at this time in game)
        '''
        self.__draw_empty_board()
        if self.selected_piece is not None:
            self.__draw_highlighted_board()
        self.all_sprites_list.draw(self.window)
        pygame.display.update()
        return

    def move_selected_piece(self, row, col):
        pos_moves = self.board.list_moves(self.selected_piece)
        print(pos_moves, row, col)
        if (row, col) in pos_moves:
            print('move is possible')
            sel_piece = self.selected_piece
            print('selected_piece pos',sel_piece.pos)
            self.board.move_piece(sel_piece.pos, (row, col))
            self.all_sprites_list.update()
            self.switch_player()
        else:
            self.selected_piece = None

    def switch_player(self):
        '''
        switches the current player
        '''
        self.selected_piece = None
        if self.curr_player == 'BLACK':
            self.curr_player = 'RED'
        else:
            self.curr_player = "BLACK"
        return

    def play_checkers(self):
        self.init_game()
        self.init_sprites()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() #this pos in in (x,y)
                    row = pos[1] // self.sq_size #y-pos
                    col = pos[0] //self.sq_size #x-pos
                    if self.selected_piece is None:
                        print('MOUSEDOWN')
                        piece = self.board.get_piece(row, col)
                        if piece is None or piece.team != self.curr_player:
                            break
                        print('found a piece at MOUSE')
                        self.selected_piece = piece
                        print('set a selected piece')
                        self.draw_board() #draws possible moves
                    else:
                        print('there is a selected piece')
                        self.move_selected_piece(row, col)
                else:
                    self.draw_board()
        pygame.quit()
        quit()

#sample board
ex_board = StubCheckerboard()
player = GUIPlayer(ex_board)
player.play_checkers()