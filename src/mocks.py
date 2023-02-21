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



    

