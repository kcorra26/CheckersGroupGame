# project-rukrainsky-kcorra-jaguirre3-sjdoepker

Running the GUI
To run the GUI you will need the pygame libraries. 
In ipython 3, you should run the following commands:
import gui
import mocks
player = gui.GUIPlayer(mocks.MockGame(), gui.CheckersPlayer(), gui.CheckersPlayer())
player.play_checkers()
Once the pygame window opens it is blacks turn so click on a black piece. The selected
piece will be highlighted in green and all possible moves in yellow. To move click
on a highlighted yellow spot. After black moves its red's turn.
Note: the MockGame class initializes some pieces at completly random locations and
returns the same list of possible moves, as such the gui shown does not obey the rules
of checkers but will once it is integrated with checkers.py and utilizes an actual
Game object

Running the TUI
To run the TUI, you will need the Time, Colorama, Typing and Click libraries installed.
In the terminal from the root of the repository, run python3 tui.py --mode stub
Other versions of the TUI have not been fully tested or implemented yet. When
prompted for a team, enter either "Red" or "Black".