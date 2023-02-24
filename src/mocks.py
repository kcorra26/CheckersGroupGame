from typing import Optional, List, Union

#was being used in GUI - am not trying to integrate Game as 
class StubCheckerboard:
    def __init__(self, n=3):
        self.n = n
        self.width = 2*n + 2
        self.red_pieces = [Piece('Red', (1,0)), Piece('Red', (3,0), True), Piece('Red', (3,2)), Piece('Red', (4,6))]
        self.black_pieces = [Piece('Black', (4,5), True), Piece('Black', (7,0)), Piece('Black', (2,3))]
        self.is_winner = None

    def __str__(self):
        return("board")
    
    def move_piece(self, old_pos, new_pos:tuple = (0,0)):
        row, col = old_pos
        piece = self.get_piece(row, col)
        piece.update_pos(new_pos)
    
    def get_piece(self, row, col):
        for piece in self.red_pieces + self.black_pieces:
            if piece.pos == (row, col):
                return piece
        return None
    
    def list_moves(self, piece):
        return [(0,0), (7,0), (3,4), (5,7), (3,6), (5,3), (0,3)]
    
    def set_winner(self, team):
        self.is_winner = team
    def is_winner(self):
        return self.is_winner

#Bot
class CheckersGameBotMock: # game mock?
    def __init__(self, n=3):
        self.n = n 
        self.width = 2*n + 2
        self.board = MockCheckerboard(n)
        self.red_pieces = set([Piece('Red', (1,2)), Piece('Red', (3,0), True), Piece('Red', (3,2)), Piece('Red', (6,2))])
        self.black_pieces = set([Piece('Black', (4,5), True), Piece('Black', (7,0)), Piece('Black', (2,3))])
        # self.board?
    
    def __str__(self) -> str:
        return "BOARD"
    
    def all_team_moves(self, team):
        return {(1, 2) : [(2, 3), (2, 1)], 
                (3, 0): [(2,3), (5,0)],
                (3, 2) : [(5, 3), (5, 0), (6, 0)], 
                (6, 2) : [(7, 3), (7, 0), (7,2)], 
                (4,5): [(1,2)],
                (7,0): [(5,0), (7,3), (6,0)], 
                (2,3): [(5,0)]} 

    def is_done(self):
        return False
    
    def will_king(self, og_pos, end_pos, team): 
        row, col = end_pos
        if row == self.width - 1:
            return True
        return False
    
    def num_jumps(self, og_pos, end_pos):
        og_row, _ = og_pos
        end_row, _ = end_pos
        return abs(end_row - og_row - 1)
    
    def is_winning_move(self, og_pos, end_pos, team):
        #row, _ = og_pos
        #if row == 6:
            #return True
        return False
    def get_piece(self, row, col):
        for piece in self.red_pieces.union(self.black_pieces):
            if piece.pos == (row, col):
                return piece
    def list_moves(self, piece):
        return self.all_team_moves(3)[piece.pos]

    def move_piece(self, old_pos, new_pos:tuple = (0,0)):
        row, col = old_pos
        piece = self.get_piece(row, col)
        piece.update_pos(new_pos)

#mock game and board
class Piece:
    def __init__(self, team:str, pos:tuple = (0,0), is_king=False):
        '''
        pos = (row, col) or (y,x) with (0,0) being in the top right
        '''
        self.team = team
        self.is_king = is_king
        self.col = pos[1]
        self.row = pos[0]
        self.pos = pos
    
    def update_pos(self, new_pos):
        self.col = new_pos[1]
        self.row = new_pos[0]
        self.pos = new_pos

class MockGame:
    def __init__(self, n=3):
        self.board = MockCheckerboard(n)
        self.n = n
        self.width = 2*n + 2
        self.is_winner = None
        self.red_pieces = set([Piece('Red', (1,0)), Piece('Red', (3,0), True), Piece('Red', (3,2)), Piece('Red', (4,6))])
        self.black_pieces = set([Piece('Black', (4,5), True), Piece('Black', (7,0)), Piece('Black', (2,3))])
        pass
    def __str__(self):
        return "Game"
    def is_valid_move(self, curr_pos, new_pos):
        return True
    def all_team_moves(self, team):
        return {(3,3):[(4,5),(5,6)]}
    def _set_winner(self, team):
        self.is_winner=team
    def get_piece(self, row, col):
        for piece in self.red_pieces.union(self.black_pieces):
            if piece.pos == (row, col):
                return piece
    def list_moves(self, p: Piece):
        return [(0,0), (7,0), (3,4), (5,7), (3,6), (5,3), (0,3)]
    def move_piece(self, old_pos, new_pos:tuple = (0,0)):
        row, col = old_pos
        piece = self.get_piece(row, col)
        piece.update_pos(new_pos)

class MockCheckerboard:

    def __init__(self, n, kings=False):
        self.board = [[None, Piece("Black", (0,1)), None, Piece("Black",(0,3)), None, Piece("Black",(0,5))],
                      [Piece("Black", (1,0)), None, Piece("Black",(1,2), is_king=True), None,Piece("Black", (1,4)), None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, Piece("Red", (4,1)), None, Piece('Red', (4,3)), None, Piece("Red", (4,5))],
                      [Piece("Red", (5,0)), None, Piece("Red",(5,2), is_king=True), None, Piece("Red", (5,4)), None]]
        self.is_winner = None
        self.n = n
        #self.width = 2*n + 2
        self.width = len(self.board)
        self.n = int((self.width - 2) // 2)
    def set_winner(self, team):
        self.is_winner = team
    def is_winner(self):
        return self.is_winner



class StubRandomBot:
    def __init__(self):
        pass

class StubSmartBot:
    def __init__(self):
        pass