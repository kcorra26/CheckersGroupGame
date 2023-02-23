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
from checkers import Board, Game, Piece, TeamColor 
from mocks import CheckersGameBotMock


class RandomBot: 
    """
    Simple Bot that just picks a move at random
    """

    #_game: Game # this is just what they have
    _color: TeamColor # again
    _opponent_color: TeamColor

    def __init__(self, game, color: TeamColor, 
                 opponent_color: TeamColor):
        """
        Constructor

        Args: 
            game: Game the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """
        self._game = game
        self._color = color
        self._opponent_color = opponent_color
    
    def suggest_move(self): # -> int:
        """
        Suggests a move 

        Returns: None
        """
        # why does the docstring say it returns none if the example code
        # returns random.choice(possible_cols)?
        move_dict = self._game.all_team_moves(self._color)
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

    #_game: BoardType # idk if we will use this
    _color: TeamColor
    _opponent_color: TeamColor

    def __init__(self, game, color: TeamColor, 
                opponent_color: TeamColor):
        """
        Constructor

        Args: 
            board: Board the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """

        self._game = game
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self): # -> int:
        """
        Suggests a move

        Returns: tup(tup(int, int), tup(int, int)) -- suggested move
        """

        """
        https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win 
        - if you have the chance to move more than one way, move toward the
        center. (a centrallized spot has two moves, while an edge has one)
        - protect the king row by advancing two of the four back pieces
        * or half, depending on the size of the board?
            - for Color1, pos (0, 2) and (0, 6)
            - for Color2, pos (width-1, 1) and (width-1, 5) *not 100% sure
        - consider and prioritize opportunities for jumping 
            - maybe have a jump counter? for each move
            - idk how to label the moves
        
        https://www.thesprucecrafts.com/how-to-win-at-checkers-411170 
        - prioritize getting a checker to the end of the board over how many 
        jumps a move will get you
        """
        # assumming that when there is at least one opportunity to jump, 
        # all_team_moves consists only of those jumping moves
        move_dict = self._game.all_team_moves(self._color) 

        # if there is just one move in the dictionary (ie if there is one 
        # key and that key just has one tuple in its list):
        if self._one_move(move_dict) is not None:
            # return the position of the key and the first (and only) value 
            # in the value list
            return self._one_move(move_dict)
        
        max_moves = {} 
        king_moves = {} 
        max_jumps = 0
        centermost = {}
        center = self._game.width // 2
        dist_from_center = center
    
        # loops through the move options, checks if it is a winning move 
        # (returns if so), and adds all the moves that will become a king to
        # a new dict
        for start_pos, list_moves in move_dict.items(): 
            for end_pos in list_moves:
                row, col = end_pos
        
                if self._game.is_winning_move(start_pos, end_pos, self._color):
                    return (start_pos, end_pos)
                
                if self._game.is_winning_move(start_pos, end_pos, 
                                            self._opponent_color):
                    continue
                
                if self._game.will_king(start_pos, end_pos, self._color): 
                    temp_lst = king_moves.get((start_pos), [])
                    temp_lst.append(end_pos)
                    king_moves[start_pos] = temp_lst

        # if there is only one king move, take it
        if self._one_move(king_moves) is not None:
            return self._one_move(king_moves)
        elif king_moves == {}:
            # considers the original list
            consider = move_dict
        else:
            # considers the new list with multiple moves that will become king
            consider = king_moves
        
        # loops through the consider dict to find the moves with the most jumps
        for start_pos, list_moves in consider.items():
            for end_pos in list_moves:
                
                # if the number of jumps is greater than the current max, 
                # reset max_moves and the current max
                if self._game.num_jumps(start_pos, end_pos) > max_jumps:
                    max_jumps = self._game.num_jumps(start_pos, end_pos)
                    max_moves = {start_pos : [end_pos]} # reset dict
                
                # if the number of jumps is equal to the current max, add it
                # to max_moves
                elif self._game.num_jumps(start_pos, end_pos) == max_jumps:
                    lst = max_moves.get((start_pos), [])
                    lst.append(end_pos)
                    max_moves[start_pos] = lst
                # if the number of jumps is fewer than the max, don't consider
        
        # if there is only one max move, take it
        if self._one_move(max_moves) is not None:
            return self._one_move(max_moves)
        elif max_moves == {}: 
            # new dict includes all king moves or all of move_dict
            consider2 = consider
        else:
            # new dict includes only moves with the most jumps
            consider2 = max_moves

        # loops through consider2 dict to find moves towards the center
        for start_pos, list_moves in consider2.items():
            for end_pos in list_moves:
                row, col = end_pos
                
                # if the distance from the center of the board is smaller 
                # than the previous minimum, reset the minimum and the options
                # dict
                if abs(col - (self._game.width // 2)) < dist_from_center:
                    dist_from_center = abs(col - (self._game.width // 2))
                    centermost = {start_pos : [end_pos]}
                # if the distance is equal ot the minimum, add it to the
                # options dict
                elif abs(col - (self._game.width // 2)) == dist_from_center:
                    centermost.get(start_pos, []).append(end_pos)
        
        # if there is only one centermost move, take it
        if self._one_move(centermost) is not None:
            return self._one_move(centermost)
        elif centermost == {}: 
            # randomly pick from the max_jump move options 
            og_pos = random.choice(list(consider2))
            end_pos = random.choice(consider2[og_pos])
            print("random from either king or jumps, centermost empty")
            return (og_pos, end_pos)
        else: 
            # if there is more than one centermost move, randomly pick 
            og_pos = random.choice(list(centermost))
            end_pos = random.choice(centermost[og_pos])
            print("random from centermost")
            return (og_pos, end_pos)
            

    def _one_move(self, dic): 
        """
        Returns the value in the given dic if there is only one value, other
        wise returns none. 

        Args: 
            dic (dict{tup(int, int)} : [tup(int, int)]) - the given dictionary
        
        Returns: 
            (tup((int, int), (int, int) or None) - the key and value if there
            is only one key in the dictionary and one item in the list of that
            key value, otherwise None
        
        I found the syntax for this here: 
        https://stackoverflow.com/questions/46042430/best-way-to-get-a-single-
        key-from-a-dictionary 
        """
        if len(dic) == 1 and len(dic[next(iter(dic))]) == 1:
            return (next(iter(dic)), dic[next(iter(dic))][0])
        return None
                
        
class BotPlayer: # playing against each other
    """
    Simple class to store information about a both player in a simulation.
    """

    name: str #idk what this stuff does
    bot: Union[RandomBot, SmartBot]
    color: TeamColor
    wins: int

    def __init__(self, name: str, game, color: TeamColor,
                 opponent_color: TeamColor):
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
            self.bot = RandomBot(game, color, opponent_color)
        elif self.name == "smart":
            self.bot = SmartBot(game, color, opponent_color)
        self.color = color
        self.wins = 0
    
    def simulate(game, n: int, bots): # -> None:
        """
        Simulate multiple games between two bots

        Args:
            board: The board to play on
            n: The number of matches to play
            bots: Dictionary mapping piece colors to BotPlayer objects
            (the bots that will face off in each match) # IDK what this is
        
        Returns: None
        """
        # CANT PLAY THIS UNTIL MOCK is_done() and 
        for _ in range(n):
            # Reset the board
            board.reset() #TODO

            # starting player 
            current = bots[TeamColor.RED] #idk what color goes first

            while not game.is_done(): # TODO OR there is a winner
                og_pos, new_pos = current.bot.suggest_move() 
                game.move_piece(og_pos, new_pos, current.color) 

                # update the player 
                if current.color == TeamColor.COLOR1: 
                    current = bots[TeamColor.COLOR2] 
                    # now it's the other team's turn
                elif current.color == TeamColor.COLOR2:
                    current = bots[TeamColor.COLOR1]
                
                # if game.is_winner(TeamColor.COLOR1):
                # elif game.is_winner(TeamColor.Color2):
                # else:
                    bots[winner].wins += 1
                
@click.command(name="checkers-bot")
@click.option("-n", "--num-games", type=click.INT, default=10000)
@click.option("--player1", 
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option("--player2", 
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
def cmd(num_games, player1, player2):
    game = Game()
                                    # bot1 team, opponent
    bot1 = BotPlayer(player1, game, TeamColor.COLOR1, TeamColor.COLOR2)
    bot2 = BotPlayer(player1, game, TeamColor.COLOR2, TeamColor.COLOR1)

    bots = {TeamColor.COLOR1: bot1, TeamColor.COLOR2: bot2}

    simulate(game, num_games, bots) # simulating for a number of games

    bot1_wins = bots[TeamColor.COLOR1].wins # number of wins
    bot2_wins = bots[TeamColor.COLOR2].wins 
    ties = num_games - (bot1_wins + bot2_wins) # how many neither of them won

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    # percentage of wins 
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


    if __name__ == "__main__": # idk what this does
        cmd()