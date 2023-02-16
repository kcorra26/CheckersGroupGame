class Piece(): 
"""
Class representing playable pieces on the board that are not kings
"""
    def __init__(self, pos, team_color):
    """
    Constructor for the Piece class. Utilizes the x and y positions of the Piece
    to calculate the space color and if the color is not dark, will notify that
    this Piece cannot be placed at this location.

    Args: 
        pos(tuple) - a tuple with two values, representing the position of the Piece object
        team(TeamColor) - the team the Piece is on

    Returns: None
    """
        # Piece's position represented by an (int, int) tuple with (x,y) position
        self.pos = pos

        # Piece's x position
        self.x_pos = pos[0]

        # Piece's y position
        self.y_pos = pos[1]

        # TeamColor enum representing the King's team
        self.team = team

        # Color of the space that the Piece is on; by the rules, must always be 
        # on a dark space, so raises an AssertionError if this doesn't happen as
        # an additional verifier
        if self.x_pos + self.y_pos % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
        assert self.space_color is 'dark'


    def update_position(self, pos)
    """
    Changes the x and y positions of the piece. Does not check if the new 
    position is valid or not.
    Args:
        pos(tuple) - a tuple with two values, representing the new position of
        the Piece object
    Returns: None
    """
    Raise NotImplementedError

    def is_empty(self):
    """
    Determines if a Piece object is empty or not. 
        Returns:
            bool: a Piece object always means an occupied space so
            this will always return False
    """
    raise NotImplementedError

    def is_king(self)
    """
    Determines if a Piece object is a king or not
        Returns (bool): a Piece object is always a king so this will return True
    """
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
        if self.x_pos + self.y_pos % 2 == 1:
            self.space_color = 'dark'
        else:
            self.space_color = 'light'
        assert self.space_color is 'dark'

    def update_position(self, pos)
    """
    Changes the x and y positions of the piece. Does not check if the new
    position is valid or not.
    Args:
        pos(tuple) - a tuple with two values, representing the new position of
        the King object
    Returns: None
    """
    Raise NotImplementedError

    def is_empty(self):
    """
    Determines if a King object is empty or not. 
        Returns:
            bool: a King object always means an occupied space so
            this will always return False
    """
    raise NotImplementedError

    def is_king(self)
    """
    Determines if a King object is a king or not
        Returns (bool): a King object is always a king so this will return True
    """
    raise NotImplementedError


