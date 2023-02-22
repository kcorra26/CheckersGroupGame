from enum import Enum
TeamColor = Enum("TeamColor",  ["RED", "BLACK", "EMPTY"]) 

B = 'black'
R = 'red'

class StubCheckerboard:
    def __init__(self, n=3):
        self.n = n
        self.width = 2*n + 2
        self.red_pieces = [Piece('RED', (1,0)), Piece('RED', (3,0), True)]
        self.black_pieces = [Piece('BLACK', (4,5), True), Piece('BLACK', (7,0)), Piece('Black', (4,3))]

        self.board=[[None, Piece('BLACK'), None, Piece('BLACK'), None,  Piece('BLACK'), None, Piece('BLACK')],
                    [Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None, Piece('BLACK'), None ],
                    [None, Piece('BLACK'), None, Piece('BLACK', True), None, Piece('BLACK'), None, Piece('BLACK')],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [Piece('RED', True), None, Piece('RED'), None, Piece('RED'), None, Piece('RED', True), None],
                    [None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED')],
                    [Piece('RED'), None, Piece('RED'), None, Piece('RED'), None, Piece('RED'), None]]

    def __str__(self):
        return("board")
    
    def move_piece(self, old_pos, new_pos:tuple = (0,0)):
        col, row = old_pos
        piece = self.get_piece(col, row)
        piece.update_pos(new_pos)
    
    def get_piece(self, col, row):
        for piece in self.red_pieces + self.black_pieces:
            if piece.pos == (col,row):
                return piece
        return None
    
    def list_moves(self, piece):
        return [(0,0), (7,0), (3,4), (5,7)]

class Piece:
    def __init__(self, team:TeamColor, pos:tuple = (0,0), is_king=False):
        '''
        pos = (col, row) or (x,y) with (0,0) being in the top right
        '''
        self.team = team
        self.is_king = is_king
        self.pos = pos
    
    def update_pos(self, new_pos):
        self.pos = new_pos

class CheckersGameBotMock: # game mock?
    def __init__(self, n=3):
        self.n = n 
        self.width = 2*n + 2
        # self.board?
    
    def __str__(self) -> str:
        return "BOARD"
    
    def all_team_moves(self, team):
        return {(1, 2) : [(2, 3), (2, 1)], (3, 2) : [(5, 3), (5, 0), (7, 0)], 
                (6, 2) : [(7, 3), (7, 0)]} 

    def is_done(self):
        return False
    
    def will_king(self, og_pos, end_pos): 
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
