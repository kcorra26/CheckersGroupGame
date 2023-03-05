"""
TUI for Checkers
"""
import time 
from typing import Union, Dict, Optional

import click
from colorama import Fore, Style, Back

from checkers import Board, Game, Piece, GameType
from mocks import MockGame, Piece, MockCheckerboard, StubCheckerboard
from bot import RandomBot, SmartBot


TOP_ROW_LIGHT = Fore.WHITE + "\u250c" + "\u2500" + "\u2510"
MIDDLE_ROW_LIGHT = Fore.WHITE + "\u2502" + " " + "\u2502"
BOTTOM_ROW_LIGHT = Fore.WHITE + "\u2514" + "\u2500" + "\u2518"

SIDE_WALL_LIGHT = Fore.WHITE + "\u2502"
SIDE_WALL_DARK = Fore.WHITE + "\u2503"

TOP_ROW_DARK = Fore.WHITE + "\u250f" + "\u2501" + "\u2513"
MIDDLE_ROW_DARK = Fore.WHITE + "\u2503" + " " + "\u2503"
BOTTOM_ROW_DARK = Fore.WHITE + "\u2517" + "\u2501" + "\u251b"

BLACK_KING = Fore.BLACK + Style.BRIGHT + "\u00A4"
RED_KING = Fore.RED + Style.BRIGHT + "\u00A4"
BLACK_PIECE = Fore.BLACK + "\u25CF"
RED_PIECE = Fore.RED + "\u25CF"
VALID_SPACE = Fore.GREEN + Back.GREEN + "?" + Style.RESET_ALL


class TUIPlayer:
    """
    A class for storing information about a player using the TUI.

    The TUIPlayer can be a human using the keyboard or a bot.
    """
    name: str
    bot: Union[None, RandomBot, SmartBot]
    game: GameType
    team: str
    bot_delay: float

    def __init__(self, player_num: int,  player_type: str, game: GameType, 
                team: str, opponent_team: str, bot_delay: float):
        """
        Args:
            n: the player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            game: the Game object being used
            team: the team the player is on ("Black" or "Red")
            opponent_team: the other player's team
            bot_delay: When playing as a bot, the artificial delay before making
                the next move (in seconds)
        """
        self.game = game
        self.board = game.game_board
        self.team = team
        self.bot_delay = bot_delay
        self.width = game.width

        if player_type == "human":
            self.name = f"Player {player_num}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {player_num}"
            self.bot = RandomBot(game, team, opponent_team)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {player_num}"
            self.bot = SmartBot(game, team, opponent_team)


    def get_move(self) -> list:
        """
        Gets a move from the player
        If the player is a human player, prompt the player for a position to
        move to. If the player is a bot, ask the bot to suggest a move.
        Returns: 
            list[tup(int, int), tup(int, int)]: A list of tuples where the first
            tuple is the position of the piece to be moved (x, y) and the second
            tuple is the ending position (x, y)
        """
        if self.bot is not None:
            time.sleep(self.bot_delay)
            space = self.bot.suggest_move(self.game)
            # Print prompt with column already filled in
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL 
                  + str(space[1]), str(space[0]))
            return space
        else:
            # Ask for a space (and re-ask if
            # a valid space is not provided)
            while True:
                #Get the player's input on what piece they want to move where
                cur_y= input(Style.BRIGHT + f"{self.name} " + f"({self.team}"
                             +"): Select the row of the piece you want to move >" 
                             + Style.RESET_ALL)
                cur_y = self._input_is_valid(cur_y, "y")

                cur_x = input(Style.BRIGHT + f"{self.name} " + f"({self.team}"
                              +"): Select the column of the piece you want to " 
                              + "move > " + Style.RESET_ALL)
                cur_x = self._input_is_valid(cur_x, "x")

                #show the possible places to move to
                if self.board.board[cur_y][cur_x] is not None:
                    select_piece(self.game, (cur_x, cur_y))

                dest_y = input(Style.BRIGHT + f"{self.name} " + f"({self.team}"
                               + "): Select the row you want to move to > " 
                               + Style.RESET_ALL)
                dest_y = self._input_is_valid(dest_y, "y")

                dest_x = input(Style.BRIGHT + f"{self.name} " + f"({self.team}"
                               +"): Select the column you want to move to > " 
                               + Style.RESET_ALL)
                dest_x = self._input_is_valid(dest_x, "x")

                if self.game.is_valid_move((cur_y, cur_x), (dest_y, dest_x)):
                    return (cur_y, cur_x), (dest_y, dest_x)
                else:
                    print("Not a valid move. Please enter a valid move.")
                    return self.get_move()

    def _input_is_valid(self, coord: str, dir:str) -> bool:
        """
        Turns the player input into a coordinate that can access the appropriate
        positions on the board. If player did not enter valid start/end 
        coordinates, re-prompts them until they do.
        Args:
            coord: the coordinate to be checked in a string format; can also
                be draw or resign; however the game logic for these may not be
                fully implemented
            dir: if a coordinate is an x (column) or y-coordinate (row)
        Returns: 
            bool: True if the coordinate exists on the board
        Raises:
            ValueError: if direction is not x or y
        """
        if coord.lower() == "draw": 
            self.game.draw(self.team)
            return -1
        if coord.lower() == "resign":
            self.game.resign(self.team)
            return -2
        # While this calls draw and resign, there is not a functional way to 
        # draw or resign with the TUI. The only way to do so is with the 
        # checkers.py file/game logic.
        while not (coord.isdigit()) or not (0 <= int(coord) <= self.width-1):
            if dir == "x":  
                coord = input(Style.BRIGHT + f"{self.name}: " +
                        " Please enter a valid column > " + Style.RESET_ALL)
            elif dir == "y":
                coord = input(Style.BRIGHT + f"{self.name}: " +
                        "Please enter a valid row > " + Style.RESET_ALL)
        return int(coord)

def print_game(game:GameType, poss_moves:Optional[list]=[]):
    """
    Prints the board out to the terminal screen.
    Args:
        game: the game to print out
        poss_moves [Optional]

    Returns: None
    """
    board = game.game_board.board
    width = game.width
    num_pairs = int(width/2)
    spacing = " " * len(str(width-1))
    even_line_top = Fore.WHITE + (
        (TOP_ROW_LIGHT + TOP_ROW_DARK) * (num_pairs) + "\n")
    even_line_bottom = Fore.WHITE + (
        (BOTTOM_ROW_LIGHT + BOTTOM_ROW_DARK) * (num_pairs) + "\n")
    odd_line_top = Fore.WHITE + (
        (TOP_ROW_DARK + TOP_ROW_LIGHT) * (num_pairs) + "\n")
    odd_line_bottom = Fore.WHITE + (
        (BOTTOM_ROW_DARK + BOTTOM_ROW_LIGHT) * (num_pairs) + "\n")

    for row in range(width):
        idx = Style.RESET_ALL + str(row)
        if row % 2 == 0:
            line = "  " + even_line_top
        else: 
            line = "  " + odd_line_top
        for col in range(width):
            if (row + col) % 2 == 0:
                wall = SIDE_WALL_LIGHT
            else:
                wall = SIDE_WALL_DARK
            space = board[row][col]
            square_str = ""

            if (row, col) in poss_moves:
                square_str = (wall + VALID_SPACE + wall)
            elif space is None:
                square_str = (wall + " " + wall)
            elif space.team == "Black":
                if space.is_king:
                    square_str = (wall + BLACK_KING + wall)
                else:
                    square_str = (wall + BLACK_PIECE + wall)
            elif space.team == "Red":
                if space.is_king:
                    square_str = (wall + RED_KING + wall)
                else:
                    square_str = (wall+ RED_PIECE +wall)
            if col == 0:
                if row <= 9:
                    square_str = idx + " " + square_str
                else:
                    square_str = idx + square_str

            line = line + square_str
        if row % 2 == 0:
            line = line + "\n " + " " + even_line_bottom
        else:
            line = line + "\n " + " " + odd_line_bottom
        if row == width-1:
            print(line.rstrip("\n"))
        else:
            print(line)
    bottom_idx = "  "
    if width <= 10:
        for i in range(width):
            bottom_idx = bottom_idx + " " + str(i) + " "
    elif width > 10:
        bottom_idx = "" + bottom_idx
        for i in range(width):
            bottom_idx = bottom_idx + " " + str(i) +  " "
    print(Style.RESET_ALL + bottom_idx)

def select_piece(game:GameType, pos:tuple) -> None:
    """
    Selects a piece on the board and highlights the positions it can move to.
    Args:
        game: the game object being used
        pos: an (int, int) tuple with the position of the piece
    Returns: None
    """
    col, row = pos
    all_poss_moves = game.list_moves((row, col))
    print_game(game, all_poss_moves)
    print(all_poss_moves)


def play_checkers(game:GameType, players: Dict[str, TUIPlayer]) -> None:
    """
    Plays a game of checkers in the terminal.
    
    Args:
        board: the board to play on
        players: a dictionary mapping team color strings to TUIPlayer objects
    Returns: None
    """
    #whichever player is on Black goes first
    current = players["Black"]
    #Play the game until there's a winner
    while not game.is_done():
            # Print the board
            print()
            print_game(game)
            print()


            cur_space, new_space = current.get_move()
            game.move_piece(cur_space, new_space, current.team)

            # Update the player team
            if current.team == "Black":
                current = players["Red"]
            elif current.team == "Red":
                current = players["Black"]


    print()
    print_game(game)

    if game.is_winner("Red"):
        game.winner = "Red"
        print(f"The winner is {players['Red'].name}!")
    elif game.is_winner("Black"):
        game.winner = "Black"
        print(f"The winner is {players['Black'].name}!")
    else:
        print("It's a tie!")


#
# Command-line interface
#

@click.command(name="checkers-tui")
@click.option('--mode',
            type=click.Choice(['real', 'stub', 'mock'], 
                              case_sensitive=False), default="real")
@click.option('--num-piece-rows', type=click.INT, default=3)
@click.option('--player1',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], 
                              case_sensitive=False), default="human")
@click.option('--player2',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], 
                              case_sensitive=False), default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(mode, num_piece_rows, player1, player2, bot_delay):
    if mode == "real":
        game = Game(num_piece_rows)
    elif mode == "stub":
        game = StubCheckerboard(num_piece_rows)
        # Functionality for StubCheckerboard is not implemented
    elif mode == "mock":
        # Mock functionality will print out a sample board, show sample moves,
        # and then crash once trying to move a piece due to functions not being 
        # implemented.
        game = MockGame(num_piece_rows)

    player1 = TUIPlayer(1, player1, game, "Black", "Red", bot_delay)
    player2 = TUIPlayer(2, player2, game, "Red", "Black", bot_delay)

    players = {"Black": player1, "Red": player2}

    play_checkers(game, players)
    


if __name__ == "__main__":
    cmd()    
    pass

"""
changes since milestone 2
Sam - TUI
    Since Milestone 2, functionality for showing all possible moves of a piece
once selected has been added using the Colorama library. Note that this
selection essentially employs the "touch-move" rule: once a piece has been
selected, there is not a way to select another one except intentionally entering
an invalid destination space.
    The feedback about making pieces and kings distinct has also been included;
pieces are represented with ● and kings with ¤ of the appropriate team color.
    The board now has full support for board sizes from 6x6 to 20x20. (Indices
on the bottom row on sizes greater than 10x10 do not display entirely
correctly due to numbers having two digits-they will run off the side)
    From feedback in Milestone 2, also sanitized user input so that the program
will not crash if a non-integer is enter for a piece position; instead,
users will be continually prompted until they enter a valid position.
    The TUI has been fully integrated with both the bots and game logic and can
play full games.

"""