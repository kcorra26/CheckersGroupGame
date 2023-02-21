from enum import Enum
TeamColor = Enum("TeamColor",  ["RED", "BLACK", "EMPTY"]) 

B = 'black'
R = 'red'

class StubCheckerboard:
    def __init__(self, n=3):
        self.n = n
        self.width = 2*n + 2
        self.board=[[None, B, None, B, None,  B, None, B],
                    [B, None, B, None, B, None, B, None ],
                    [None, B, None, None, None,  B, None, B],
                    [None, None, None, B, None, None, None, None],
                    [None, None, R, None, None, None, None, None],
                    [R, None, R, None, R, None, None, None],
                    [None, R, None, R, None, R, None, R],
                    [R, None, R, None, R, None, R, None]]

    def __str__(self):
        return("board")
    

