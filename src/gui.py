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
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

from checkers import Board, Game, Piece, GameType
from mocks import StubCheckerboard, MockGame
from sprites import PieceSprite
from bot import RandomBot, SmartBot
import click
from typing import Union

WIDTH = HEIGHT = 800

#colors
WHITE = (255, 255,255)
BLACK = (0,0,0)
RED = (170,0,20)
YELLOW = (255, 204, 0)
GREEN = (75, 139, 59)
GOLD = (255, 215, 0)

class CheckersPlayer():
    '''
    simple class to store player information
    '''
    bot: Union[None, SmartBot, RandomBot]
    
    def __init__(self, bot = None):
        '''
        initialization function for the Checkers Player

        args: 
            bot: a bot object or None if player is not a
            bot
        '''
        if bot == None:
            self.is_bot = False
        else:
            self.is_bot = True
        self.bot = bot
        if self.is_bot:
            self.color = self.bot._color
        else:
            self.color = None
    
    def can_play_checkers (self, other):
        '''
        determines if two players can play checkers, if they can their team
        color is set

        args:
            other: another CheckersPlayer object

        returns(bool): whether these two players can play checkers
        '''
        assert isinstance(other, CheckersPlayer)
        if not self.is_bot and not other.is_bot:
            self.color = 'Black'
            other.color = 'Red'
            return True
        elif self.is_bot and other.is_bot and self.color != other.color:
            return True
        elif other.is_bot and not self.is_bot:
            if other.color == 'Red':
                self.color = 'Black'
            else:
                self.color = 'Red'
            return True
        elif self.is_bot and not other.is_bot:
            if self.color == 'Red':
                other.color = 'Black'
            else:
                other.color = 'Red'
            return True
        else:
            return False


class GUIPlayer():

    def __init__(self, game:GameType, player_1: CheckersPlayer, \
                 player_2:CheckersPlayer):
        """
        init function for GUI Player

        args: 
            game(GameType): the game being played
            player_1(CheckersPlayer): A CheckersPlayer object
            player_2(CheckersPlayer): A CheckersPlayer object
        """
        self.game = game
        self.ROWS = game.width
        self.sq_size = WIDTH // game.width

        #ensures game can continue
        if player_1.can_play_checkers(player_2):
            self.players = [player_1, player_2]
            self.curr_player = self.players[0]
        else: 
            raise TypeError('These two bots have the same team and cannot play against each other')

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
        self._init_sprites()
        pygame.display.update()
    
    def _init_sprites(self):
        '''
        this function initializes all Pieces and add thems to
        all_piece_list

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
        updates the sprites by removing sprites whoose pieces are no longer
        in play and updating the locations of the remaining sprites

        Args: None
        '''
        pieces = self.game.red_pieces.union(self.game.black_pieces)
        for sprite in self.all_sprites_list:
            if sprite.piece not in pieces:
                sprite.kill() #will kill sprites that were jumped over
        self.all_sprites_list.update() #sets new pos for sprites that moved

    #draw board methods
    def __draw_empty_board(self):
        '''
        Draws checkerboard without pieces or highlights, helper function for
        draw_board()

        args:
            None
        '''
        self.window.fill(BLACK)
        for row in range(self.ROWS):
            for col in range(row%2, self.ROWS, 2):
                pygame.draw.rect(self.window, RED, (row*self.sq_size, col*self.sq_size,\
                                                    self.sq_size, self.sq_size))

    def __draw_highlighted_board(self):
        '''
        Draws checkerboard without pieces but with possible moves highlighted
        and selected piece highlighted in green, helper function for draw_board()

        Args:
            None
        '''
        moves = self.game.list_moves(self.selected_piece.pos)
        for row in range(self.ROWS):
            for col in range(self.ROWS):
                #highlights possible moves in yellow
                if (row, col) in moves: 
                    pygame.draw.rect(self.window, YELLOW, (col*self.sq_size, \
                                                           row*self.sq_size, \
                                                            self.sq_size, \
                                                                self.sq_size))
                #highlights current selected piece in green
                if (row, col) == self.selected_piece.pos:
                    pygame.draw.rect(self.window, GREEN, (col*self.sq_size,\
                                                           row*self.sq_size, \
                                                            self.sq_size, \
                                                                self.sq_size))
    
    def draw_board(self):
        '''
        draws checkerboard with sprites, and highlighted mvoes if a piece
        is currently selected

        Args: 
            None
        '''
        self.__draw_empty_board()
        if self.selected_piece is not None:
            self.__draw_highlighted_board()
        self.all_sprites_list.draw(self.window) #redraws sprites
        pygame.display.update()
        return

    def move_selected_piece(self, row, col):
        """
        moves the selected piece to the new position represented by row, col,
        does this by calling self.move_piece. Then switched current player and
        sets selected piece to none. If the selected piece cannot be
        moved to (row, col) position, the piece is unselected. At the end, also
        redraws the board

        Args:
            row: represents the row of the position self.selected_piece will
            be moved to
            col: represents the col of the position self.selected_piece will
            be moved to

        """
        pos_moves = self.game.list_moves(self.selected_piece.pos)
        if (row, col) in pos_moves:
            self.game.move_piece(self.selected_piece.pos, (row, col), self.curr_player.color)
            self.update_sprites() #changes locations and kills sprites
            self.switch_player()
        else:
            self.selected_piece = None
        self.draw_board()

    def switch_player(self):
        '''
        switches the current player and sets the selected piece to
        None

        args: None
        '''
        self.selected_piece = None
        if self.curr_player == self.players[0]:
            self.curr_player = self.players[1]
        else:
            self.curr_player = self.players[0]
        return
    
    def bot_play_turn(self):
        '''
        plays current turn for bot, ensures that the current player is
        a bot, then makes move suggested by bot

        args: None
        '''
        assert self.curr_player.is_bot
        pygame.time.wait(1000) #bot delay (edit later)
        org_pos, new_pos = self.curr_player.bot.suggest_move(self.game)
        self.selected_piece = self.game.piece_at_pos((org_pos[0], org_pos[1]))
        self.move_selected_piece(new_pos[0], new_pos[1])

    def play_checkers(self):
        """
        This function plays checkers on a pygame window.

        Args: none
        """
        self.init_game()

        run = True
        while run:
            for event in pygame.event.get():
                self.draw_board()
                if event.type == pygame.QUIT:
                    run = False
                elif self.game.is_done():
                    font = pygame.font.Font('freesansbold.ttf', 45)
                    if self.game.is_winner('Red'):
                        text = font.render('RED WINS!!', True, RED, WHITE)
                    elif self.game.is_winner('Black'):
                        text = font.render('BLACK WINS!!', True, BLACK, WHITE)
                    else:
                        text = font.render('DRAW', True, GOLD, WHITE)
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2, HEIGHT// 2)
                    self.window.blit(text, textRect)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    run = False
                elif self.curr_player.is_bot:
                    self.bot_play_turn()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() #this pos is in (x,y)
                    row = pos[1] // self.sq_size #y-pos
                    col = pos[0] //self.sq_size #x-pos
                    if self.selected_piece is None:
                        piece = self.game.game_board.board[row][col]
                        if piece is not None and piece.team == self.curr_player.color:
                            self.selected_piece = piece
                        self.draw_board() #draws possible moves
                    else:
                        self.move_selected_piece(row, col) #moves if valid move
            else:
                continue
                
        pygame.display.quit()
        pygame.quit()

#
# Command-line interface
#

@click.command(name="checkers-gui")
@click.option('--mode',
            type=click.Choice(['real', 'stub', 'mock'], 
                              case_sensitive=False), default="real")
@click.option('--num-piece-rows', type=click.INT, default=3)
@click.option('--black-type',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], 
                              case_sensitive=False), default="human")
@click.option('--red-type',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], 
                              case_sensitive=False), default="smart-bot")

def cmd(mode, num_piece_rows, black_type, red_type):
    if mode == "real":
        game = Game(num_piece_rows)
    elif mode == "stub":
        game = StubCheckerboard(num_piece_rows)
    elif mode == "mock":
        game = MockGame(num_piece_rows)

    if black_type == 'human':
        player1 = CheckersPlayer()
    elif black_type == 'random-bot':
        player1 = CheckersPlayer(RandomBot(game, 'Black', 'Red'))
    else:
        player1 = CheckersPlayer(SmartBot(game, 'Black', 'Red'))

    if red_type == 'human':
        player2 = CheckersPlayer()
    elif red_type == 'random-bot':
        player2= CheckersPlayer(RandomBot(game, 'Red', 'Black'))
    else:
        player2 = CheckersPlayer(SmartBot(game, 'Red', 'Black'))

    gui = GUIPlayer(game, player1, player2)
    gui.play_checkers()

if __name__ == "__main__":
    cmd()    
    pass
