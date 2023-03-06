# Checkers Milestone 1: project-rukrainsky-kcorra-jaguirre3-sjdoepker
This repository contains a design and implementation for Checkers. The existing bugs and inefficiencies will be resolved by Milestone 3. 

- Robert Ukrainsky - Game Logic
- Kasey Corra - Bot
- Jaslin Aguirre - GUI
- Sam Doepker - TUI

## Changes to design since Milestone 1
- transferred almost all functionality in `Board` class to `Game` to make the game the center component of the user interfaces. 
- instead of individual `Piece`, `Empty`, and `King` classes, we added a `is_king` attribute to the `Piece` class and set all empty spaces to `None`
- added multiple functions to each component, including `checkers.py`, for the purposes of integration throughout both Milestones (see summary of changes below for details)
- got rid of ENUM for team color and instead used string `"Red"` and `"Black"` identifiers 

## Summary of changes we’ve made/missing functionality we’ve added since Milestone 2
- Robert (Game Logic) Changed the `list_moves_king` and `list_moves_piece` to be more concise.
Also added `get piece`,`add piece`, and `remove piece` methods to the board class to make it
transferable to other types of games. Also, methods that allow a team to request and accept
a draw were added to the `Game` class. 
- Kasey (Bot) updated the instructions for running the integrated bot more clearly in the README, as requested by the TA. Though she made little to no changes to the structure of her bot code after submitting for Milestone 2, she identified areas of `checkers.py` that needed to be corrected or implemented, and helped debug them in order to be able to run simulations on her bots using the `Game` class. 
- Jaslin (GUI) integrated the GUI with the Game Logic and made necessary changes to the code. I added an endscreen which displays the winner or if the game was a draw. I updated the filepaths to ensure the sprites ran correctly when on the main root of the repository and updated my docstrings. Finally, board generalization to other sizes was correctly implemented. 
- Sam (TUI) added functionality for showing all possible moves of a piece once selected and confirmed that piece and kings are shown differently. Also added support for board sizes between 6x6 and 20x20, integrated with game logic, and sanitized user input so that the program doesn't crash on an incorrect input.


## How we implemented the feedback from milestones 1 and 2
- We implemented a Game agnostic Board class and shifted all user interface calls to the Game class, as advised by the TA who reviewed our code after Milestone 1.
- This TA also advised us to combine the `Piece`, `Empty`, and `King` classes, which we did. 
- Robert (Game Logic) added `get_piece` and `remove_piece` functionality to the `Game` class after our Code Review meeting from Milestone 2
- Sam (TUI) added support for different board sizes, updated `select_piece` function to correctly show possible moves, and verified that kings and pieces are shown with different characters.
- Jaslin(GUI) added support for different board sizes. 

# Setup
Running the code in this repository requires using a number of Python libraries. We recommend creating a virtual environment before installing these libraries. To do so, run the following from the root of your local repository:
```
python3 -m venv venv
```
To activate your virtual environment, run the following:
```
source venv/bin/activate
```
You should now see `(venv)` in your terminal prompt, indicating that the virtual environment is active, e.g.:
```
(venv) student@linux1:~/repos/project-rukrainsky-kcorra-jaguirre3-sjdoepker$
```
To install the required Python libraries run the following:

```
pip3 install -r requirements.txt
```
To deactivate the virtual environment (e.g., because you're done working on or using the checkers code), just run the following:
```
deactivate
```
# Running the GUI
To run the GUI, run this from the root of the repository
```
python src/gui.py
```
By default, this will begin a game where a human player plays against the smart
bot. As the human player is Black, they must move first. 

To select a piece to move, click the piece. Once it has been selected, it will be
highlighted in green and the possible moves it can make will be highlighted in
yellow. To make a move, click on one of the highlighted pieces. To deselect the
piece simply click anywhere that's not highlighted in yellow.

To play a game with two human players on the same computer, run
```
python src/gui.py --red-type human
```

To make two bots play a game, run
```
python src/gui.py --black-type <bot> --red-type <bot>
```
where ```<bot>``` is ``smart-bot`` or ``random-bot``. When making two bots play
against it each other it is necessary to move your mouse around the pygame
window, so that pygame can recognize an event occuring. Otherwise the bots
will appear to 'freeze' and not move. 

To modify the number of rows and pieces on the board, run
```
python src/gui.py --num-piece-rows <int>
```
where ``<int>`` is the number of rows of pieces the checkerboard will have. 
The default is set to ``int=3`` as in a classic checkers game. Please note that when the board
gets big enough, the game is more likely to end in a draw because of the ```40-move-rule```.

# TUI

To run the TUI, run this from the root of the repository:
```
python3 src/tui.py
```
If this does not work, instead use:
```
python src/tui.py
```
    
Due to the size and layout of the board, it's recommended you run in a terminal
left or right-aligned, as it will appear taller than it is wide.

The TUI shows the current board state and asks the player for the location of
a piece to move with a text prompt. Rows are numbered 0 to width of the 
board - 1 from the top to bottom, and columns are numbered left to right in the
same way. There are indices showing the numbering of rows and columns on the 
left and bottom of the board to help. (note: the bottom indices do not appear
perfectly on boards of ``C > 4`` due to double-digit numbers- they will run off
the side)

Possible moves for the selected piece will be shown on the board with question
marks in the appropriate spaces. If you enter a move that is not valid for any
reason, you will be prompted to re-enter the move.

To modify the number of rows of pieces on the board, run
```
python3 src/tui.py --num-piece-rows <num>
```
where ``<num>`` is the number of rows of checkers pieces the board will have.
The default is ``num = 3`` (a standard checkerboard). This parameter must come 
before bot parameters when running the TUI. Please note that when the board
gets big enough, the game is more likely to end in a draw because of the ```40-move-rule```.


To play against a bot, run
```
python3 src/tui.py --player2 <bot>
```
where ``<bot>`` is ``random-bot`` or ``smart-bot``.

To have two bots play each other, run
```
python3 src/tui.py --player1 <bot> --player2 <bot>
```
The TUI inserts an artifical delay between each bot's move so you can see the 
game more easily. You can modify this delay using the ``--bot-delay <seconds>``
parameter.

# Bots
The `bots.py` file includes two classes:
- `RandomBot`: A bot that will just choose a move at random. 
- `SmartBot`: A bot that will try to make a winning move if possible. If not such move is possible, it checks whether the opposing player would win by the bot making a certain move and, if so, it does not make that move. 
    - It then checks if any move would make a piece a king. If so, it selects that move. If there are multiple such moves, it makes the following selections considering only those moves. If there are no king moves, it makes the following selections considering the all moves that were evaluated when looking for king moves.
    - The bot then finds the move that would result in the most number of jumps, or captures. If there are multiple such moves, it makes the following selections considering only those moves. If there are no jumping moves, it makes the following selections considering all moves that were evaluated when looking for maximum jumps.
    - The bot then finds the move with an end column closest to the center of the board. If there are multiple such moves, it chooses one of these moves at random. If there are no such moves, it picks a move at random from the moves that were evaluated when looking for centermost jumps.

These two classes are used in the TUI and GUI, but you can also run `bot.py` to run 1000 simulated games where two bots play each other (defaulted to one smart and one random), and see the percentage of wins and ties. For example:
```
$ python3 src/bot.py
Bot 1 (smart) wins: 99.40%
Bot 2 (random) wins: 0.00%
Ties: 0.60%

$ python3 src/bot.py --player1 random
Bot 1 (random) wins: 12.00%
Bot 2 (random) wins: 11.40%
Ties: 76.60%
```
Note: the 1000 game simulation should take about 2 minutes to run. For a faster result, control the number of games with the commend `python3 src/bot.py -n <num-games>`.


# Running with stubs and mocks
Stub and mock implementations of the Game class are available in the mocks.py file. After Milestone 2, we were focused on integration of the `Game` class with bots, GUI, and TUI. Because we were sucessful, there is no longer a need for stubs and mocks, and the `mocks.py` file is thus not up to date with our recent changes to other classes. 

The TUI and GUI both accept a `--mode <mode>` parameter, where `<mode>` is one of:
- `real`: Use the `Game`(default)
- `stub`: Use the `StubCheckerboard`
- `mock`: Use the `MockGame`

The GUI will print the board with some mock pieces if ```<mode> ``` is ```stub``. However, a piece cannot be selected and an error will be thrown. 
The GUI will print the board with mock pieces if ```<mode>``` is ```mock``. However, the first player is red and not black. When you click a red piece, its possible moves will be highlighted. However, the mock cannot move a piece and will throw an error.

The TUI does not work if `<mode>` is `stub` due to how stub is implemented.
The TUI will print the board with mock pieces if in `<mode> mock`. The player can choose a piece to move and mock possible spaces to move to will be highlighted. However, the game will throw an error and crash after entering a destination space.