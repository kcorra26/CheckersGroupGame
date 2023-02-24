"""
TUI for Checkers
"""
import time 
from typing import Union, Dict

import click
from colorama import Fore, Style

from checkers import Board, Game, Piece
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

BLACK_KING = Fore.BLACK + Style.BRIGHT + "¤"
RED_KING = Fore.RED + Style.BRIGHT + "¤"
BLACK_PIECE = Fore.BLACK + "●"
RED_PIECE = Fore.RED + "●"
VALID_SPACE = Fore.GREEN + Style.BRIGHT + "?"


class TUIPlayer:
    """
    A class for storing information about a player using the TUI.

    The TUIPlayer can be a human using the keyboard or a bot.
    """
    name: str
    bot: Union[None, RandomBot, SmartBot]
    #board will change
    game: MockGame
    team: str
    bot_delay: float

    def __init__(self, player_num: int,  player_type: str, game: MockGame, 
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
        self.board = game.board
        self.team = team
        self.bot_delay = bot_delay

        if player_type == "human":
            self.name = f"Player {player_num}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {player_num}"
            self.bot = RandomBot(game, team, opponent_team)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {player_num}"
            self.bot = SmartBot(game, team, opponent_team)


    def get_move(self) -> int:
        """
        Gets a move from the player
        If the player is a human player, prompt the player for a position to
        move to. If the player is a bot, ask the bot to suggest a move.
        Args: 
            team: the team making the move
        Returns: 
            list[tup(int, int), tup(int, int)]: A list of tuples where the first
            tuple is the position of the piece to be moved (x, y) and the second
            tuple is the ending position (x, y)
        """
        if self.bot is not None:
            time.sleep(self.bot_delay)
            space = self.bot.suggest_move()
            # Print prompt with column already filled in
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL 
                  + str(space+1))
            return space
        else:
            # Ask for a space (and re-ask if
            # a valid space is not provided)
            while True:
                #Get the player's input on what piece they want to move where
                cur_x = input(Style.BRIGHT + f"{self.name} " + f"({self.team}): Select the column of the piece you want to move > " 
                              + Style.RESET_ALL)
                cur_x = self._input_to_valid_move(cur_x, "x")

                cur_y= input(Style.BRIGHT + f"{self.name} " + f"({self.team}): Select the row of the piece you want to move > " 
                             + Style.RESET_ALL)
                cur_y = self._input_to_valid_move(cur_y, "y")

                if self.game.board.board[cur_y][cur_x] is not None:
                    select_piece(self.game, (cur_x, cur_y), self.team)


                dest_x = input(Style.BRIGHT + f"{self.name} " + f"({self.team}): Select the column you want to move to > " 
                               + Style.RESET_ALL)
                dest_x = self._input_to_valid_move(dest_x, "x")

                dest_y = input(Style.BRIGHT + f"{self.name} " + f"({self.team}): Select the row you want to move to > " 
                               + Style.RESET_ALL)
                dest_y = self._input_to_valid_move(cur_y, "y")

                # Convert the indices the player chose to ones that play nice with
                # the list of list representation of the board (may be able to not have this)
                if self.game.is_valid_move((cur_x, cur_y), (dest_x, dest_y)):
                    return (cur_x, cur_y), (dest_x, dest_y)
                else:
                    print("Not a valid move. Please enter a valid move.")
                    return self.get_move()

    def _input_to_valid_move(self, coord: str, dir:str) -> tuple:
        """
        Turns the player input into a coordinate that can access the appropriate
        positions on the board. If player did not enter valid start/end 
        coordinates, re-prompts them until they do.
        Args:
            game: the Game object being used
            coord: the coordinate to be checked in a string format
            dir: if a coordinate is an x (column) or y-coordinate (row)
            team: the team that's moving a place
        Returns: 
            int: a coordinate converted into one that can correctly access board
            positions
        Raises:
            ValueError: if direction is not x or y
        """
        coord = int(coord)
        if coord == "draw": 
            self.game.draw(self.team)
        if coord == "resign":
            self.game.resign(self.team)
        if dir == "x":
            while not (0 <= int(coord) <= self.board.width-1):
                coord = input(Style.BRIGHT + 
                              f"{self.name}: Please enter a valid column >" + 
                              Style.RESET_ALL)
        elif dir == "y":
            while not (0 <= int(coord) <= self.board.width-1):
                coord = input(Style.BRIGHT + 
                              f"{self.name}: Please enter a valid row >" + 
                              Style.RESET_ALL)
        else:
            raise ValueError("Direction was not passed correctly")
        return coord

def print_game(game:MockGame, poss_moves:set=[]):
    """
    Prints the board out to the terminal screen.
    Args:
        board (Board): the board to be printed

    Returns: None
    """
    board = game.board
    width = game.width
    num_pairs = int(width/2)
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
            line = " " + even_line_top
        else: 
            line = " " + odd_line_top
        for col in range(width):
            if (row + col) % 2 == 0:
                wall = SIDE_WALL_LIGHT
            else:
                wall = SIDE_WALL_DARK
            space = board.board[row][col]
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
                square_str = idx + square_str
            line = line + square_str
        if row % 2 == 0:
            line = line + "\n " + even_line_bottom
        else:
            line = line + "\n " + odd_line_bottom
        if row == width-1:
            print(line.rstrip("\n"))
        else:
            print(line)
    bottom_idx = " "
    for i in range(width):
        bottom_idx = bottom_idx + " " + str((i)) + " "
    print(Style.RESET_ALL +bottom_idx)

def select_piece(game:MockGame, pos:tuple, team:str):
    """
    Selects a piece on the board and highlights the positions it can move to.
    Args:
        game: the game object being used
        pos: an (int, int) tuple with the position of the piece
        team: the team to select a piece for
    Returns: None
    """
    col, row = pos
    piece = game.board.board[row][col]
    all_poss_moves = game.list_moves(piece)
    print_game(game, all_poss_moves)



def play_checkers(game:MockGame, players: Dict[str, TUIPlayer]) -> None:
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
    while game.is_winner is None:
            # Print the board
            print()
            print_game(game)
            print()

            cur_space, new_space = current.get_move()
            game.move_piece(cur_space, new_space)
            print("New position:")

            # Update the player
            if current.team == "Black":
                current = players["Red"]
            elif current.team == "Red":
                current = players["Black"]

    print()
    print_game(game)

    winner = game.is_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
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
    elif mode == "mock":
        game = MockGame(num_piece_rows)

    player1 = TUIPlayer(1, player1, game, "Black", "Red", bot_delay)
    player2 = TUIPlayer(2, player2, game, "Red", "Black", bot_delay)

    players = {"Black": player1, "Red": player2}

    play_checkers(game, players)


if __name__ == "__main__":
    cmd()    
    pass

