"""
TUI for Checkers
"""
import time 
from typing import Union, Dict

import click
from colorama import Fore, Style

from checkers import TeamColor, Board, Game, Piece
from mocks import TeamColor, StubCheckerboard, CheckersGameBotMock
from bot import RandomBot, SmartBot


TOP_ROW_LIGHT = Fore.WHITE + "\u250c" + "\u2500" + "\u2510"
MIDDLE_ROW_LIGHT = Fore.WHITE + "\u2502" + " " + "\u2502"
BOTTOM_ROW_LIGHT = Fore.WHITE + "\u2514" + "\u2500" + "\u2518"

SIDE_WALL_LIGHT = Fore.WHITE + "\u2502"
SIDE_WALL_DARK = Fore.WHITE + "\u2503"

TOP_ROW_DARK = Fore.WHITE + "\u250f" + "\u2501" + "\u2513"
MIDDLE_ROW_DARK = Fore.WHITE + "\u2503" + " " + "\u2503"
BOTTOM_ROW_DARK = Fore.WHITE + "\u2517" + "\u2501" + "\u251b"

class TUIPlayer:
    """
    A class for storing information about a player using the TUI.

    The TUIPlayer can be a human using the keyboard or a bot.
    """
    name: str
    bot: Union[None, RandomBot, SmartBot]
    #board will change
    board: StubCheckerboard
    color: TeamColor
    bot_delay: float

    def __init__(self, n: int,  player_type: str, board: StubCheckerboard, 
                game: Game, color: TeamColor, opponent_color: TeamColor, 
                bot_delay: float):
        """
        Args:
            n: the player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: the Checkers Board the game is being played on
            game: the Game object being used
            color: the team the player is on
            opponent_color: the other player's team
            bot_delay: When playing as a bot, the artificial delay before making
                the next move (in seconds)
        """
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(board, color, opponent_color)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, color, opponent_color)
        self.board = board
        self.game = Game
        self.color = color
        self.bot_delay = bot_delay


    def get_move(self, team:TeamColor) -> int:
        """
        Gets a move from the player
        If the player is a human player, prompt the player for a position to move to.
        If the player is a bot, ask the bot to suggest a move.
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
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL + str(space+1))
            return space
        else:
            # Ask for a space (and re-ask if
            # a valid space is not provided)
            while True:
                #Get the player's input on what piece they want to move where
                cur_x = input(Style.BRIGHT + f"{self.name}: Select the column of the piece you want to move >" + Style.RESET_ALL)
                cur_x = self._input_to_valid_move(cur_x, "x", team)

                cur_y= input(Style.BRIGHT + f"{self.name}: Select the row of the piece you want to move > " + Style.RESET_ALL)
                cur_y = self._input_to_valid_move(cur_y, "y", team)

                dest_x = input(Style.BRIGHT + f"{self.name}: Select the column you want to move to > " + Style.RESET_ALL)
                dest_x = self._input_to_valid_move(dest_x, "x", team)

                dest_y = input(Style.BRIGHT + f"{self.name}: Select the row you want to move to > " + Style.RESET_ALL)
                dest_y = self._input_to_valid_move(cur_y, "y", team)

                # Convert the indices the player chose to ones that play nice with
                # the list of list representation of the board (may be able to not have this)
                if self.game.is_valid_move((cur_x, cur_y), (dest_x, dest_y)):
                    return [(cur_x, cur_y), (dest_x, dest_y)]
                else:
                    see_all = input("This is not a valid move." + Style.BRIGHT 
                                    + "Would you like to see all of your team's possible moves? y/n > "
                                    + Style.RESET_ALL)
                    if see_all == "y":
                        print(self.game.all_team_moves(team))


    """if len(cur_row) == 1 and cur_row len(col) == 1and v[0] in "1234567":
        try:
            #col = int(v) - 1
            if self.board.can_drop(col):
                return col
        except ValueError:
            continue"""


    def _input_to_valid_move(self, game:Game, coord: str, dir:str, team:TeamColor) -> int:
        """
        Turns the player input into a coordinate that can access the appropriate
        positions on the board. If player did not enter valid start/end coordinates,
        re-prompts them until they do.
        Args:
            game: the Game object being used
            coord: the coordinate to be checked in a string format
            dir: if a coordinate is an x-coordinate (column) or y-coordinate (row)
            team: the team that's moving a place
        Returns: 
            int: a coordinate converted into one that can correctly access board
            positions
        Raises:
            ValueError: if direction is not x or y
        """
        if coord == "draw": 
            game.draw(team)
        if coord == "resign":
            game.resign(team)
        if dir == "x":
            while not (len(coord) == 1 and 1 <= int(coord) <= self.board.width):
                coord = input(Style.BRIGHT + f"{self.name}: Please enter a valid column >" + Style.RESET_ALL)
            coord = int(coord) - 1
        elif dir == "y":
            while not (len(coord) == 1 and 1 <= int(coord) <= self.board.width):
                coord = input(Style.BRIGHT + f"{self.name}: Please enter a valid row >" + Style.RESET_ALL)
            coord = self.board.width - int(coord)
        else:
            raise ValueError("Direction was not passed correctly")
        return coord

def print_board(board:StubCheckerboard):
    """
    Prints the board out to the terminal screen.
    Args:
        board (Board): the board to be printed

    Returns: None
    """
    grid = board.board
    width = board.width
    num_pairs = int(width/2)
    even_line_top = Fore.WHITE + ((TOP_ROW_LIGHT + TOP_ROW_DARK) * (num_pairs) + "\n")
    even_line_bottom = Fore.WHITE + (BOTTOM_ROW_LIGHT + BOTTOM_ROW_DARK) * (num_pairs) + "\n"
    odd_line_top = Fore.WHITE + (TOP_ROW_DARK + TOP_ROW_LIGHT) * (num_pairs) + "\n"
    odd_line_bottom = Fore.WHITE + (BOTTOM_ROW_DARK + BOTTOM_ROW_LIGHT) * (num_pairs) + "\n"

    black_king = Fore.BLACK + Style.BRIGHT + "◎"
    red_king = Fore.RED + Style.BRIGHT + "◎"
    black_piece = Fore.BLACK + "●"
    red_piece = Fore.RED + "●"


    for row in range(width):
        idx = str(width-row)
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

            if space is None:
                square_str = (wall + " " + wall)
            elif space.team == "BLACK":
                if space.is_king:
                    square_str = (wall + black_king + wall)
                else:
                    square_str = (wall + black_piece + wall)
            elif space.team == "RED":
                if space.is_king:
                    square_str = (wall + red_king + wall)
                else:
                    square_str = (wall+ red_piece +wall)
            if col == 0:
                square_str = idx + square_str
            line = line + square_str
        if row % 2 == 0:
            line = line + "\n " + (even_line_bottom)
        else:
            line = line + "\n " + odd_line_bottom
        if row == width-1:
            print(line.rstrip("\n"))
        else:
            print(line)
    bottom_idx = " "
    for i in range(width):
        bottom_idx = bottom_idx + " " + str((i+1)) + " "
    print(bottom_idx)

def play_checkers(game:Game, players: Dict[TeamColor, TUIPlayer]) -> None:
    """
    Plays a game of checkers in the terminal.
    
    Args:
        board: the board to play on
        players: a dictionary mapping TeamColors to TUIPlayer objects
    Returns: None
    """
    #whichever player is on Black goes first
    current = players[TeamColor.BLACK]
    #Play the game until there's a winner; should NOT be turned on right now

    while game.is_winner() is None:
            # Print the board
            print()
            print_board(game.board)
            print()

            cur_space, new_space = current.get_move(current)
            game.move_piece(cur_space, new_space)

            # Update the player
            if current.color == TeamColor.BLACK:
                current = players[TeamColor.RED]
            elif current.color == TeamColor.RED:
                current = players[TeamColor.BLACK]

    print()
    print_board(game.board)

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
            type=click.Choice(['real', 'stub', 'mock'], case_sensitive=False),
            default="real")
@click.option('--num-piece-rows',
              type=click.INT, default=3)
@click.option('--player1',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
            default="human")
@click.option('--player2',
            type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
            default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(mode, num_pieces, player1, player2, bot_delay):
    if mode == "real":
        game = Game(num_pieces)
    elif mode == "stub":
        print('stub')
        board = CheckersGameBotMock()
    #    board = GameStub(nrows=6, ncols=7, m=4)
    elif mode == "mock":
        board = CheckersGameBotMock()

    player1 = TUIPlayer(1, player1, board, TeamColor.BLACK, TeamColor.RED, bot_delay)
    player2 = TUIPlayer(2, player2, board, TeamColor.RED, TeamColor.BLACK, bot_delay)

    players = {TeamColor.BLACK: player1, TeamColor.RED: player2}

    play_checkers(game, players)


if __name__ == "__main__":
    cmd()
    pass
