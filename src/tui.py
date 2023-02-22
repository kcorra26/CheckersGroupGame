"""
TUI for Checkers
"""
import time 
from typing import Union, Dict

import click
from colorama import Fore, Style

#from checkers import TeamColor, Board, Game, Piece
from mocks import TeamColor, StubCheckerboard
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
                color: TeamColor, opponent_color: TeamColor, bot_delay: float):
        """
        Args:
            n: the player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: the Checkers Board the game is being played on
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
        self.color = color
        self.bot_delay = bot_delay


    def get_move(self) -> int:
        """ Gets a move from the player
        If the player is a human player, prompt the player for a position to move to.
        If the player is a bot, ask the bot to suggest a move.
        Returns: None
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
                """
                how to enter desired move:
                first enter row
                    check if there are any valid spaces to go to in row(?)
                then enter column
                    check if that position is valid
                    if so, move the piece there and remove it from the previous spot
                    capture/jump pieces if necessary
                    conditions for a valid space
                
                """
                v = input(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL)
                if len(v) == 1 and v[0] in "1234567":
                    try:
                        col = int(v) - 1
                        if self.board.can_drop(col):
                            return col
                    except ValueError:
                        continue




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

def play_checkers(board:StubCheckerboard, players: Dict[TeamColor, TUIPlayer]) -> None:
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
    """while board.is_winner() is None:
        print()
        print(board)
        print()
    """
    while board.is_winner() is None:
            # Print the board
            print()
            print_board(board)
            print()

            space = current.get_move()

            # Drop the piece
            board.drop(column, current.color)

            # Update the player
            if current.color == TeamColor.BLACK:
                current = players[TeamColor.RED]
            elif current.color == TeamColor.RED:
                current = players[TeamColor.BLACK]

    print()
    print_board(board)

    winner = board.get_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")


#
# Command-line interface
#

    @click.command(name="connect4-tui")
    @click.option('--mode',
                type=click.Choice(['real', 'stub', 'mock'], case_sensitive=False),
                default="real")
    @click.option('--player1',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
                default="human")
    @click.option('--player2',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
                default="human")
    @click.option('--bot-delay', type=click.FLOAT, default=0.5)
    def cmd(mode, player1, player2, bot_delay):
        if mode == "real":
            board = ConnectMBoard(nrows=6, ncols=7, m=4)
        elif mode == "stub":
            board = ConnectMBoardStub(nrows=6, ncols=7, m=4)
        elif mode == "mock":
            board = ConnectMBoardMock(nrows=6, ncols=7, m=4)

        player1 = TUIPlayer(1, player1, board, PieceColor.YELLOW, PieceColor.RED, bot_delay)
        player2 = TUIPlayer(2, player2, board, PieceColor.RED, PieceColor.YELLOW, bot_delay)

        players = {PieceColor.YELLOW: player1, PieceColor.RED: player2}

        play_connect_4(board, players)


if __name__ == "__main__":
    cmd()
    pass
