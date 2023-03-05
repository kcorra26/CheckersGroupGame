"""
Examples:
    1) Make a new board:
        game = Game(n)
            n is the number of rows of pieces on the board, and it defaults to 3 

    2) Check whether a given move is feasible:
        game.can_move((0, 1))
            if they want to just check to see if it can move at all
            where the position is the (row, col) on the board passed as a tuple
        board.is_valid_move((0, 1), (1, 2))
            if they want to check if they can make a specific move 
            from one position to another; the first parameter is the current
            position of the piece, and the second is the intended destination

    3) How to obtain all the valid moves for a piece at a given position:
        game.list_moves((1,1))

    4) How to obtain the list of all possible moves a player can make on the 
        board:
        game.all_team_moves(team)

    5) How to check whether there is a winner and, if so, who the winner is:
        game.is_winner("Red")
        game.is_winner("Black")
            If both functions return False, there is no winner. If the first 
            function returns True, the red team has won. If the second function
            returns True, the black team has won. Both functions will not
            return True.

"""
class Board:
    """Class for representing an empty board of any size"""
    def __init__(self, n=3, a=3):
        """"
        Constructor for the Game Class
        Parameters: 
            width(int): width of board
            n: number of rows in board
            a: number of columns in board
        """
        #width of the board
        self.width = (2 * n) + 2
        #number of rows of the board
        self._num_rows = (2 * n) + 2
        #number of columns of the board
        self._num_columns = (2 * a) + 2
        #the empty board
        self.board = self._create_board()
    def _create_board(self): 
        """
        Initializes an empty board, represented by a list of lists where every 
        cell is filled with None objects
        Args: None
        Returns: a board (list of lists) populated with None obects
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a string representation of the Board.
        Parameters: None
        Returns (str): string representation of the board
        """
        raise NotImplementedError
    
    def add_piece(self,piece):
        """
        Adds a piece to the board.
        Parameters (Piece): Piece being added
        Returns: None
        """
        raise NotImplementedError
        
    
    def get_piece(self,pos):
        """
        Returns the piece specified at the position.
        Parameters(tup): Position of the Piece
        Returns: None if there is not piece at the position or the piece at the
        position
        """
        raise NotImplementedError
    
    def remove_piece(self,pos):
        """
        Removes a piece at a position and replaces it with a None object
        Parameters(pos): Position of the piece being removed
        Returns: None
        """
        raise NotImplementedError

class Game:
    """
    Class for representing a board game; in this case, Checkers
    """
    def __init__(self, n=3):
        """
        Constructor for the Game class
        Args:
            n (int): number of rows of pieces; this defaults to 2 such as in 
            Chess or Checkers
        
        Note: A Checkers Game board is a square, and size is determined by 
        2n + 2
        """
        # Color on board determined by even/odd position of x and y
        # n: number of rows of pieces; board length and width is calculated 
        # as 2n + 2
        # Set containing all Piece and King objects for the red team
        self.red_pieces = set()
        # Set containining all Piece and King objects for the black team
        self.black_pieces = set()
        # Width/length of the board; the board is a square
        self.width = (2 * n) + 2
        
        # the number of rows of pieces per team
        self._num_rows = n
        # Runs the create board function, creating a list of lists (grid) with
        # None objects at each position in the grid
        self.game_board = Board(n,n)

        #Starts the game of checkers and places all pieces
        self._initialize_checkers()
       
        #Contains the winner of the game. It is none while there is no winner,
        #and when there is one it is either "Red" or "Black"
        self.winner = None

        #counts the number of moves since a black piece was removed
        self.since_piece_removed_black = 0

        #counts the number of moves since a red piece was removed
        self.since_piece_removed_red = 0

        #indicates if red wants to draw
        self.red_wants_to_draw = False

        #indicates if black wants to draw
        self.black_wants_to_draw = False
  
    def __str__(self):
        """
        Returns a string representation of the Game.
        Parameters: None
        Returns (str)
        """
        raise NotImplementedError

    def make_king(self):
        """
        Turns every piece that reaches the last row of the opposite side and
        isn't a king into a king
        Parameters:None
        Returns:None
        """
        raise NotImplementedError
                
    
    def will_king(self,old_pos,new_pos,team):
        """
        Determines if a certain move will make the piece become a king
        Parameters:
            old_pos(tup): original position of the piece
            new_pos(tup): new position of the piece
            team(str): team of the piece
        Returns(bool): True if the piece will become a king if it moves to that
        postion and false otherwise
        """
        raise NotImplementedError
    
    def num_jumps(self,old_pos,new_pos,team):
        """
        Computes the number of jumps a piece will makes when moving to a certain 
        position
        
        Parameters:
            old_pos(tup):original position
            new_pos(tup): new position
            team(str): team of piece at the original position
        Returns(int):Number of jumps a piece must make from one spot to another
        """
        raise NotImplementedError


    def is_winning_move(self, old_pos, new_pos, team_making, team_would_win):
        """
        Determines if a move will make corresponding piece's team win
        Parameters:
            old_pos(tup): original position
            new_pos(tup): new position
            team_making: team of the piece at the original position making the 
            move
            team_would_win: team of the piece to check if it would win if the 
            move was made
        Returns(bool): if this move will make the team win
        """
        raise NotImplementedError
    
    def is_done(self):
        """
        Determines if the game is over
        Parameters: None
        Returns(bool): if the game is over
        """
        raise NotImplementedError


    def find_correct_sequence(self, old_pos,new_pos,team):
        """
        Finds the best sequence that a piece should jump through to get to a 
        destination
        Parameters:
            old_pos(tup): the original positon
            new_pos(tup): new position
            team: team of the piece at the original position
        Returns(list): The best sequence a piece should go through to get to a
        destination
        """
        raise NotImplementedError
    

    def middle_positions(self,old_pos,new_pos,team):
        """
        Returns all the spots a piece must go thorugh when jumping from one spot
        to another
        Parameters:
            old_pos(tup): the original positon
            new_pos(tup): new position
            team: team of the piece at the original position
        
        Returns(list): All the spot a piece must go through when jumping from one 
        spot to another
        """
        raise NotImplementedError
        

    def jump_piece(self,old_pos,new_pos,team):
        """
        Makes a piece jump from one spot to another, only under the condition
        that it is a valid jump
         Parameters:
            old_pos(tup): the original positon
            new_pos(tup): new position
            team: team of the piece at the original position
        Returns:None
        """
        raise NotImplementedError

        
    def _remove_piece(self, pos,team):
        """
        Removes a piece at a specific position.
        Parameters: 
            pos: tuple(int, int)
            team: team of the piece
        Returns: None
        """
        raise NotImplementedError
            
    def _initialize_checkers(self):
        """
        Adds all the pieces to the board in starting positions and to the 
        respective team sets
        Parameters: None
        Returns: None
        """
        raise NotImplementedError
    
    def reset_game(self):
        """
        Resets the game, putting the pieces back to where they were initially
        and refilling the red and black piece set
        Parameters:None
        Returns:None
        """
        raise NotImplementedError
        
    
    def all_team_moves(self, team): 
        """
        Maps the location of each piece that has at least one valid move to 
        a list of valid next moves, ultimately returning a dictionary of all 
        possible moves for that team. 
        Args: 
            Team (TeamColor): the team to get moves for
        Returns: 
            dict{tup(int, int): [tup(int, int)]} : dict mapping positions to 
            possible next positions for the piece at each position
            
        """
        raise NotImplementedError
                        
    def is_winner(self, team): 
        """
        Determines if the given team is the winner
        Args:
            team(TeamColor) - the team who is being checked if it is winner
        Returns (bool): whether the specified team is a winner
        """
        raise NotImplementedError


    def can_move(self, pos):
        """
        Determines if the piece at position specified by pos has available 
        moves.
        Args: 
            pos (tuple) - a tuple representing the position of the Piece
        Return (bool) whether the piece at given position has available moves
        """
        raise NotImplementedError
        
    def is_valid_position(self,pos):
        """
        Determines if a given tuple position is a position that is on the board
        Parameters:
            pos(tup): the position
        Returns(bool): If the given tuple positions is on the board
        """
        raise NotImplementedError

    def list_moves(self,pos):
        """
        Lists all the moves of a piece at a position
        Parameters:
            pos(tup): the position 
        Returns(list): returns a list of tuples of all the positions a piece can
        go to
        """
        raise NotImplementedError
        
    def can_jump(self,pos,team,is_king):
        """
        Determines if a piece can jump at a position
        Parameters:
            pos(tup): position of the piece
            team: team of piece
        Returns(bool): If the piece can jump at that position
        """
        raise NotImplementedError
    
    
    def jump_trail_piece(self,pos,team):
        """
        Returns a sequences representing all the possible ways a piece can jump
            Parameters:
            pos(tup): position of the piece
            team: team of piece
        Returns(list): A list of lists of all the sequences a piece can jump through
        """
        raise NotImplementedError
    
    def jump_trail_king(self, pos,original_pos,prev_pos,already_jumped,team):
        """
        Returns a sequences representing all the possible ways a king piece can
        jump
            Parameters:
            pos(tup): position of the piece
            team: team of piece
            already_move(list): all the spots the king piece has already jumped 
            through
        Returns(list): A list of list of all the sequences a king piece 
        can jump throuogh
        """
        raise NotImplementedError
   
    def list_moves_piece(self,pos,team):
        """
        Lists all the moves a piece can make
        Parameters:
            pos(tup): The position of the piece
            team(str): The team of the piece
        Returns(lst): List of all locations a piece can go to
        """
        raise NotImplementedError
        
    def list_moves_king(self,pos,team):
        """
        Lists all the moves a king can make
        Parameters:
            pos(tup): The position of the king
            team(str): The team of the piece
        Returns(lst): List of all locations a king can go to
        """
        raise NotImplementedError
        
    def is_valid_move(self, curr_pos, new_pos):
        """
        Determines if moving from one position to another is a valid move
        Parameters:
            curr_pos(tup): the current positions
            new_pos(tup): the final position
        Returns(bool): If the piece at the current position can jump to the new
        position
        """
        raise NotImplementedError
   
    def resign(self, team): 
        """
        Allows one team to resign and designates the other team as winner.
        
        Args:
            team (TeamColor): the team that is resigning 
        
        Returns:
            None
        """
        raise NotImplementedError
    
    def _is_draw(self):
        """
        Determines if the state of the game is a draw; the game is a draw if 
        neither team can make any moves.
        
        Returns:
            bool: return True if neither team has any possible moves to make 
            (the draw condition), False otherwise
        """
        raise NotImplementedError


    def piece_at_pos(self,pos):
        """
        Returns the piece at a position. Similar to the Board Class's get_piece
        function, but this is for GUI purposes.

        Parameters:
            pos(tup):Position of piece
        Returns (Piece): Piece at the position
        """
        raise NotImplementedError

    def draw(self, team): 
        """
        Allows one team to propose a draw if they believe they have no moves 
        left. The draw condition of no valid moves left for either 
        team does not have to be met. 
        
        Args:
            team (str): the team that wishes to declare a draw
        
        Returns:
            None
        """
        raise NotImplementedError
    
    def response_to_draw(self,team,wants_to_draw):
        """
        Allows a team to respond to a draw if the other team proposes to draw. 

        Parameters:
            team(str): team that is deciding whether to agree to a draw
        Returns: None
        """
        raise NotImplementedError

class Piece(): 
    """
    Class representing playable pieces on the board
    """
    def __init__(self, pos, team_color, is_king = False):
        """
        Constructor for the Piece class. Utilizes the x and y positions of the 
        Piece to calculate the space color and if the color is not dark, will 
        notify that this Piece cannot be placed at this location.
        Args: 
            pos(tuple) - a tuple with two values, representing the position of
            the Piece object (row, col)
            team(TeamColor) - the team the Piece is on
        Returns: None
        """
        #Piece's position represented by an (int, int) tuple with (x,y) position
        # Piece's x position or col
        self.x_pos = pos[1]
        # Piece's y position or row
        self.y_pos = pos[0]
        #The team's position, which depends on the x_pos and y_pos attributes
        self.pos = (self.y_pos,self.x_pos)
        # The team of the piece which is either "Red" or "Black"
        self.team = team_color
        #The attribute that describes if the piece is a king or not. By default 
        #it is false, but if the piece is a king the attribute is equal to True
        self.is_king = is_king
        #The direction that the piece travels in on the board if it is not a king
        self.dir = None
        if self.team == "Red":
            self.dir = -1
        else:
            self.dir = 1
        # Color of the space that the Piece is on; by the rules, must always be 
        # on a dark space, so raises an AssertionError if this doesn't happen as
        # an additional verifier
        if (self.x_pos + self.y_pos) % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
        assert self.space_color == 'dark'
    
    def __str__(self):
        """
        Returns a string representation of the piece.
        Parameters: None
        Returns: str
        """
        raise NotImplementedError
       
    def update_position(self, pos):
        """
        Changes the x and y positions of the piece. Does not check if the new 
        position is valid or not.
        Args:
            pos(tuple) - a tuple with two values, representing the new position 
            of the Piece object
        Returns: None
        """
        raise NotImplementedError
        
    def is_king(self):
        """
        Determines if a Piece object is a king or not
        Returns (bool): whether or not its a king piece
        """
        raise NotImplementedError
        
    def can_move(self, new_pos):
        '''
        Determines if Piece can move to the new position, based on the rules of 
        checkers for a Piece (e.g. Pieces can only move forward)
        Args: 
            new_pos (tuple): a tuple representing the new position
        Returns (bool): whether the Piece can move to that position. Note that 
        this does not take into account whether another Piece is in 
        new_position, which is handled by the board method
        '''
        raise NotImplementedError
        
    
   
from typing import Union
from mocks import StubCheckerboard, MockGame
GameType = Union[Game, MockGame, StubCheckerboard]