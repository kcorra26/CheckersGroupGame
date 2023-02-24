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
Once the pygame window opens it is blacks turn so click on a black piece. The selected
piece will be highlighted in green and all possible moves in yellow. To move click
on a highlighted yellow spot. After black moves its red's turn.

To run GUI with the bot run the following commands:
player = GUIPlayer(mock.Game(), gui.CheckersPlayer(), gui.CheckersPlayer(SmartBot(ex_board, 'Red', 'Black)))
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