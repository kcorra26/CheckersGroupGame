from enum import Enum
TeamColor = Enum("TeamColor",  ["RED", "BLACK", "EMPTY"]) 

B = 'black'
R = 'red'

class StubCheckerboard:
    def __init__(self, n=3):
        self.n = n
        self.width = 2*n + 2
        self.red_pieces = [Piece('RED', (1,0)), Piece('RED', (3,0), True), Piece('RED', (3,2)), Piece('RED', (4,6))]
        self.black_pieces = [Piece('BLACK', (4,5), True), Piece('BLACK', (7,0)), Piece('BLACK', (2,3))]

        '''self.board=[[None, Piece('BLACK'), None, Piece('BLACK'), None,  Piece('BLACK'), None, Piece('BLACK')],
                    [Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None ],
                    [None, Piece('BLACK'), None, Piece('BLACK', True), None, Piece('BLACK'), None, Piece('BLACK')],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [Piece('RED', True), None, Piece('RED'), None, Piece('RED'), None, Piece('RED', True), None],
                    [None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED')],
                    [Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None]]'''

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

class Piece:
    def __init__(self, team:TeamColor, pos:tuple = (0,0), is_king=False):
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

class CheckersGameBotMock: # game mock?
    def __init__(self, n=3):
        self.n = n 
        self.width = 2*n + 2
        # self.board?
    
    def __str__(self) -> str:
        return "BOARD"
    
    def all_team_moves(self, team):
        return {(1, 2) : [(2, 3), (2, 1)], (3, 2) : [(5, 3), (5, 0), (6, 0)], 
                (6, 2) : [(7, 3), (7, 0)]} 

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

class MockGame:
    def __init__(self, n=3):
        self.board = MockCheckerboard(n)
        self.n = n
        self.width = 2*n + 2
        pass
    def __str__(self):
        return "Game"
    def is_valid_move(self, curr_pos, new_pos):
        return True
    def all_team_moves(self, team):
        return {(3,3):[(4,5),(5,6)]}
    


class MockCheckerboard:

    def __init__(self, n, kings=False):
        self.grid=[[None, Piece('BLACK'), None, Piece('BLACK'), None,  Piece('BLACK'), None, Piece('BLACK')],
                    [Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None ],
                    [None, Piece('BLACK'), None, Piece('BLACK', True), None, Piece('BLACK'), None, Piece('BLACK')],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [Piece('RED', True), None, Piece('RED'), None, Piece('RED'), None, Piece('RED', True), None],
                    [None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED')],
                    [Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None]]
        self.n = n
        self.width = 2*n + 2

class StubRandomBot:
    def __init__(self):
        pass

class StubSmartBot:
    def __init__(self):
        pass