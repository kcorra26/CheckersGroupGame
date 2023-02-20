from enum import Enum
TeamColor = Enum("TeamColor",  ["RED", "BLACK", "EMPTY"]) 

class StubCheckerboard:
    def __init__(self, n):
        self.n = n
        self.width = 2*n + 2

    def __str__(self):
        return("board")
