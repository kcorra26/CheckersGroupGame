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
from checkers import Board, Game, Piece
from mocks import CheckersGameBotMock


class RandomBot: 
    """
    Simple Bot that just picks a move at random
    """

    def __init__(self, game, color, 
                 opponent_color):
        """
        Constructor

        Args: 
            game: Game the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """
        #self._game = game
        self._color = color
        self._opponent_color = opponent_color
    
    def suggest_move(self, game):
        """
        Suggests a move 

        Returns: tup(tup(int, int), tup(int, int)) -- suggested move
        """
        #move_dict = self._game.all_team_moves(self._color)
        move_dict = game.all_team_moves(self._color)
        og_pos = random.choice(list(move_dict))
        end_pos = random.choice(move_dict[og_pos])
        print("random bot picked at random")

        return (og_pos, end_pos) 


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

    def __init__(self, game, color, 
                opponent_color):
        """
        Constructor

        Args: 
            board: Board the bot will play on
            color: Bot's team color
            opponent_color: Opponent's color
        """

        #self._game = game
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self, game): # do i need to pass the game in every time?
        """
        Suggests a move

        Returns: tup(tup(int, int), tup(int, int)) -- suggested move
        """

        """
        https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win 
        - if you have the chance to move more than one way, move toward the
        center. (a centrallized spot has two moves, while an edge has one)
        - consider and prioritize opportunities for jumping 
        
        https://www.thesprucecrafts.com/how-to-win-at-checkers-411170 
        - prioritize getting a checker to the end of the board over how many 
        jumps a move will get you
        """
        # assumming that when there is at least one opportunity to jump, 
        # all_team_moves consists only of those jumping moves
        #move_dict = self._game.all_team_moves(self._color) # but self.color works?
        move_dict = game.all_team_moves(self._color)
        print(move_dict)

        # if there is just one move in the dictionary (ie if there is one 
        # key and that key just has one tuple in its list):
        if self._one_move(move_dict) is not None:
            # return the position of the key and the first (and only) value 
            # in the value list
            print("only option")
            return self._one_move(move_dict)
        
        max_moves = {} 
        king_moves = {} 
        max_jumps = 0
        centermost = {}
        center = game.width // 2
        dist_from_center = center
    
        # loops through the move options, checks if it is a winning move 
        # (returns if so), and adds all the moves that will become a king to
        # a new dict (king strategy by thesprucecrafts)
        for start_pos, list_moves in move_dict.items(): 
            for end_pos in list_moves:
                row, col = end_pos
                
                if game.is_winning_move(start_pos, end_pos, self._color, self._color): 
                    print("picked from winning moves")
                    return (start_pos, end_pos)

                if game.is_winning_move(start_pos, end_pos, 
                                        self._color, self._opponent_color):
                    print("winning move exists, ignoring")
                    continue
                
                #if self._game.will_king(start_pos, end_pos, self._color): 
                if game.will_king(start_pos, end_pos, self._color):
                    temp_lst = king_moves.get((start_pos), [])
                    temp_lst.append(end_pos)
                    king_moves[start_pos] = temp_lst

        # if there is only one king move, take it
        if self._one_move(king_moves) is not None:
            print("picked from king moves")
            return self._one_move(king_moves)
        elif king_moves == {}:
            # considers the original list
            consider = move_dict
        else:
            # considers the new list with multiple moves that will become king
            consider = king_moves
        
        # loops through the consider dict to find the moves with the most jumps
        # (jump strategy by HobbyLark)
        for start_pos, list_moves in consider.items():
            for end_pos in list_moves:
                
                # if the number of jumps is greater than the current max, 
                # reset max_moves and the current max
                

                #if self._game.num_jumps(start_pos, end_pos, self._color) > max_jumps:
                if game.num_jumps(start_pos, end_pos, self._color) > max_jumps:
                    #max_jumps = self._game.num_jumps(start_pos, end_pos, self._color)
                    max_jumps = game.num_jumps(start_pos, end_pos, self._color)
                    max_moves = {start_pos : [end_pos]} # reset dict
                
                # if the number of jumps is equal to the current max, add it
                # to max_moves
                
                #elif self._game.num_jumps(start_pos, end_pos, self._color) == max_jumps:
                elif game.num_jumps(start_pos, end_pos, self._color) == max_jumps:
                    lst = max_moves.get((start_pos), [])
                    lst.append(end_pos)
                    max_moves[start_pos] = lst
                # if the number of jumps is fewer than the max, don't consider
        
        # if there is only one max move, take it
        if self._one_move(max_moves) is not None:
            print("picked from sole max_move")
            return self._one_move(max_moves)
        elif max_moves == {}: 
            # new dict includes all king moves or all of move_dict
            print("no jumps")
            consider2 = consider
        else:
            # new dict includes only moves with the most jumps
            consider2 = max_moves 

        # loops through consider2 dict to find moves towards the center 
        # (centermost strategy suggested by both HobbyLark and thesprucecrafts)
        for start_pos, list_moves in consider2.items():
            for end_pos in list_moves:
                row, col = end_pos
                
                # if the distance from the center of the board is smaller 
                # than the previous minimum, reset the minimum and the options
                # dict
                if abs(col - (center)) < dist_from_center:
                    dist_from_center = abs(col - (center))
                    centermost = {start_pos : [end_pos]}
                # if the distance is equal ot the minimum, add it to the
                # options dict
                elif abs(col - (center)) == dist_from_center:
                    centermost.get(start_pos, []).append(end_pos)
        
        # if there is only one centermost move, take it
        if self._one_move(centermost) is not None:
            print(consider2)
            print("only one centermost option")
            return self._one_move(centermost)
        elif centermost == {}: 
            # randomly pick from the max_jump move options 
            og_pos = random.choice(list(consider2))
            end_pos = random.choice(consider2[og_pos])
            print("random from max jump")
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
    Simple class to store information about a bot player in a simulation.
    """

    #name: str #idk what this stuff does
    #bot: Union[RandomBot, SmartBot]
    #color: str
    #wins: int

    def __init__(self, name, game, color,
                 opponent_color):
        """
        Constructor

        Args:
            name: Name of the bot
            game: Game to play
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
    

def simulate(game, n: int, bots):
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
        # Reset the game
        game.reset_game() 

        # starting player 
        current = bots["Black"] 

        while not game.is_done(): 
            og_pos, new_pos = current.bot.suggest_move(game) 
            print(og_pos, new_pos)
            # the former piece is still in game.black_pieces
            game.move_piece(og_pos, new_pos, current.color) 
            old_color = current.color

            # update the player 
            if current.color == "Black": 
                current = bots["Red"] 
            elif current.color == "Red":
                current = bots["Black"]
            
            if game.is_winner("Red"):
                bots["Red"].wins += 1
                print(f'Red wins! num red wins: {bots["Red"].wins}')
            elif game.is_winner("Black"):
                bots["Black"].wins += 1
                print(f'Black wins! num black wins: {bots["Black"].wins}')
            print(f'{old_color} : {og_pos}, {new_pos}') # but (2, 3) is an empty space
            print("after decision:")
            print(game)
            print("----------------------------------------")

# for TUI integration, not fully complete (but have fully integrated with GUI)
@click.command(name="checkers-bot")
@click.option("-n", "--num-games", type=click.INT, default=10000)

def cmd(num_games, player1, player2):
    game = Game()

    bot1 = BotPlayer(player1, game, "Black", "Red")
    bot2 = BotPlayer(player2, game, "Red", "Black")

    bots = {"Black": bot1, "Red": bot2}

    simulate(game, num_games, bots) 

    bot1_wins = bots["Black"].wins 
    bot2_wins = bots["Red"].wins 
    ties = num_games - (bot1_wins + bot2_wins) 

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")

    
    if __name__ == "__main__": 
        cmd()