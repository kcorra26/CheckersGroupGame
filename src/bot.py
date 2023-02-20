"""
- basic research on Checkers-playing strategies
- document the exact strategies we are implementing, citing sources
- implementation should match cited strategy
- demonstrate that bot is able to beat a random bot more than 50% of the time

Bots for Checkers

(and command for running simulations with bots)
"""
import random
from typing import Union # idk what this does yet

import click
from checkers import Board, Empty, Piece, King, TeamColor # BoardType?


class RandomBot: 
    """
    Simple Bot that just picks a move at random
    """

    _board: BoardType # this is just what they have
    _color: TeamColor # again
    _opponent_color: TeamColor

    def __init__(self, board: BoardType, color: TeamColor, 
                 _opponent_color: TeamColor)
        """
        Constructor

        Args: 
            board: Board the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """
        self._board = board
        self._color = color
        self._opponent_color = opponent_color
    
    def suggest_move(self) # -> int:
        """
        Suggests a move 

        Returns: None
        """
        # why does the docstring say it returns none if the example code
        # returns random.choice(possible_cols)?
        move_dict = board.all_team_moves(self._color)
        og_pos = random.choice(list(move_dict))
        end_pos = random.choice(move_dict[og_pos])

        return (og_pos, end_pos) # returns tuple of tuples
        # ((x, y), (x2, y2))

class SmartBot: 
    """
    Smart bot. Will do the following:
    - If there is a winning move, take it #idk if this applies
    # check for skips?
    - Otherwise, check if there is a move that will block the opponent
      from winning. If so, take it. 
    - Otherwise, pick a move at random

    # research other strategies
    """

    _board: BoardType # idk if we will use this
    _color: TeamColor
    _opponent_color: TeamColor

    def __init__(self, board: BoardType, color: TeamColor, 
                opponent_color: TeamColor):
        """
        Constructor

        Args: 
            board: Board the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """

        self._board = board
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self) # -> int:
        """
        Suggests a move

        Returns: None???
        """
        # returns tuple w/ origin position, end position
        # if there are just a bunch with one move, pick one at random

        """
        - if you have the chance to jump more than one way, jump toward the
        center. 
            - if you have the choice between moving or jumping to the side
            or the center, go toward the center (bc a centrallized piece has
            two moves)
        - protect the king row by advancing two of the four back pieces
        * or half, depending on the size of the board?
            - for Color1, pos (0, 2) and (0, 6)
            - for Color2, pos (width-1, 1) and (width-1, 5) *not 100% sure
        - try not to separate pieces??
            - give preference to the decisions that keep pieces close 
            to eachother
        
        """


class BotPlayer:
    """
    Simple class to store information about a both player in a simulation.
    """

    name: str #idk what this stuff does
    bot: Union[RandomBot, SmartBot]
    color: TeamColor
    wins: int

    def __init__(self, name: str, board: BoardType, color: TeamColor,
                 opponent_color: TeamColor)
        """
        Constructor

        Args:
            name: Name of the bot
            board: Board to play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self.name = name

        if self.name == "random":
            self.bot = RandomBot(board, color, opponent_color)
        elif self.name == "smart":
            self.bot = SmartBot(board, color, opponent_color)
        self.color = color
        self.wins = 0
    
    def simulate(board: BoardType, n: int, bots) # -> None:
        """
        Simulate multiple games between two bots

        Args:
            board: The board to play on
            n: The number of matches to play
            bots: Dictionary mapping piece colors to BotPlayer objects
            (the bots that will face off in each match) # IDK what this is
        
        Returns: None
        """
        for _ in range(n):
            # Reset the board
            # board.reset()

            # starting player
            #current = bots[TeamColor.COLOR1] idk what color goes first

            while not board.is_done(): # board class needs an is_done function
                og_pos, new_pos = current.bot.suggest_move() # two tuples
                board.move_piece(og_pos, new_pos, current.color) # need to pass
                # team as a parameter

                # update the player 
                if current.color == TeamColor.COLOR1: 
                    current = bots[TeamColor.COLOR2] 
                    # now it's the other team's turn
                elif current.color == TeamColor.COLOR2:
                    current = bots[TeamColor.COLOR1]
                
                winner = board.get_winner() # if we make a get_winner function
                # otherwise, do 
                # if winner = board.is_winner(TeamColor.COLOR1):
                # elif winner = board.is_winner(TeamColor.Color2):
                if winner is not None:
                    bots[winner].wins += 1
                
@click.command(name="checkers-bot")
@click.option("-n", "--num-games", type=click.INT, default-10000)
@click.option("--player1", 
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option("--player2", 
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
def cmd(num_games, player1, player2):
    board = Board()
                                    # bot1 team, opponent
    bot1 = BotPlyaer(player1, board, TeamColor.COLOR1, TeamColor.COLOR2)
    bot2 = BotPlyaer(player1, board, TeamColor.COLOR2, TeamColor.COLOR1)

    bots = {TeamColor.COLOR1: bot1, TeamColor.COLOR2: bot2}

    simulate(board, num_games, bots) # simulating for a number of games

    bot1_wins = bots[TeamColor.COLOR1].wins # number of wins
    bot2_wins = bots[TeamColor.COLOR2].wins 
    ties = num_games - (bot1_wins + bot2_wins) # how many neither of them won

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    # percentage of wins 
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


    if __name__ == "__main__": # idk what this does
        cmd()