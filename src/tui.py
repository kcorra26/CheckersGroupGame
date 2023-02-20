"""
TUI for Checkers
"""
import time 
from typing import Union, Dict



from checkers import TeamColor, Board, Empty, Piece, King

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


