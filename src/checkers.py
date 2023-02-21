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
    def __init__(self, n=3):
        self.width = (2 * n) + 2
        self.board = self._create_board()
        self._num_rows = n

    def _create_board(self): 
        """
        Initializes an empty board, represented by a list of lists where every 
        cell is filled with an Empty object

        Args: None

        Returns: a board (list of lists) populated with Empty objects
        """
        empty_board = []
        for i in range(self.width):
            one_row = []
            for j in range(self.width):
                one_row.append(None)
            empty_board.append(one_row)
        return empty_board
    def __str__(self):
        s = ""
        for row in self.board:
            for spot in row:
                s+= "| |"

            s += "\n" 
        return s




class Game:
    """
    Class for representing a board game; in this case, Checkers
    """
    def __init__(self, n=3):
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
        self.game_board = Board().board
        self._initialize_checkers()

        # Starts the game of checkers and places all pieces
        self.winner = None
  

    def __str__(self):
        """
        Returns a string representation of the board.

        Parameters: None
        Returns: str
        """
        s = ""
        for row in self.game_board:
            for spot in row:
                if spot == None:
                    s += "| |"
                else:
                    s += spot.__str__()
            s += "\n"    
        return s
                    
    
    def move_piece(self, old_pos, new_pos, team):
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
        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        new_piece = self.game_board[new_pos[0]][new_pos[1]]
        if (not self.can_move(old_pos) or not current_piece.can_move(new_pos) or
            not self.is_valid_move(old_pos,new_pos)):
            print("Invalid Move")

        
        
        new_piece = current_piece
        new_piece.x_pos = new_pos[0]
        new_piece.y_pos = new_pos[1]
        current_piece = Empty((old_pos[0],old_pos[1]))
        if abs(new_pos[1] - old_pos[1]) == 2:
            middle_x = (old_pos[0] + new_pos[0])/2
            middle_y = (old_pos[1] + new_pos[1])/2
            if team == "Red":
                    self.black_pieces.remove(self.game_board[middle_x][middle_y])
            self.red_pieces.remove(self.game_board[middle_x][middle_y])
            
            

    def _remove_piece(self, pos):
        """
        Removes a piece at a specific position. 

        Parameters: 
            pos: tuple(int, int)
        Returns: None
        """
        for piece in self.black_pieces:
            if piece.pos_x == pos[0] and piece.pos[y] == pos[1]:
                self.black_pieces.remove(piece)
        for piece in self.red_pieces:
            if piece.pos_x == pos[0] and piece.pos[y] == pos[1]:
                self.red_pieces.remove(piece)
        
    
    def _initialize_checkers(self):
        """
        Adds all the pieces to the board in starting positions and to the 
        respective team sets

        Parameters: None

        Returns: None
        """
        for i in range(3):
            for j in range(self.width):
                if (i + j) % 2 == 1:
                    self.game_board[i][j] = Piece((i,j),"Black")
                    self.black_pieces.add(Piece((i,j),"Black"))
        for i in range(self.width - 3, self.width):
            for j in range(self.width):
                if (i + j) % 2 == 1:
                    self.game_board[i][j] = Piece((i,j),"Red")
                    self.red_pieces.add(Piece((i,j),"Red"))


    
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
        team_moves ={}
        if team == "Red":
            for piece in self.red_pieces:
                if self.can_move((piece.pos_x,piece.pos_y)):
                    if piece.is_king is False:
                        team_moves[piece] = self.list_moves_piece(piece)
                    if piece.is_king is True:
                        team_moves[piece] = self.list_moves_king(piece)
        return team_moves

                        

    def is_winner(self, team): 
        """
        Determines if the given team is the winner

        Args:
            team(TeamColor) - the team who is being checked if it is winner

        Returns (bool): whether the specified team is a winner
        """
        if team == "Red":
            if len(self.black_pieces) == 0 and len(self.all_team_moves(team)) == 0:
                return True
            return False
        if team == "Black":
            if len(self.red_pieces) == 0 and len(self.all_team_moves(team)) == 0:
                return True
            return False


    def can_move(self, pos):
        """
        Determines if the piece at position specified by pos has available 
        moves.

        Args: 
            pos (tuple) - a tuple representing the position of the Piece

        Return (bool) whether the piece at given position has available moves
        """
        current_piece = self.game_board[pos[0]][pos[1]]
        if current_piece.is_king is False:
            if len(self.list_moves_piece(pos,False)) > 0:
                return True
            return False
        if current_piece.is_king is True:
            if len(self.list_moves_king(pos,False)) > 0:
                return True
            return False

        

    def is_valid_position(self,pos):
        if 0 <= pos[0] <= self.width - 1 and 0 <= pos[1] <= self.width - 1:
            return True
        return False 
        
    
    def list_moves_piece(self, pos, has_jumped):
        """
        Determines the list of moves that a piece at a given position 
        specified by pos can make.
        
        Args:
            pos(tuple) - a tuple representing the position of the Piece 

        Returns:
            lst(tup(int,int)): all possible move locations for the Piece at the 
            given position
        """
        moves = []
        current_piece = self.game_board[pos[0]][pos[1]]
        assert current_piece.is_king is False
        if has_jumped is False:
            if self.is_valid_position(((pos[0] + current_piece.dir), pos[1] - 1 )):
                if (self.game_board[(pos[0] + current_piece.dir)][pos[1] - 1] == None):
                    moves.append(((pos[0] + current_piece.dir), pos[1] - 1 ))
                elif (self.game_board[(pos[0] + current_piece.dir)][pos[1] - 1].team 
                      != current_piece.team and self.is_valid_position(((pos[0] + 2*current_piece.dir), pos[1] - 2 ))):
                    if self.game_board[(pos[0] + 2*current_piece.dir)][pos[1] - 2] is None:
                        moves += self.list_moves_piece(((pos[0] + 2*current_piece.dir), pos[1] - 2 ), True)
            if self.is_valid_position(((pos[0] + current_piece.dir), pos[1] + 1 )):
                if (self.game_board[(pos[0] + current_piece.dir)][pos[1] + 1] is None):
                    moves.append(((pos[0] + current_piece.dir), pos[1] + 1 ))
                elif (self.game_board[(pos[0] + current_piece.dir)][pos[1] + 1].team 
                    != current_piece.team and self.is_valid_position(((pos[0] + 2*current_piece.dir), pos[1] + 2 ))):
                    if self.game_board[(pos[0] + 2*current_piece.dir)][pos[1] + 2] is None:
                        moves += self.list_moves_piece(((pos[0] + 2*current_piece.dir), pos[1] + 2 ), True)
        if has_jumped is True:
            if (self.is_valid_position(((pos[0] + current_piece.dir), pos[1] - 1 ))):
                if (self.self.game_board[(pos[0] + current_piece.dir)][pos[1] - 1]
                    is not None):
                    if (self.game_board[(pos[0] + current_piece.dir)][pos[1] - 1].team 
                        != current_piece.team and self.is_valid_position(((pos[0] + 2*current_piece.dir), pos[1] - 2 ))):
                        if self.game_board[(pos[0] + 2*current_piece.dir)][pos[1] - 2] is None:
                            moves += self.list_moves_piece(((pos[0] + 2*current_piece.dir), pos[1] - 2 ), True)
            if (self.is_valid_position(((pos[0] + current_piece.dir), pos[1] + 1 ))):
                if (self.self.game_board[(pos[0] + current_piece.dir)][pos[1] + 1]
                    is not None):
                    if (self.game_board[(pos[0] + current_piece.dir)][pos[1] + 1].team 
                        != current_piece.team and self.is_valid_position(((pos[0] + 2*current_piece.dir), pos[1] + 2))):
                        if self.game_board[(pos[0] + 2*current_piece.dir)][pos[1] + 2] is None:
                            moves += self.list_moves_piece(((pos[0] + 2*current_piece.dir), pos[1] + 2 ), True)
            moves += current_piece
        return moves
        
    def list_moves_king(self, pos, has_jumped):
        moves = []
        current_piece = self.game_board[pos[0]][pos[1]]
        assert current_piece.is_king is True
        directions = [-1,1]
        if has_jumped is False:
            for i in directions:
                if self.is_valid_position(((pos[0] + i), pos[1] - 1 )):
                    if (self.game_board[(pos[0] + i)][pos[1] - 1] is None):
                        moves.append(((pos[0] + i), pos[1] - 1 ))
                    elif (self.game_board[(pos[0] + i)][pos[1] - 1].team 
                        != current_piece.team and self.is_valid_position(((pos[0] + 2*i), pos[1] - 2 ))):
                        if self.game_board[(pos[0] + 2*i)][pos[1] - 2] is None:
                            moves += self.list_moves_king(((pos[0] + 2*i), pos[1] - 2 ), True)
                if self.is_valid_position(((pos[0] + i), pos[1] + 1 )):
                    if (self.game_board[(pos[0] + i)][pos[1] + 1] is None):
                        moves.append(((pos[0] + i), pos[1] + 1 ))
                    elif (self.game_board[(pos[0] + i)][pos[1] + 1].team 
                        != current_piece.team and self.is_valid_position(((pos[0] + 2*i), pos[1] + 2 ))):
                        if self.game_board[(pos[0] + 2*i)][pos[1] + 2] is None:
                            moves += self.list_moves_king(((pos[0] + 2*i), pos[1] + 2 ), True)
        if has_jumped is True:
            for i in directions:
                if (self.is_valid_position(((pos[0] + i), pos[1] - 1 ))):
                    if (self.self.game_board[(pos[0] + i)][pos[1] - 1]
                        is not None):
                        if (self.game_board[(pos[0] + i)][pos[1] - 1].team 
                            != current_piece.team and self.is_valid_position(((pos[0] + 2*i), pos[1] - 2 ))):
                            if self.game_board[(pos[0] + 2*i)][pos[1] - 2] is None:
                                moves += self.list_moves_king(((pos[0] + 2*i), pos[1] - 2 ), True)
            if (self.is_valid_position(((pos[0] + i), pos[1] + 1 ))):
                if (self.self.game_board[(pos[0] + i)][pos[1] + 1]
                    is not None):
                    if (self.game_board[(pos[0] + i)][pos[1] + 1].team 
                        != current_piece.team and self.is_valid_position(((pos[0] + 2*i), pos[1] + 2))):
                        if self.game_board[(pos[0] + 2*i)][pos[1] + 2] is None:
                            moves += self.list_moves_king(((pos[0] + 2*i), pos[1] + 2 ), True)
            moves += current_piece



                

            
            

    
    def is_valid_move(self, curr_pos, new_pos):

        current_piece = self.game_board[curr_pos[0]][curr_pos[1]]
        if current_piece.is_king is False:
            if new_pos not in self.list_moves_piece(curr_pos):
                return True
            return False
        if current_piece.is_king is True:
            if new_pos not in self.list_moves_king(curr_pos):
                return True
            return False


        
        
        
    
    def resign(self, team): 
        """
        Allows one team to resign and designates the other team as winner.
        
        Args:
            team (TeamColor): the team that is resigning 
        
        Returns:
            None
        """
        if team == "Red":
            self.winner = "Black"
        self.winner = "Red"
    
    def _is_draw(self):
        """
        Determines if the state of the game is a draw; the game is a draw if 
        neither team can make any moves.
        
        Returns:
            bool: return True if neither team has any possible moves to make 
            (the draw condition), False otherwise
        """
        if self.all_team_moves("Red") == {} and self.all_team_moves("Black") == {}:
            return True
        return False
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



class Piece(): 
    """
    Class representing playable pieces on the board that are not kings
    """
    def __init__(self, pos, team_color, is_king = False):
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
        self.is_king = is_king
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
        assert self.space_color is 'dark'
    
    def __str__(self):
        """
        Returns a string representation of the piece.

        Parameters: None
        Returns: str
        """
        if self.is_king is False:
            if self.team == "Red":
                return "|r|"
            return "|b|"
        if self.is_king is True:
            if self.team == "Red":
                return "|kr|"
            return "|kb|"
       

    def update_position(self, pos):
        """
        Changes the x and y positions of the piece. Does not check if the new 
        position is valid or not.
        Args:
            pos(tuple) - a tuple with two values, representing the new position 
            of the Piece object
        Returns: None
        """
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        

    def is_king(self):
        """
        Determines if a Piece object is a king or not
        Returns (bool): a Piece object is always a king so this will return True
        """
        return self.is_king

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
        if self.team == "Red":
            if (abs(new_pos[1] - self.y_pos) == 1 and new_pos[0] - self.x_pos == -1):
                return True
        if self.team == "Black":
            if (abs(new_pos[1] - self.y_pos) == 1 and new_pos[0] - self.x_pos == 1):
                return True
        return False
        #Take into account eating chip!!!
        #Recursive Function?
            
        





board = Game(3)
print(board.list_moves_piece((5,0),False))
print(board.game_board[5][2])
