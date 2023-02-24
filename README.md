# project-rukrainsky-kcorra-jaguirre3-sjdoepker

- Robert Ukrainsky - Game Logic
- Kasey Corra - Bot
- Jaslin Aguirre - GUI
- Sam Doepker - TUI

Running the GUI
To run the GUI you will need the pygame library. 
In ipython 3, you should run the following commands:
import gui
import mocks
player = gui.GUIPlayer(mocks.MockGame(), gui.CheckersPlayer(), gui.CheckersPlayer())
player.play_checkers()
Once the pygame window opens it is black's turn so click on a black piece. The selected
piece will be highlighted in green and all possible moves in yellow. To move click
on a highlighted yellow spot. After black moves its red's turn.

To run GUI with the bot run the following commands:
player = GUIPlayer(mock.Game(), gui.CheckersPlayer(), gui.CheckersPlayer(SmartBot(ex_board, 'Red', 'Black')))
player.play_checkers()

Note: the MockGame class initializes some pieces at completly random locations and
returns the random list of possible moves, as such the gui shown does not obey the rules
of checkers but will once it is integrated with checkers.py and utilizes an actual
Game object. Similarly, because the bot is more attuned to the actual rules of checkers but
the gui only runs game.move_piece() when a move is returned by list_moves() which is a
predetermined set of locations that have been made up for testing purposes, this creates errors


Running the TUI
To run the TUI in the terminal from the root of the repository, 
run python3 src/tui.py --mode mock
Other versions of the TUI have not been fully tested or implemented yet. When
prompted for a team, enter either "Red" or "Black".
This will bring up a checkerboard with labels on the left and bottom of the board
to signify square locations to move pieces to. While the pieces do not move,
a set of locations marked as possible moves will be displayed as question marks.

Bots
The bots.py file includes two classes:
    - RandomBot: A bot that will just choose a move at random. 
    - SmartBot: A bot that will try to make a winning move if possible. If not such move is possible, it checks whether the opposing player would win by the bot making a certain move and, if so, it does not make that move. 
    It then checks if any move would make a piece a king. If so, it selects that move. If there are multiple such moves, it makes the following selections considering only those moves. If there are no king moves, it makes the following selections considering the all moves that do not result in the other team winning.
    The bot then finds the move that would result in the most number of jumps, or captures. If there are multiple such moves, it makes the following selections considering only those moves. If there are no jumping moves, it makes the following selections considering the king moves.
    The bot then finds the move with an end column closest to the center of the board. If there are multiple such moves, it chooses one of these moves at random. If there are no such moves, it picks a move at random from the king and max jump moves.
These two classes are used in the GUI and are integrated with the CheckersGameBotMock class in mocks.py (see instructions below). Due to the existing bugs in the Game class in checkers.py, the simulate() and cmd() functions do not yet operate as intended. 

Running with stubs and mocks
Stub and mock implementations of the Game class are available in the mocks.py file. 

The bots have their own mock class (CheckersGameBotMock), which can be used to test the efficacy of the bot like this:
    game = mocks.CheckersGameBotMock()
    smart = bot.SmartBot(game, "Red", "Black")
    smart.suggest_move()

