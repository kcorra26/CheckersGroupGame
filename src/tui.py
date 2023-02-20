"""
TUI for Checkers
"""
import time 
from typing import Union, Dict


#from checkers import TeamColor, Board, Empty, Piece, King
from mocks import TeamColor, StubCheckerboard

"""
Things that the TUI needs to do
-display the board with a width of 2n+2/self.width of the board itself
-display pieces on the board
-visually demarcate regular pieces and Kings


commands it will need to support
-just starting the game
-setting player 2 to be a bot (either random or smart)
-moving pieces: maybe choose piece and then choose direction?
-winning game and ending it
-drawing
-resigning
"""



def play_checkers(board):
    """
    This prints out/draws the board in its starting position for a game of 
    checkers
    
    """
    #black goes first
    current = TeamColor.BLACK
    width = board.width

    #hard coded for regular checkerboard/n=2/width=8 right now
    for row in range(width):
        line = "["
        for col in range(width):
            #right now, the "top" rows will be red; might have to change
            #this will need to be changed to if space is Empty/Piece and then check TeamColor
            if row < (board.n):
                line = line + (" " + "r" + " ")
            elif row > board.n * 2 - 2:
                line = line +  (" " + "b" + " ")
            else:
                line = line + ("   ")
        line = line + "]"
        print(line)



        

    #Play the game until there's a winner; should NOT be turned on right now
    """while board.is_winner() is None:
        print()
        print(board)
        print()
    """

    pass
