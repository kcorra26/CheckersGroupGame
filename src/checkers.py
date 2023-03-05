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
        Returns (str): string representation of the board
        """
        s = ""
        for row in self.board:
            for spot in row:
                s+= "| |"
            s += "\n" 
        return s
    
    def add_piece(self,piece):
        """
        Adds a piece to the board.
        Parameters (Piece): Piece being added
        Returns: None
        """
        self.board[piece.y_pos][piece.x_pos] = piece
        
    
    def get_piece(self,pos):
        """
        Returns the piece specified at the position.
        Parameters(tup): Position of the Piece
        Returns: None if there is not piece at the position or the piece at the
        position
        """
        return self.board[int(pos[0])][int(pos[1])]
    
    def remove_piece(self,pos):
        """
        Removes a piece at a position and replaces it with a None object
        Parameters(pos): Position of the piece being removed
        Returns: None
        """
        self.board[pos[0]][pos[1]] = None

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
        s = ""
        for row in self.game_board.board:
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
        for spot in self.game_board.board[0]:
            if spot is not None and spot.is_king is False and (
                spot.team == "Red"):
                self._remove_piece((spot.y_pos,spot.x_pos),"Red")
                spot.is_king = True
                self.red_pieces.add(spot)
                
        for spot in self.game_board.board[self.width - 1]:
            if (spot is not None and 
                spot.is_king is False and spot.team == "Black"):
                self._remove_piece((spot.y_pos,spot.x_pos),"Black")
                spot.is_king = True
                self.black_pieces.add(spot)
                
    
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
        current_piece = self.game_board.board[old_pos[0]][old_pos[1]]
        if self.is_valid_move(old_pos,new_pos):
            if team == "Red" and current_piece.is_king is False and \
            new_pos[0] == 0:
                return True
            if team == "Black" and current_piece.is_king is False and \
            new_pos[0] == self.width - 1:
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
        if self.find_correct_sequence(old_pos,new_pos,team) is not None: 
            return len(self.find_correct_sequence(old_pos,new_pos,team))
        return 0


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
        original_set = None
        exists = False
        current_piece = self.game_board.get_piece(old_pos)
        is_winner = None
        original_set_red = set()
        original_set_black = set()
        middle_pos = []
        initial_pos = self.game_board.get_piece(old_pos)
        initial_pos_is_king = False
        if initial_pos.is_king is True:
            initial_pos_is_king = True
        end_pos = self.game_board.get_piece(new_pos)
        if abs(new_pos[1] - old_pos[1]) != 1 and \
        abs(new_pos[0] - old_pos[0]) != 1:
            for pos in self.middle_positions(old_pos,new_pos,team_making):
                middle_pos.append(self.game_board.get_piece(pos))
        for piece in self.red_pieces:
            original_set_red.add(piece)
        for piece in self.black_pieces:
            original_set_black.add(piece)
        
        if self.is_valid_move(old_pos,new_pos):
            self.move_piece(old_pos,new_pos, team_making, True)
            is_winner = self.is_winner(team_would_win)
        if middle_pos != [] :       
            for pos in middle_pos:
                self.game_board.add_piece(pos) 
        self.red_pieces = original_set_red
        self.black_pieces = original_set_black
        
        if old_pos != new_pos:
            initial_pos.update_position(old_pos)
            initial_pos.is_king = initial_pos_is_king
            self.game_board.add_piece(initial_pos)
            self.game_board.board[new_pos[0]][new_pos[1]] = None
        return is_winner
    
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
                
    def move_piece(self, old_pos, new_pos, team, checking_winner=False):
        """
        Ensures the piece is in play, moves the piece at the old position to 
        the new position if the move is valid, and notifies the player 
        if invalid. If the Piece reaches the end of the board and is not 
        already a king, it changes into a King object. If the piece involves
        jumps, the jump_piece method is called. 
        Parameters:
            old_pos: tuple(int, int)
            new_pos: tuple(int, int)
            team(str): team of piece being moved
            checking_winner(bool): if the game is checking for a winner
        Returns: None
        """
        current_piece = self.game_board.get_piece(old_pos)
        if new_pos in self.list_moves(old_pos):
            if abs(new_pos[0] - old_pos[0]) == 1 and \
            (abs(new_pos[1] - old_pos[1])== 1): 
                self.game_board.board[new_pos[0]][new_pos[1]] = current_piece
                self.game_board.board[new_pos[0]][new_pos[1]].update_position(new_pos)
                self.game_board.board[old_pos[0]][old_pos[1]] = None
                if team == "Red":
                    for piece in self.red_pieces:
                        if piece.x_pos == old_pos[1] and piece.y_pos == old_pos[0]:
                            self.red_pieces.remove(piece)
                            self.red_pieces.add(self.game_board.board[new_pos[0]][new_pos[1]])
                if team == "Black":
                    for piece in self.black_pieces:
                        if piece.x_pos == old_pos[1] and \
                        piece.y_pos == old_pos[0]:
                            self.black_pieces.remove(piece)
                            self.black_pieces.add(self.game_board.board[new_pos[0]][new_pos[1]])
                self.make_king()

                if not checking_winner:
                    if team == "Red":
                        self.since_piece_removed_red += 1
                    if team == "Black":
                        self.since_piece_removed_black += 1
            else: 
                self.jump_piece(old_pos, new_pos, team)
                if not checking_winner:
                    if team == "Red":
                        self.since_piece_removed_red = 0
                    if team == "Black":
                        self.since_piece_removed_black = 0
        else:
            print("invalid move")


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
        choose_sequence = None 
        current_piece = self.game_board.board[old_pos[0]][old_pos[1]]
        if current_piece.is_king is False:
            for sequence in self.jump_trail_piece(old_pos,team):
                if len(sequence) > 0:
                    if choose_sequence is None and \
                    sequence[len(sequence) - 1] == new_pos:
                        choose_sequence = sequence
                    elif choose_sequence != None and \
                    sequence[len(sequence) - 1] == new_pos:
                        if len(choose_sequence) < len(sequence):
                            choose_sequence = sequence
            return choose_sequence
        if current_piece.is_king is True:
            for sequence in self.jump_trail_king(old_pos, old_pos, None, [], team):
                if len(sequence) > 0:
                    if (choose_sequence == None and 
                        sequence[len(sequence) - 1] == new_pos):
                        choose_sequence = sequence
                    elif choose_sequence != None and \
                    sequence[len(sequence) - 1] == new_pos:
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
        full_sequence = [old_pos] + \
        self.find_correct_sequence(old_pos,new_pos,team)
        
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
        current_piece = self.game_board.board[old_pos[0]][old_pos[1]]
        if self.is_valid_move(old_pos,new_pos):
            for pos in self.middle_positions(old_pos,new_pos,team):
                
                if team == "Red":
                    self._remove_piece((int(pos[0]),int(pos[1])),"Black")
                if team == "Black":
                    self._remove_piece((int(pos[0]),int(pos[1])),"Red")
                self.game_board.remove_piece((int(pos[0]),int(pos[1])) )
            if old_pos != new_pos:
                self._remove_piece(old_pos,team)
                self.game_board.board[int(old_pos[0])][int(old_pos[1])] = None
                self.game_board.board[int(new_pos[0])][int(new_pos[1])] = current_piece
                self.game_board.board[int(new_pos[0])][int(new_pos[1])].update_position((new_pos[0],new_pos[1]))
                if team == "Red":
                    self.red_pieces.add(self.game_board.board[int(new_pos[0])][int(new_pos[1])])
            
                if team == "Black":
                    self.black_pieces.add(self.game_board.board[int(new_pos[0])][int(new_pos[1])])
                self.make_king()

        
    def _remove_piece(self, pos,team):
        """
        Removes a piece at a specific position.
        Parameters: 
            pos: tuple(int, int)
            team: team of the piece
        Returns: None
        """
        piece = self.game_board.get_piece(pos)
        if team == "Black":
            self.black_pieces.remove(piece)
        else:
            self.red_pieces.remove(piece)
    def _initialize_checkers(self):
        """
        Adds all the pieces to the board in starting positions and to the 
        respective team sets
        Parameters: None
        Returns: None
        """
        for i in range(self._num_rows):
            for j in range(self.width):
                if (i + j) % 2 == 1:
                    piece = Piece((i,j),"Black")
                    self.game_board.add_piece(piece)
                    self.black_pieces.add(piece)
        for i in range(self.width - self._num_rows, self.width):
            for j in range(self.width):
                if (i + j) % 2 == 1:
                    piece = Piece((i,j),"Red")
                    self.game_board.add_piece(piece)
                    self.red_pieces.add(piece)
    
    def reset_game(self):
        """
        Resets the game, putting the pieces back to where they were initially
        and refilling the red and black piece set
        Parameters:None
        Returns:None
        """
        self.red_pieces = set()
        self.black_pieces = set()
        self.red_wants_to_draw = False
        self.black_wants_to_draw = False
        self.since_piece_removed_black = 0
        self.since_piece_removed_red = 0
        for i in range(self.width):
            for j in range(self.width):
                if self.game_board.board[i][j] is not None:
                    self.game_board.board[i][j] = None
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
                    team_moves[(piece.y_pos,piece.x_pos)] = \
                    self.list_moves((piece.y_pos,piece.x_pos))
        if team == "Black":
            for piece in self.black_pieces:
                if self.can_move((piece.y_pos,piece.x_pos)):
                    team_moves[(piece.y_pos,piece.x_pos)] = \
                    self.list_moves((piece.y_pos,piece.x_pos))
        
        return team_moves
                        
    def is_winner(self, team): 
        """
        Determines if the given team is the winner
        Args:
            team(TeamColor) - the team who is being checked if it is winner
        Returns (bool): whether the specified team is a winner
        """
        if team == "Red":
            if len(self.black_pieces) == 0 or \
            len(self.all_team_moves("Black")) == 0:
                return True
            return False
        if team == "Black":
            if len(self.red_pieces) == 0 or \
            len(self.all_team_moves("Red")) == 0:
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
        current_piece = self.game_board.get_piece(pos)
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
        current_spot = self.game_board.get_piece(pos)
        directions = [-1,1]
        direction = None
        if team == "Red":
            direction = -1
        if team == "Black":
            direction = 1
        if (current_spot is None and is_king is False) or \
        (current_spot is not None and is_king is False):
            if self.is_valid_position((pos[0] + direction, pos[1] + 1)):
                if (self.game_board.board[pos[0] + direction][pos[1] + 1] is not None
                    and self.game_board.board[pos[0] + direction][pos[1] + 1].team != team):
                    if (self.is_valid_position((pos[0] + 2* direction, pos[1] + 2)) and
                        self.game_board.board[pos[0] + 2*direction][pos[1] + 2] is None):
                        return True
            if self.is_valid_position((pos[0] + direction, pos[1] - 1)):
                if (self.game_board.board[pos[0] + direction][pos[1] - 1] is not None
                    and self.game_board.board[pos[0] + direction][pos[1] - 1].team != team):
                    if (self.is_valid_position((pos[0] + 2*direction, pos[1] - 2)) and
                        self.game_board.board[pos[0] + 2*direction][pos[1] - 2] is None):
                        return True
        elif (current_spot is None and is_king is True) or \
        (current_spot is not None and current_spot.is_king is True):
            for i in directions:
                if self.is_valid_position((pos[0] + i, pos[1] + 1)):
                    if (self.game_board.board[pos[0] + i][pos[1] + 1] is not None
                        and self.game_board.board[pos[0] + i][pos[1] + 1].team != team):
                        if (self.is_valid_position((pos[0] + 2*i, pos[1] + 2)) and
                            self.game_board.board[pos[0] + 2*i][pos[1] + 2] is None):
                            return True
                if self.is_valid_position((pos[0] + i, pos[1] - 1)):
                    if (self.game_board.board[pos[0] + i][pos[1] - 1] is not None
                        and self.game_board.board[pos[0] + i][pos[1] - 1].team != team):
                        if (self.is_valid_position((pos[0] + 2*i, pos[1] - 2)) and
                            self.game_board.board[pos[0] + 2*i][pos[1] - 2] is None):
                            return True
        return False
    
    
    def jump_trail_piece(self,pos,team):
        """
        Returns a sequences representing all the possible ways a piece can jump
            Parameters:
            pos(tup): position of the piece
            team: team of piece
        Returns(list): A list of lists of all the sequences a piece can jump through
        """
        trails = []
        current_piece = self.game_board.board[pos[0]][pos[1]]
        direction = None
        if team == "Red":
            direction = -1
        else:
            direction = 1
        if not self.can_jump(pos,team,False):
            return []
        if self.can_jump(pos,team,False):
            if (self.is_valid_position(((pos[0] + direction),pos[1] + 1)) and
                (self.game_board.board[pos[0] + direction][pos[1] + 1] is not None)):
                if (self.game_board.board[(pos[0] + direction)][pos[1] + 1].team != team and 
                    self.is_valid_position(((pos[0] + 2*direction),pos[1] + 2))):
                    if self.game_board.board[pos[0] + 2*direction][pos[1] + 2] is None:
                        if self.can_jump((pos[0] + 2*direction,pos[1] + 2),team,False) is False:
                            trails.append([(pos[0] + 2*direction,pos[1] + 2)])
                        for trail in self.jump_trail_piece((pos[0] + 2*direction,pos[1] + 2),team):
                            trails.append([(pos[0] + 2*direction,pos[1] + 2)] + trail)
            if (self.is_valid_position(((pos[0] + direction),pos[1] - 1)) and
                (self.game_board.board[(pos[0] + direction)][pos[1] - 1] is not None)):
                if ((self.game_board.board[(pos[0] + direction)][pos[1] - 1].team != team) and 
                    self.is_valid_position(((pos[0] + 2*direction),pos[1] - 2))):
                    if self.game_board.board[pos[0] + 2*direction][pos[1] - 2] is None:
                        if self.can_jump((pos[0] + 2*direction,pos[1] - 2),team,False) is False:
                            trails.append([(pos[0] + 2*direction,pos[1] - 2)])
                        for trail in self.jump_trail_piece((pos[0] + 2*direction,pos[1] - 2),team):
                            trails.append([(pos[0] + 2*direction,pos[1] - 2)] + trail)
            return trails
    
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
        trails = []
        directions = [-1,1]
        current_piece = self.game_board.board[pos[0]][pos[1]]
        for i in directions:
            if (self.is_valid_position(((pos[0] + i),pos[1] + 1)) and
                self.game_board.board[pos[0] + i][pos[1] + 1] is not None):
                if (self.game_board.board[(pos[0] + i)][pos[1] + 1].team !=team 
                    and self.is_valid_position(((pos[0] + 2*i),pos[1] + 2))):
                    if ((self.game_board.board[pos[0] + 2*i][pos[1] + 2] is None
                        and ((pos[0] + 2*i),(pos[1] + 2))!= original_pos and 
                        ((pos[0] + 2*i),(pos[1] + 2)) not in already_jumped)):
                        if self.jump_trail_king((pos[0] + 2*i,pos[1] + 2),original_pos,pos,already_jumped + [pos],team) != []:
                            for trail in (self.jump_trail_king((pos[0] + 2*i,pos[1] + 2),original_pos,pos,already_jumped + [pos],team)):
                                trails.append(
                                [((pos[0] + 2*i),(pos[1] + 2))] + trail)
                        else:
                            trails.append([((pos[0] + 2*i),(pos[1] + 2))])
                    elif ((pos[0] + 2*i),(pos[1] + 2)) == original_pos and original_pos != prev_pos:
                        trails.append([((pos[0] + 2*i),(pos[1] + 2))])
            if (self.is_valid_position(((pos[0] + i),pos[1] - 1)) and
                self.game_board.board[pos[0] + i][pos[1] - 1] is not None):
                if (self.game_board.board[(pos[0] + i)][pos[1] - 1].team != team
                    and self.is_valid_position(((pos[0] + 2*i),pos[1] - 2))):
                    if (self.game_board.board[pos[0] + 2*i][pos[1] - 2] is None
                        and ((pos[0] + 2*i),(pos[1] -2))!= original_pos and ((pos[0] + 2*i),(pos[1] - 2)) 
                        not in already_jumped):
                        if self.jump_trail_king((pos[0] + 2*i,pos[1] - 2),original_pos,pos,already_jumped + [pos],team) != []:
                            for trail in (self.jump_trail_king((pos[0] + 2*i,pos[1] - 2),original_pos,pos, already_jumped + [pos],team)):
                                trails.append(
                                [((pos[0] + 2*i),(pos[1] - 2))] + trail)
                        else:
                            trails.append([((pos[0] + 2*i),(pos[1] - 2))])
                    elif ((pos[0] + 2*i),(pos[1] - 2)) == original_pos and \
                    original_pos != prev_pos:
                        trails.append([((pos[0] + 2*i),(pos[1] - 2))])
                        
        return trails
   
    def list_moves_piece(self,pos,team):
        """
        Lists all the moves a piece can make
        Parameters:
            pos(tup): The position of the piece
            team(str): The team of the piece
        Returns(lst): List of all locations a piece can go to
        """
        current_piece = self.game_board.get_piece(pos)
        positions = []
        if self.can_jump(pos,team,False):
            for trail in self.jump_trail_piece(pos,team):
                positions.append(trail[len(trail) - 1])
        if self.is_valid_position(((pos[0] + current_piece.dir),(pos[1] + 1))):
            if self.game_board.board[pos[0] + current_piece.dir][pos[1] + 1] is None:
                positions.append(((pos[0] + current_piece.dir),(pos[1] + 1)))
        if self.is_valid_position(((pos[0] + current_piece.dir),(pos[1] - 1))):
            if self.game_board.board[pos[0] + current_piece.dir][pos[1] - 1] is None:
                positions.append(((pos[0] + current_piece.dir),(pos[1] - 1)))
        return positions
        
    def list_moves_king(self,pos,team):
        """
        Lists all the moves a king can make
        Parameters:
            pos(tup): The position of the king
            team(str): The team of the piece
        Returns(lst): List of all locations a king can go to
        """
        current_piece = self.game_board.board[pos[0]][pos[1]]
        positions = []
        directions = [-1,1]
        if self.can_jump(pos,team,True):
            for trail in self.jump_trail_king(pos,pos,None,[],team):
                positions.append(trail[len(trail) - 1])
        for i in directions:
            if self.is_valid_position(((pos[0] + i),(pos[1] + 1))):
                if self.game_board.board[pos[0] + i][pos[1] + 1] is None:
                    positions.append(((pos[0] + i),(pos[1]+1)))
            if self.is_valid_position(((pos[0] + i),(pos[1] - 1))):
                if self.game_board.board[pos[0] + i][pos[1]-1] is None:
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
        if new_pos not in self.list_moves(curr_pos):
            return False
        return True
   
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
        if self.all_team_moves("Red") == {} and \
        self.all_team_moves("Black") == {}:
            return True
        if self.since_piece_removed_black >= 40 or \
        self.since_piece_removed_red >= 40: 
            return True
        if self.red_wants_to_draw and self.black_wants_to_draw: 
            return True
        return False

    def piece_at_pos(self,pos):
        """
        Returns the piece at a position. Similar to the Board Class's get_piece
        function, but this is for GUI purposes.

        Parameters:
            pos(tup):Position of piece
        Returns (Piece): Piece at the position
        """
        return self.game_board.get_piece(pos)

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
        if team == "Red":
            self.red_wants_to_draw = True
        elif team == "Black":
            self.black_wants_to_draw = True
    
    def response_to_draw(self,team,wants_to_draw):
        """
        Allows a team to respond to a draw if the other team proposes to draw. 

        Parameters:
            team(str): team that is deciding whether to agree to a draw
        Returns: None
        """
        if team == "Red":
            if wants_to_draw is True:
                self.red_wants_to_draw = True
            else:
                self.black_wants_to_draw = False

        if team == "Black":
            if wants_to_draw is True:
                self.black_wants_to_draw = True
            else:
                self.red_wants_to_draw = False


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
                if (abs(new_pos[1] - self.y_pos) == 1 and \
                new_pos[0] - self.x_pos == -1):
                    return True
                return False
                
            if self.team == "Black":
                if (abs(new_pos[1] - self.y_pos) == 1 and \
                new_pos[0] - self.x_pos == 1):
                    return True
                return False    
                
        if self.is_king is True:
            if (abs(new_pos[1] - self.y_pos) == 1 and \
            abs(new_pos[0] - self.x_pos) == 1):
                return True
            return False
        
    
   
from typing import Union
from mocks import StubCheckerboard, MockGame
GameType = Union[Game, MockGame, StubCheckerboard]