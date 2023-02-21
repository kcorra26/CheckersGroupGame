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

class Piece:
    def __init__(self, team:TeamColor, pos:tuple = (0,0), is_king=False):
        '''
        pos = (col, row) or (x,y) with (0,0) being in the top right
        '''
        self.team = team
        self.is_king = is_king
        self.pos = pos

