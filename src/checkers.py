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
    """Class for representing an empty board of any size"""
    def __init__(self, n=3, a=3):
        """"
        Constructor for the Game Class
        Parameters: 
            width(int): width of board
            n: number of rows in board
            a: number of columns in board
        """

        self.width = (2 * n) + 2
        self._num_rows = (2 * n) + 2
        self._num_columns = (2 * a) + 2
        self.board = self._create_board()


    def _create_board(self): 
        """
        Initializes an empty board, represented by a list of lists where every 
        cell is filled with an Empty object

        Args: None

        Returns: a board (list of lists) populated with Empty objects
        """
        empty_board = []
        for i in range(self._num_rows):
            one_row = []
            for j in range(self._num_columns):
                one_row.append(None)
            empty_board.append(one_row)
        return empty_board
    def __str__(self):
        """
        Returns a string representation of the Board.

        Parameters: None
        Returns: str
        """
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
        Constructor for the Game class
        Args:
            n (int): number of rows of pieces; this defaults to 2 such as in 
            Chess or Checkers
        
        Note: A Checkers Game board is a square, and size is determined by 2n + 2
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
        Returns a string representation of the Game.

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

    def make_king(self):
        """
        Turns every piece that reaches the last row of the opposite side and
        isn't a king into a king

        Parameters:None
        Returns:None
        """
        for spot in self.game_board[0]:
            if spot is not None and spot.is_king is False and spot.team == "Red":
                self._remove_piece((spot.y_pos,spot.x_pos),"Red")
                spot.is_king = True
                self.red_pieces.add(spot)
                
        for spot in self.game_board[self.width - 1]:
            if spot is not None and spot.is_king is False and spot.team == "Black":
                self._remove_piece((spot.y_pos,spot.x_pos),"Black")
                spot.is_king = True
                self.red_pieces.add(spot)
                
    
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
        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        if self.is_valid_move(old_pos,new_pos):
            if team == "Red" and current_piece.is_king is False and new_pos[0] == 0:
                return True
            if team == "Black" and current_piece.is_king is False and new_pos[0] == self.width - 1:
                return True
            return False
    
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
        if self.find_correct_sequence(old_pos,new_pos,team): 
            return len(self.find_correct_sequence(old_pos,new_pos,team)) #- 1
        return 0

    def is_winning_move(self, old_pos, new_pos, team_making, team_would_win):
        """
        Determines if a move will make corresponding piece's team win

        Parameters:
            old_pos(tup): original position
            new_pos(tup): new position
            team_making: team of the piece at the original position making the move
            team_would_win: team of the piece to check if it would win if the move was made
        Returns(bool): if this move will make the team win
        """
        original_set = None
        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        is_winner = None
        original_set_red = self.red_pieces
        original_set_black = self.black_pieces
        original_board = self.game_board
        if self.is_valid_move(old_pos,new_pos):
            if current_piece.can_move(new_pos): 
                self.move_piece(old_pos,new_pos, team_making)
                is_winner = self.is_winner(team_would_win)
                """
                self.game_board[old_pos[0]][old_pos[1]] = self.game_board[new_pos[0]][new_pos[1]]
                self.game_board[new_pos[0]][new_pos[1]] = None """
                 
            """" i commented this out because move_piece already checks for can_jump
            if self.can_jump(old_pos, team_making):
                self.jump_piece(old_pos, new_pos, team_making)
                is_winner = self.is_winner(team_would_win)
                self.game_board[old_pos[0]][old_pos[1]] = self.game_board[new_pos[0]][new_pos[1]]
                self.game_board[new_pos[0]][new_pos[1]] = None """
        self.game_board = original_board # this updates the whole board (and it works), which is good because may jump and mess up other spots
        # i'm not sure if we need to update the pieces too 
        self.red_pieces = original_set_red
        self.black_pieces = original_set_black
        return is_winner
        # is winner works as intended now 
        
    def is_done(self):
        """
        Determines if the game is over

        Parameters: None

        Returns(bool): if the game is over
        """
        if self.is_winner("Red") or self.is_winner("Black"):
            return True
        if self._is_draw():
            return True
        return False


                
    def move_piece(self, old_pos, new_pos,team):
        """
        Ensures the piece is in play, moves the piece at the old position to 
        the new position if the new position is valid, and notifies the player 
        if invalid. If the Piece reaches the end of the board, it changes into
        a King object. The piece can only be moved one space at a time

        Parameters:
            old_pos: tuple(int, int)
            new_pos: tuple(int, int)

        Returns: None
        """
        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        if new_pos in self.list_moves(old_pos):
            if abs(new_pos[0] - old_pos[0]) == 1 and abs(new_pos[1] - old_pos[1]) == 1: # this only accounts for non-jumping pieces
                self.game_board[new_pos[0]][new_pos[1]] = current_piece
                #print("updating position of move piece")
                self.game_board[new_pos[0]][new_pos[1]].update_position(new_pos)
                self.game_board[old_pos[0]][old_pos[1]] = None
                if team == "Red":
                    for piece in self.red_pieces:
                        if piece.x_pos == old_pos[1] and piece.y_pos == old_pos[0]:
                            self.red_pieces.remove(piece)
                            self.red_pieces.add(self.game_board[new_pos[0]][new_pos[1]])
                if team == "Black":
                    for piece in self.black_pieces:
                        if piece.x_pos == old_pos[1] and piece.y_pos == old_pos[0]:
                            self.black_pieces.remove(piece)
                            self.black_pieces.add(self.game_board[new_pos[0]][new_pos[1]])
                self.make_king()
            else: # this didn't exist before. need to update the position of jump pieces as well. 
                self.jump_piece(old_pos, new_pos, team)
                # this works


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

        choose_sequence = None # something about this is wrong
        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        if current_piece.is_king is False:
            for sequence in self.jump_trail_piece(old_pos,team):
                if choose_sequence is None and sequence[len(sequence) - 1] == new_pos:
                    choose_sequence = sequence
                elif choose_sequence != None and sequence[len(sequence) - 1] == new_pos:
                    if len(choose_sequence) < len(sequence):
                        choose_sequence = sequence
            return choose_sequence
        if current_piece.is_king is True:
            for sequence in self.jump_trail_king(old_pos, old_pos, None, [], team):
                if choose_sequence == None and sequence[len(sequence) - 1] == new_pos:
                    choose_sequence = sequence
                elif choose_sequence != None and sequence[len(sequence) - 1] == new_pos:
                    if len(choose_sequence) < len(sequence):
                        choose_sequence = sequence
            return choose_sequence
    
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

        middle_positions = []
        full_sequence = [old_pos] + self.find_correct_sequence(old_pos,new_pos,team)
        
        for i in range(len(full_sequence) - 1):
                middle_pos = ((full_sequence[i][0] + full_sequence[i+1][0])/2,
                (full_sequence[i][1] + full_sequence[i+1][1])/2)
                middle_positions.append(middle_pos)
        return middle_positions

        
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


        current_piece = self.game_board[old_pos[0]][old_pos[1]]
        if self.is_valid_move(old_pos,new_pos):
            for pos in self.middle_positions(old_pos,new_pos,team):
                
                if team == "Red":
                    self._remove_piece((int(pos[0]),int(pos[1])),"Black")
                if team == "Black":
                    self._remove_piece((int(pos[0]),int(pos[1])),"Red")
                self.game_board[int(pos[0])][int(pos[1])] = None 

            if old_pos != new_pos:
                self._remove_piece(old_pos,team)
                self.game_board[int(old_pos[0])][int(old_pos[1])] = None
                self.game_board[int(new_pos[0])][int(new_pos[1])] = current_piece
            #print("updating position of jump piece") # this never happens
                self.game_board[int(new_pos[0])][int(new_pos[1])].update_position((new_pos[0],new_pos[1]))
                if team == "Red":
                    self.red_pieces.add(self.game_board[int(new_pos[0])][int(new_pos[1])])
            
                if team == "Black":
                    self.black_pieces.add(self.game_board[int(new_pos[0])][int(new_pos[1])])

                self.make_king()
        




            
        
    def print_tuple_pairs(self):
        tuple_pair = []
        for piece in self.black_pieces:
            tuple_pair.append((piece.y_pos,piece.x_pos))
        return tuple_pair
        
        

        

    def _remove_piece(self, pos,team):
        """
        Removes a piece at a specific position. 

        Parameters: 
            pos: tuple(int, int)
            team: team of the piece
        Returns: None
        """
        new_set = set()
        if team == "Red":
            for piece in self.red_pieces:
                if pos != (piece.y_pos,piece.x_pos):
                    new_set.add(piece)
            self.red_pieces = new_set
        if team == "Black":
            for piece in self.black_pieces:
                if pos != (piece.y_pos,piece.x_pos):
                    new_set.add(piece)
            self.black_pieces = new_set

    
        
    
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
    
    def reset_game(self):
        """
        Resets the game, putting the pieces back to where they were initially
        and refilling the red and black piece set

        Parameters:None
        Returns:None
        """
        self.red_pieces = set()
        self.black_pieces = set()
        for i in range(self.width):
            for j in range(self.width):
                if self.game_board[i][j] is not None:
                    self.game_board[i][j] = None
        self._initialize_checkers()
        


    
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
                if self.can_move((piece.y_pos,piece.x_pos)):
                    team_moves[(piece.y_pos,piece.x_pos)] = self.list_moves((piece.y_pos,piece.x_pos))
        if team == "Black":
            for piece in self.black_pieces:
                if self.can_move((piece.y_pos,piece.x_pos)):
                    team_moves[(piece.y_pos,piece.x_pos)] = self.list_moves((piece.y_pos,piece.x_pos))
        
        return team_moves

                        

    def is_winner(self, team): 
        """
        Determines if the given team is the winner

        Args:
            team(TeamColor) - the team who is being checked if it is winner

        Returns (bool): whether the specified team is a winner
        """
        if team == "Red":
            if len(self.black_pieces) == 0 and len(self.all_team_moves("Black")) == 0:
                return True
            return False
        if team == "Black":
            if len(self.red_pieces) == 0 and len(self.all_team_moves("Red")) == 0:
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
        if len(self.list_moves(pos))> 0:
            return True
        return False

        

    def is_valid_position(self,pos):
        """
        Determines if a given tuple position is a position that is on the board
        Parameters:
            pos(tup): the position
        Returns(bool): If the given tuple positions is on the board
        """
        if 0 <= pos[0] <= self.width - 1 and 0 <= pos[1] <= self.width - 1:
            return True
        return False 

    def list_moves(self,pos):
        """
        Lists all the moves of a piece at a position
        Parameters:
            pos(tup): the position 
        Returns(list): returns a list of tuples of all the positions a piece can
        go to
        """
        """current_piece = self.game_board[pos[0]][pos[1]]
        if current_piece.is_king is False:
            return self.list_moves_piece(pos,False,[],current_piece.team)
        else:
            return self.list_moves_king(pos,False,[],current_piece.team)"""
        current_piece = self.game_board[pos[0]][pos[1]]
        if current_piece is None:
            print(pos)
        if current_piece.is_king is False:
            return self.list_moves_piece(pos,current_piece.team)
        else:
            return self.list_moves_king(pos,current_piece.team)
        

    def can_jump(self,pos,team,is_king):
        """
        Determines if a piece can jump at a position
        Parameters:
            pos(tup): position of the piece
            team: team of piece
        Returns(bool): If the piece can jump at that position
        """
        current_spot = self.game_board[pos[0]][pos[1]]
        directions = [-1,1]
        direction = None
        if team == "Red":
            direction = -1
        if team == "Black":
            direction = 1
        if (current_spot is None and is_king is False) or (current_spot is not None and not current_spot.is_king):
            if self.is_valid_position((pos[0] + direction, pos[1] + 1)):
                if (self.game_board[pos[0] + direction][pos[1] + 1] is not None
                    and self.game_board[pos[0] + direction][pos[1] + 1].team != team):
                    if (self.is_valid_position((pos[0] + 2* direction, pos[1] + 2)) and
                        self.game_board[pos[0] + 2*direction][pos[1] + 2] is None):
                        return True
            if self.is_valid_position((pos[0] + direction, pos[1] - 1)):
                if (self.game_board[pos[0] + direction][pos[1] - 1] is not None
                    and self.game_board[pos[0] + direction][pos[1] - 1].team != team):
                    if (self.is_valid_position((pos[0] + 2*direction, pos[1] - 2)) and
                        self.game_board[pos[0] + 2*direction][pos[1] - 2] is None):
                        return True
        elif (current_spot is None and is_king is True) or (current_spot is not None and current_spot.is_king is True):
            for i in directions:
                if self.is_valid_position((pos[0] + i, pos[1] + 1)):
                    if (self.game_board[pos[0] + i][pos[1] + 1] is not None
                        and self.game_board[pos[0] + i][pos[1] + 1].team != team):
                        if (self.is_valid_position((pos[0] + 2*i, pos[1] + 2)) and
                            self.game_board[pos[0] + 2*i][pos[1] + 2] is None):
                            return True
                if self.is_valid_position((pos[0] + i, pos[1] - 1)):
                    if (self.game_board[pos[0] + i][pos[1] - 1] is not None
                        and self.game_board[pos[0] + i][pos[1] - 1].team != team):
                        if (self.is_valid_position((pos[0] + 2*i, pos[1] - 2)) and
                            self.game_board[pos[0] + 2*i][pos[1] - 2] is None):
                            return True
        return False
    def jump_trail_piece(self,pos,team):
        """
        Returns a sequences representing all the possible ways a piece can jump
            Parameters:
            pos(tup): position of the piece
            team: team of piece
        Returns(list): A list of lists of all the sequences a piece can jump throuogh
        """


        trails = []
        current_piece = self.game_board[pos[0]][pos[1]]
        direction = None
        if team == "Red":
            direction = -1
        else:
            direction = 1
        if not self.can_jump(pos,team,False):
            return []
        if self.can_jump(pos,team,False):
            if (self.is_valid_position(((pos[0] + direction),pos[1] + 1)) and
                (self.game_board[pos[0] + direction][pos[1] + 1] is not None)):
                if (self.game_board[(pos[0] + direction)][pos[1] + 1].team != team and 
                    self.is_valid_position(((pos[0] + 2*direction),pos[1] + 2))):
                    if self.game_board[pos[0] + 2*direction][pos[1] + 2] is None:
                        if self.can_jump((pos[0] + 2*direction,pos[1] + 2),team,False) is False:
                            trails.append([(pos[0] + 2*direction,pos[1] + 2)])
                        for trail in self.jump_trail_piece((pos[0] + 2*direction,pos[1] + 2),team):
                            trails.append([(pos[0] + 2*direction,pos[1] + 2)] + trail)
            if (self.is_valid_position(((pos[0] + direction),pos[1] - 1)) and
                (self.game_board[(pos[0] + direction)][pos[1] - 1] is not None)):
                if ((self.game_board[(pos[0] + direction)][pos[1] - 1].team != team) and 
                    self.is_valid_position(((pos[0] + 2*direction),pos[1] + 2))):
                    if self.game_board[pos[0] + 2*direction][pos[1] - 2] is None:
                        if self.can_jump((pos[0] + 2*direction,pos[1] - 2),team,False) is False:
                            trails.append([(pos[0] + 2*direction,pos[1] - 2)])
                        for trail in self.jump_trail_piece((pos[0] + 2*direction,pos[1] - 2),team):
                            trails.append([(pos[0] + 2*direction,pos[1] - 2)] + trail)
            return trails
    
    def jump_trail_king(self, pos,original_pos,prev_pos,already_jumped,team):
        """
        Returns a sequences representing all the possible ways a king piece can jump
            Parameters:
            pos(tup): position of the piece
            team: team of piece
            already_move(list): all the spots the king piece has already jumped through
        Returns(list): A list of list of all the sequences a king piece 
        can jump throuogh
        """
        trails = []
        directions = [-1,1]
        current_piece = self.game_board[pos[0]][pos[1]]
        #assert current_piece.is_king is False
        if self.can_jump(pos,team,True) is False:
            return [[]]
        for i in directions:
            if (self.is_valid_position(((pos[0] + i),pos[1] + 1)) and
                self.game_board[pos[0] + i][pos[1] + 1] is not None):
                if (self.game_board[(pos[0] + i)][pos[1] + 1].team !=team 
                    and self.is_valid_position(((pos[0] + 2*i),pos[1] + 2))):
                    if ((self.game_board[pos[0] + 2*i][pos[1] + 2] is None
                        and ((pos[0] + 2*i),(pos[1] + 2))!= original_pos and ((pos[0] + 2*i),(pos[1] + 2)) 
                        not in already_jumped)):
                        for trail in (self.jump_trail_king((pos[0] + 2*i,pos[1] + 2),original_pos,pos,already_jumped + [pos],team)):
                            trails.append(
                            [((pos[0] + 2*i),(pos[1] + 2))] + trail)
                    elif ((pos[0] + 2*i),(pos[1] + 2)) == original_pos and original_pos != prev_pos:
                        trails.append([((pos[0] + 2*i),(pos[1] + 2))])
                
                    #else:
                        #trails.append([])
            if (self.is_valid_position(((pos[0] + i),pos[1] - 1)) and
                self.game_board[pos[0] + i][pos[1] - 1] is not None):
                if (self.game_board[(pos[0] + i)][pos[1] - 1] != team and 
                    self.is_valid_position(((pos[0] + 2*i),pos[1] - 2))):
                    if (self.game_board[pos[0] + 2*i][pos[1] - 2] is None
                        and ((pos[0] + 2*i),(pos[1] -2))!= original_pos and ((pos[0] + 2*i),(pos[1] - 2)) 
                        not in already_jumped):
                        
                        for trail in (self.jump_trail_king((pos[0] + 2*i,pos[1] - 2),original_pos,pos, already_jumped + [pos],team)):
                            trails.append(
                            [((pos[0] + 2*i),(pos[1] - 2))] + trail)
                    elif ((pos[0] + 2*i),(pos[1] - 2)) == original_pos and original_pos != prev_pos:
                        trails.append([((pos[0] + 2*i),(pos[1] - 2))])
                    
                    #else:
                        #trails.append([])
                        
    
        
        return trails

   
    def list_moves_piece(self,pos,team):
        current_piece = self.game_board[pos[0]][pos[1]]
        positions = []
        if self.can_jump(pos,team,False):
            for trail in self.jump_trail_piece(pos,team):
                positions.append(trail[len(trail) - 1])
        if self.is_valid_position(((pos[0] + current_piece.dir),(pos[1] + 1))):
            if self.game_board[pos[0] + current_piece.dir][pos[1] + 1] is None:
                positions.append(((pos[0] + current_piece.dir),(pos[1] + 1)))
        if self.is_valid_position(((pos[0] + current_piece.dir),(pos[1] - 1))):
            if self.game_board[pos[0] + current_piece.dir][pos[1] - 1] is None:
                positions.append(((pos[0] + current_piece.dir),(pos[1] - 1)))
        return positions

        

    def list_moves_king(self,pos,team):
        current_piece = self.game_board[pos[0]][pos[1]]
        positions = []
        directions = [-1,1]
        if self.can_jump(pos,team,True):
            for trail in self.jump_trail_king(pos,pos,None,[],team):
                positions.append(trail[len(trail) - 1])
        for i in directions:
            if self.is_valid_position(((pos[0] + i),(pos[1] + 1))):
                if self.game_board[pos[0] + i][pos[1] + 1] is None:
                    positions.append(((pos[0] + i),(pos[1]+1)))
            if self.is_valid_position(((pos[0] + i),(pos[1] - 1))):
                if self.game_board[pos[0] + i][pos[1]-1] is None:
                    positions.append(((pos[0] + i),(pos[1] - 1)))
        
        
        return positions
        




    def is_valid_move(self, curr_pos, new_pos):
        """
        Determines if moving from one position to another is a valid move
        Parameters:
            curr_pos(tup): the current positions
            new_pos(tup): the final position
        Returns(bool): If the piece at the current position can jump to the new
        position
        """
        
        current_piece = self.game_board[curr_pos[0]][curr_pos[1]]
        if new_pos not in self.list_moves(curr_pos): # why is current_piece necessary here?
            return False
        return True

    def remove_pieces(self,pos,team):
        self.red_pieces = set()
        self.black_pieces = set()
        for i in range(self.width):
            for j in range(self.width):
                if self.game_board[i][j] is not None:
                    if self.game_board[i][j].x_pos != pos[1] or self.game_board[i][j].y_pos != pos[0]:
                        self.game_board[i][j] = None
        self.game_board[pos[0]][pos[1]].is_king = True
        if team == "Red":
            self.red_pieces.add(Piece(pos,"Red", True))
        if team == "Black":
            self.black_pieces.add(Piece(pos,"Red",True))
    
    def add_piece(self,pos,team):
        self.game_board[pos[0]][pos[1]] = Piece((pos[0],pos[1]),team)
        if team == "Red":
            self.red_pieces.add(Piece((pos[0],pos[1]),team))
        if team == "Black":
            self.black_pieces.add(Piece((pos[0],pos[1]),team))


        
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
            the Piece object (row, col)
            team(TeamColor) - the team the Piece is on

        Returns: None
        """
        #Piece's position represented by an (int, int) tuple with (x,y) position

        # Piece's x position or col
        self.x_pos = pos[1]

        # Piece's y position or row
        self.y_pos = pos[0]
        self.pos = (self.y_pos,self.x_pos)

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
        assert self.space_color == 'dark'
    
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
                return "|R|"
            return "|B|"
       

    def update_position(self, pos):
        """
        Changes the x and y positions of the piece. Does not check if the new 
        position is valid or not.
        Args:
            pos(tuple) - a tuple with two values, representing the new position 
            of the Piece object
        Returns: None
        """
        self.y_pos = pos[0]
        self.x_pos = pos[1]
        self.pos = pos
        

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
        if self.is_king is False:
            if self.team == "Red":
                if (abs(new_pos[1] - self.y_pos) == 1 and new_pos[0] - self.x_pos == -1):
                    return True
                return False
                
            if self.team == "Black":
                if (abs(new_pos[1] - self.y_pos) == 1 and new_pos[0] - self.x_pos == 1):
                    return True
                return False    
                
        if self.is_king is True:
            if (abs(new_pos[1] - self.y_pos) == 1 and abs(new_pos[0] - self.x_pos) == 1):
                return True
            return False
    
   

        





#board = Game(3)
#print(board)

#board.all_team_moves("Black")
#print(board.is_winner("Red"))
#print(board.game_board[5][2])
#print(type(board.game_board[5][2]))g

from typing import Union
from mocks import StubCheckerboard, MockGame
GameType = Union[Game, MockGame, StubCheckerboard]