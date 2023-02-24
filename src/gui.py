'''
Pygame and GUI Implementation

Resources Consulted:
    https://github.com/techwithtim/Python-Checkers/tree/master/checkers
    - the implementation is completly different, but was helpful in thinking of the
    structure of the main pygame loop and the needed functions, such as switch_piece
    https://www.ucode.com/coding_classes_for_kids_honors_course/course-videos/pgd-sprite-groups-in-py-games
    - this was helpful in setting up the sprite groups
    http://programarcadegames.com/python_examples/show_file.php?file=moving_sprites.py
    - this was helpful in initializing the sprite class

'''
import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

from mocks import Piece, MockCheckerboard, MockGame
from sprites import PieceSprite
from bot import RandomBot, SmartBot

WIDTH = HEIGHT = 800

#colors
WHITE = (255, 255,255)
BLACK = (0,0,0)
RED = (170,0,20)
YELLOW = (255, 204, 0)
GREEN = (75, 139, 59)

class CheckersPlayer:
    '''
    simple class to store player information
    '''
    def __init__(self, bot = None):
        '''
        '''
        if bot == None:
            self.is_bot = False
        else:
            self.is_bot = True
        self.bot = bot
        self.color = None

class GUIPlayer():

    def __init__(self, game:MockGame, player_1: CheckersPlayer, player_2:CheckersPlayer):
        """
        init function for GUI Player

        args: 
            board: the board being played
        """
        self.game = game
        self.board = game.board
        self.ROWS = game.width
        self.sq_size = WIDTH // game.width

        #players
        player_1.color = 'Black'
        player_2.color = 'Red'
        self.players = [player_1, player_2]
        self.curr_player = self.players[0]

        #attributes for game play
        self.all_sprites_list = pygame.sprite.Group()
        self.window = None
        self.selected_piece = None

    def init_game (self):
        '''
        initializes the display and the sprites for the game

        args: 
            None
        '''
        pygame.init()
        display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window = display
        pygame.display.set_caption('Checkers')
        self.init_sprites()
        pygame.display.update()
    
    def init_sprites(self):
        '''
        this function initializes all Pieces and add thems to all_piece_list

        args: 
            None
        '''
        all_pieces = self.game.red_pieces.union(self.game.black_pieces)

        for piece in all_pieces:
            sprite = PieceSprite(piece, self.sq_size)
            self.all_sprites_list.add(sprite)
        self.all_sprites_list.update()
        return 
    
    def update_sprites(self):
        '''
        updates the sprites by removing sprites whoose pieces are no longer in play
        and updating the locations of the remaining sprites
        '''
        pieces = self.game.red_pieces.union(self.game.black_pieces)
        for sprite in self.all_sprites_list:
            if sprite.piece not in pieces:
                sprite.kill() #will kill sprites that were jumped over
        self.all_sprites_list.update() #sets new pos for sprites that moved

    #draw board methods
    def __draw_empty_board(self):
        '''
        Draws checkerboard without pieces, helper function for draw_board()

        args:
            None
        '''
        self.window.fill(BLACK)
        for row in range(self.ROWS):
            for col in range(row%2, self.ROWS, 2):
                pygame.draw.rect(self.window, RED, (row*self.sq_size, col*self.sq_size, self.sq_size, self.sq_size))

    def __draw_highlighted_board(self):
        '''
        Draws checkerboard without pieces but with possible moves highlighted, helper
        function for draw_board

        Args:
            None
        '''
        moves = self.game.list_moves(self.selected_piece)
        for row in range(self.ROWS):
            for col in range(self.ROWS):
                #highlights possible moves in yellow
                if (row, col) in moves: 
                    pygame.draw.rect(self.window, YELLOW, (col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))
                #highlights current selected piece in green
                if (row, col) == self.selected_piece.pos:
                    pygame.draw.rect(self.window, GREEN, (col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))
    
    def draw_board(self):
        '''
        draws checkerboard with sprites

        Args: 
            None
        '''
        self.__draw_empty_board()
        if self.selected_piece is not None:
            self.__draw_highlighted_board()
        self.all_sprites_list.draw(self.window)
        pygame.display.update()
        return

    def move_selected_piece(self, row, col):
        """
        moves the selected piece to the new position represented by row, col,
        does this by calling self.move_piece. If the selected piece cannot be
        moved to (row, col) position, the piece is unselected

        Args:
            row: represents the row of the position self.selected_piece will
            be moved to
            col: represents the col of the position self.selected_piece will
            be moved to

        """
        pos_moves = self.game.list_moves(self.selected_piece)
        print(pos_moves, row, col)
        if (row, col) in pos_moves:
            print('move is possible')
            self.game.move_piece(self.selected_piece.pos, (row, col))
            self.update_sprites() 
            self.switch_player()
        else:
            self.selected_piece = None

    def switch_player(self):
        '''
        switches the current player
        '''
        self.selected_piece = None
        if self.curr_player == self.players[0]:
            self.curr_player = self.players[1]
        else:
            self.curr_player = self.players[0]
        return

    def play_checkers(self):
        """
        """
        self.init_game()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif self.curr_player.is_bot:
                    pygame.time.wait(10000)
                    org_pos, new_pos = self.curr_player.bot.suggest_move()
                    self.selected_piece = self.game.get_piece(org_pos[0], org_pos[1])
                    self.move_selected_piece(new_pos[0], org_pos[1])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() #this pos is in (x,y)
                    row = pos[1] // self.sq_size #y-pos
                    col = pos[0] //self.sq_size #x-pos
                    if self.selected_piece is None:
                        piece = self.game.get_piece(row, col)
                        if piece is None or piece.team != self.curr_player.color:
                            break
                        self.selected_piece = piece
                        self.draw_board() #draws possible moves
                    else:
                        self.move_selected_piece(row, col)
                else:
                    self.draw_board()

        pygame.display.quit()
        pygame.quit()

'''
way for game to end
if certain peices cannot be moved
'''
#sample board
ex_board = MockGame()
play1 = CheckersPlayer()
play2 = CheckersPlayer(SmartBot(ex_board, 'Red', 'Black'))
player = GUIPlayer(ex_board, play1, play2)
player.play_checkers()