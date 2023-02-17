"""
Examples:
    1) Make a new board:
        board = Board()

    2) Check whether a given move is feasible:
        board.can_move((0, 1))
        # if they want to just check to see if it can move at all
        board.is_valid_move((0, 1), (1, 2))
        #if they want to check if they can move to a certain place

    3) How to obtain all the valid moves for a piece at a given position:
        board.list_moves((0, 1))

    4) How to obtain the list of all possible moves a player can make on the 
        board:
        board.all_team_moves(team)

    5) How to check whether there is a winner and, if so, who the winner is:
        board.is_winner(team)

"""

from enum import Enum
TeamColor = Enum("TeamColor",  ["RED", "BLACK", "EMPTY"]) 

class Board:
    """
    Class for representing a board game; in this case, Checkers
    """
    def __init__(self, n=2):
        """
        Constructor for the Board class
        Args:
            n (int): number of rows of pieces; this defaults to 2 such as in 
            Chess or Checkers
        
        Note: board is a square, and size is determined by 2n + 2
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
        # Empty objects at each position in the grid
        self._create_board()

        # Starts the game of checkers and places all pieces
        self._initialize_checkers()
    
    def _create_board(self): 
        """
        Initializes an empty board, represented by a list of lists where every 
        cell is filled with an Empty object

        Args: None

        Returns: a board (list of lists) populated with Empty objects
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a string representation of the board.

        Parameters: None
        Returns: str
        """
        raise NotImplementedError
    
    def move_piece(self, old_pos, new_pos):
        """
        Ensures the piece is in play, moves the piece at the old position to 
        the new position if the new position is valid, and notifies the player 
        if invalid. If the Piece reaches the end of the board, it changes into
        a King object. 

        Parameters:
            old_pos: tuple(int, int)
            new_pos: tuple(int, int)

        Returns: None
        """
        raise NotImplementedError

    def _remove_piece(self, pos):
        """
        Removes a piece at a specific position. 

        Parameters: 
            pos: tuple(int, int)
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
    
    def list_moves(self, pos):
        """
        Determines the list of moves that a piece at a given position 
        specified by pos can make.
        
        Args:
            pos(tuple) - a tuple representing the position of the Piece 

        Returns:
            lst(tup(int,int)): all possible move locations for the Piece at the 
            given position
        """
        raise NotImplementedError
    
    def is_valid_move(self, curr_pos, new_pos):
        """
        Checks if the piece at a given position can legally move to a 
        different given position.
        
        Args:
            curr_pos (tup(int, int)): the current position
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
    
    def draw(self, team): 
        """
        Allows one team to declare a draw if they believe they have no moves 
        left. If the opposing player agrees then the game ends in a draw with 
        no winner. The draw condition of no valid moves left for either team 
        does not have to be met.
        
        Args:
            team (TeamColor): the team that wishes to declare a draw
        
        Returns:
            None
        """
        raise NotImplementedError


class Empty: 
    """
    Class representing spaces on the board that are empty (positions without
    a playable piece on them)

    """
    
    def __init__ (self, pos):
        """
        constructor for the Empty class

        Args: 
            pos(tuple) - a tuple with two values, representing the position 
            of the Empty object
        
        Returns: None
        """
        #Empty's position represented by an (int, int) tuple with (x,y) position
        self.pos = pos

        # Empty's x position
        self.x_pos = pos[0]

        # Empty's y position
        self.y_pos = pos[1]

        # Empty class has no team
        self.team = TeamColor.EMPTY

        # Color of the space that the Empty is on based on coordinates
        if (self.x_pos + self.y_pos) % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
    
    def __str__(self):
        """
        Returns a string representation of the empty space.

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

    def is_empty(self):
        """
        Determines if an Empty object is empty or not. 
        Args:
            None
            Returns:
                boolean: an Empty object always means an unoccupied space so 
                this will always return True
        """
        raise NotImplementedError

    def is_king(self):
            """
            Determines if an Empty object is a king or not
                Args: 
                    None
                Returns (bool): a Empty object is not a king so this will
                return False
            """
            raise NotImplementedError
    
    def can_move(self, new_pos):
        '''
        Determines if Empty can move to the new position, based on the rules of 
        checkers for a Empty (e.g. Empty can only move forward)

        Args: 
            new_pos (tuple): a tuple representing the new position

        Returns (bool): as Empty cannot move will always return false
        '''
        raise NotImplementedError



class Piece(): 
    """
    Class representing playable pieces on the board that are not kings
    """
    def __init__(self, pos, team_color):
        """
        Constructor for the Piece class. Utilizes the x and y positions of the 
        Piece to calculate the space color and if the color is not dark, will 
        notify that this Piece cannot be placed at this location.

        Args: 
            pos(tuple) - a tuple with two values, representing the position of
            the Piece object
            team(TeamColor) - the team the Piece is on

        Returns: None
        """
        #Piece's position represented by an (int, int) tuple with (x,y) position
        self.pos = pos

        # Piece's x position
        self.x_pos = pos[0]

        # Piece's y position
        self.y_pos = pos[1]

        # TeamColor enum representing the Piece's team
        self.team = team_color

        # Color of the space that the Piece is on; by the rules, must always be 
        # on a dark space, so raises an AssertionError if this doesn't happen as
        # an additional verifier
        if (self.x_pos + self.y_pos) % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
        assert self.space_color is 'dark'
    
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

    def is_empty(self):
        """
        Determines if a Piece object is empty or not. 
        Returns:
            bool: a Piece object always means an occupied space so
            this will always return False
        """
        raise NotImplementedError

    def is_king(self):
        """
        Determines if a Piece object is a king or not
        Returns (bool): a Piece object is always a king so this will return True
        """
        raise NotImplementedError

    def can_move(self, new_pos):
        '''
        Determines if Piece can move to the new position, based on the rules of 
        checkers for a Piece (e.g. Pieces can only move forward)

        Args: 
            new_pos (tuple): a tuple representing the new position

        Returns (bool): whether the Piece can move to that position. Note that 
        this does not take into account whether another Piece is in new_position
        , which is handled by the board method
        '''
        raise NotImplementedError


class King():
    """
    Class representing pieces on the board that are kings 
    """

    def __init__(self, pos, team): 
        """
        Constructor for the King class.
        Args: 
	        pos(tup(int,int)) - a tuple with two values, representing the
            position of the King object
	        team(TeamColor) - the team the King object is on     
        """
        # King's position represented by an (int, int) tuple with (x,y) position
        self.pos = pos

        # King's x position
        self.x_pos = pos[0]

        # King's y position
        self.y_pos = pos[1]

        # TeamColor enum representing the King's team
        self.team = team

        # Color of the space that the King is on; by the rules, must always be 
        # on a dark space, so raises an AssertionError if this doesn't happen as
        # an additional verifier
        if (self.x_pos + self.y_pos) % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
        assert self.space_color is 'dark'

    def __str__(self):
        """
        Returns a string representation of the king piece.

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
            of the King object
        Returns: None
        """
        raise NotImplementedError

    def is_empty(self):
        """
        Determines if a King object is empty or not. 
        Returns:
            bool: a King object always means an occupied space so
            this will always return False
        """
        raise NotImplementedError

    def is_king(self):
        """
        Determines if a King object is a king or not
        Returns (bool): a King object is always a king so this will return True
        """
        raise NotImplementedError
    
    def can_move(self, new_pos):
        '''
        Determines if King can move to the new position, based on the rules of 
        checkers for a King (e.g. King can only in any direction)

        Args: 
            new_pos (tuple): a tuple representing the new position

        Returns (bool): whether the King can move to that position. Note that 
        this does not take into account whether another Piece is in 
        new_position, which is handled by the board method
        '''
        raise NotImplementedError
